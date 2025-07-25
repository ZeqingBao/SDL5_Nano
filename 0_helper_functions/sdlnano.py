import os
import re
import pandas as pd
import numpy as np
from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.modelbridge.generation_strategy import GenerationStep, GenerationStrategy
#from ax.modelbridge.factory import Models
from ax.modelbridge.registry import Generators as Models

from ax.core.observation import ObservationFeatures
from ax.models.torch.botorch_modular.surrogate import Surrogate
from botorch.models.gp_regression import SingleTaskGP
from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement

from ax import Client
from ax.api.configs import RangeParameterConfig
from ax.api.protocols.metric import IMetric
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Generators as Models
from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement
from ax.models.torch.botorch_modular.surrogate import Surrogate
from botorch.models import SingleTaskGP

from ax.api.configs import (
    ChoiceParameterConfig,
    RangeParameterConfig,
)

def initialize_ax(SOBOL_trials: int = 16, max_excipients: int = 12) -> Client:
    # 1) Define a custom GenerationStrategy
    gs = GenerationStrategy(
        steps=[
            GenerationStep(
                model=Models.SOBOL,
                num_trials=SOBOL_trials,
                model_kwargs={"seed": 0},
            ),
            GenerationStep(
                model=Models.BOTORCH_MODULAR,
                num_trials=-1,
                model_kwargs={
                    "botorch_acqf_class": qLogNoisyExpectedHypervolumeImprovement,
                    "surrogate": Surrogate(botorch_model_class=SingleTaskGP),
                },
            ),
        ]
    )

    client = Client()


    # 2) Configure experiment with binary “use” + conditional ratio
    parameters = []
    for name in [
        "SL_1", "SL_2", "SL_3",
        "LL_1", "LL_2", "LL_3",
        "P_1",  "P_2",  "P_3",
        "S_1",  "S_2",  "S_3",
        "Water",
    ]:
        # binary flag
        parameters.append(
            ChoiceParameterConfig(
                name=f"use_{name}",
                parameter_type="choice",
                values=[0, 1],
            )
        )
        # ratio, only if used
        parameters.append(
            RangeParameterConfig(
                name=name,
                parameter_type="float",
                bounds=(0.0, 1.0),
                # condition: name only active when use_name == 1
                conditions=[{"use_{}".format(name): 1}],
            )
        )

    client.configure_experiment(
        parameters=parameters,
        parameter_constraints=[
            # sum of all use_* flags ≤ max_excipients
            " + ".join(f"use_{n}" for n in [
                "SL_1","SL_2","SL_3",
                "LL_1","LL_2","LL_3",
                "P_1", "P_2", "P_3",
                "S_1", "S_2", "S_3",
                "Water",
            ]) + f" <= {max_excipients}"
        ],
    )

    # 3) Attach your GS  
    client.set_generation_strategy(gs)

    # 4) Only register the *actual* metrics you care to optimize
    client.configure_metrics(
        metrics=[
            IMetric(name="Solu"),
            IMetric(name="Size"),
            IMetric(name="PDI"),
        ]
    )

    # 5) Multi‑objective optimize just those three
    client.configure_optimization(
        objective="Solu, -Size, -PDI",
        # no outcome_constraints at all
    )

    return client



def virtual_experiment(df): # only for testing purposes

    # Define weights for each feature per objective
    weights = {
        'Solu': {
            'SL_1':  0.30, 'SL_2': -0.0, 'SL_3':  0.10,
            'LL_1':  0.0, 'LL_2': -0.05, 'LL_3':  0.00,
            'P_1':   0.10, 'P_2': -0.10, 'P_3':  0.00,
            'S_1':   0.0, 'S_2':  0.0, 'S_3': -0.0,
            'Water': 0.20
        },
        'Size': {
            'SL_1': -0.0, 'SL_2':  0.20, 'SL_3':  0.0,
            'LL_1':  0.30, 'LL_2': -0.0, 'LL_3':  0.0,
            'P_1':   0.0, 'P_2':  0.10, 'P_3': -0.10,
            'S_1':   0.00, 'S_2':  0.05, 'S_3':  0.10,
            'Water': 0.15
        },
        'PDI': {
            'SL_1':  0.05, 'SL_2':  0.05, 'SL_3': -0.0,
            'LL_1':  0.10, 'LL_2':  0.10, 'LL_3': -0.0,
            'P_1':   0.0, 'P_2': -0.0, 'P_3':  0.20,
            'S_1':  -0.0, 'S_2':  0.10, 'S_3':  0.05,
            'Water': -0.0
        }
    }
    

    out = df.copy()
    for obj_name, w in weights.items():
        # compute raw weighted sum
        raw = sum(out[col] * coef for col, coef in w.items())

        # # min-max normalize to [0,1]
        # min_val, max_val = raw.min(), raw.max()
        # if max_val > min_val:
        #     normed = (raw - min_val) / (max_val - min_val)
        # else:
        #     normed = raw * 0.0  # fallback if no variation

        # # ensure within [0,1]
        # out[obj_name] = normed.clip(0, 10)
        out[obj_name] = raw

        out[obj_name + '_STD'] = 0.0  # add a dummy STD column

    # List of columns to check for non-zero values
    columns_to_check = ['SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3', 'S_1', 'S_2', 'S_3']

    # Calculate the Complexity column as the count of non-zero entries in the specified columns
    out['Complexity'] = out[columns_to_check].apply(lambda row: (row != 0).sum(), axis=1)


    # out['Complexity'] = out['Complexity'].values
    # out['Complexity_STD'] = 0

    return out
    

# Generate trials
def generate_trials(ax_client, num_of_trials, drug, bopt=1):
    # Advance to the desired generation‐strategy step
    ax_client._generation_strategy._curr = ax_client._generation_strategy._steps[bopt]

    # Ask the Client for the next batch of trials (only max_trials is supported)
    trials = ax_client.get_next_trials(max_trials=num_of_trials)  # :contentReference[oaicite:0]{index=0}

    # Build a DataFrame, overriding drug features manually since fixed_features isn't supported
    trials_data = []
    for trial_index, parameters in trials.items():
        if drug == "ACE":
            parameters["Drug_MW"]  = 0.354
            parameters["Drug_LogP"] = 0.391
            parameters["Drug_TPSA"] = 0.067

        trials_data.append(
            {
                "trial_index": trial_index,
                **parameters,
                "Solu": None,
                "Solu_STD": None,
                "Size": None,
                "Size_STD": None,
                "PDI": None,
                "PDI_STD": None,
                "Complexity": None,
                "Complexity_STD": None,
            }
        )

    return pd.DataFrame(trials_data), ax_client


# Process the data to obtain the drug/excipient ratios
def process_trails(data):

    df = data.copy()

    cols_organic = ['Drug', 'SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3']
    cols_auqeous = ['S_1', 'S_2', 'S_3', 'Water']

    cols = [cols_organic, cols_auqeous]

    for col in cols:
        sums = df[col].sum(axis=1)
        df[col] = df[col].div(sums, axis=0).round(3)


    df['Drug_MW'] = df['Drug_MW'] * 1000
    df['Drug_LogP'] = df['Drug_LogP'] * 10
    df['Drug_TPSA'] = df['Drug_TPSA'] * 1000

    return df


# Load the data to complete the trails
def load_labeled_data(ax_client, labeled_data_path):
    labeled_data = pd.read_excel(labeled_data_path)
    for _, row in labeled_data.iterrows():
        trial_index = int(row["trial_index"])
        raw_data = {
            "Solu": (row["Solu"], row["Solu_STD"]),
            "Size": (row["Size"], row["Size_STD"]),
            "PDI": (row["PDI"], row["PDI_STD"]),
            "Complexity": (row["Complexity"], row["Complexity_STD"]),
        }
        
        ax_client.complete_trial(trial_index=trial_index, raw_data=raw_data)

    return ax_client


# Obtain the iteration number
def get_iteration_number():

    current_dir = os.getcwd()

    folder_name = os.path.basename(current_dir)

    match = re.search(r"iteration_(\d+)", folder_name)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Wrong file")


# Data normalization
def normalize(data):

    df=data.copy()
    df['Size'] = df['Size'].apply(lambda x: min(1, x / 1000))
    df['Size_STD'] = df['Size_STD']/1000



    df['Complexity'] = df['Complexity'].apply(lambda x: x / 12)

    df['Solu'] = df['Solu'].apply(lambda x: x / 2000)
    df['Solu_STD'] = df['Solu_STD'].apply(lambda x: x / 2000)
    
    return df

# Data denormalization
def denormalize(data):

    df=data.copy()
    df['Size'] = df['Size'].apply(lambda x: x * 1000)
    df['Size_STD'] = df['Size_STD'].apply(lambda x: x * 1000)


    df['Complexity'] = df['Complexity'].apply(lambda x: x * 12)

    df['Solu'] = df['Solu'].apply(lambda x: x * 2000)
    df['Solu_STD'] = df['Solu_STD'].apply(lambda x: x * 2000)
    
    return df

