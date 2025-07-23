import os
import re
import pandas as pd
import numpy as np
from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.modelbridge.generation_strategy import GenerationStep, GenerationStrategy
from ax.modelbridge.factory import Models
from ax.core.observation import ObservationFeatures
from ax.models.torch.botorch_modular.surrogate import Surrogate
from botorch.models.gp_regression import SingleTaskGP
from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement



class BayesianOptimizer_Auto:
    @staticmethod
    def initialize_ax(random_seed=0):

        # Initialize the AxClient with a generation strategy
        gs = GenerationStrategy(
            steps=[
                GenerationStep(model=Models.SOBOL, num_trials=6, model_kwargs={"seed": 0}),
                GenerationStep(model=Models.BOTORCH_MODULAR, num_trials=-1, model_kwargs={"botorch_acqf_class": qLogNoisyExpectedHypervolumeImprovement, "surrogate": Surrogate(botorch_model_class=SingleTaskGP)} ),
            ]
        )
        ax_client = AxClient(generation_strategy=gs)

        # Set the design space for optimization
        ax_client.create_experiment(
            name="sdlnano",
            parameters=[

                # Drug_MW [0, 1000] ~ [0.0,1,0]
                {"name": "Drug_MW", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                # Drug_LogP [0, 10] ~ [0.0,1,0]
                {"name": "Drug_LogP", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                # Drug_TPSA [0, 1000] ~ [0.0,1,0]
                {"name": "Drug_TPSA", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                {"name": "Drug", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                {"name": "SL_1", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "SL_2", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "SL_3", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                {"name": "LL_1", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "LL_2", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "LL_3", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                {"name": "P_1", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "P_2", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "P_3", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

                {"name": "S_1", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "S_2", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "S_3", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},
                {"name": "Water", "type": "range", "bounds": [0.0, 1.0], "value_type": "float"},

            ],
            # Set the objective metrics for optimization
            objectives={

                "Solu": ObjectiveProperties(minimize=False),
                "Size": ObjectiveProperties(minimize=True),
                "Complexity": ObjectiveProperties(minimize=True),
                "PDI": ObjectiveProperties(minimize=True),
            },

        )
        return ax_client

    # Generate trials
    @staticmethod
    def generate_trials(ax_client, num_of_trials, drug, bopt=1):

        ax_client.generation_strategy._curr = ax_client.generation_strategy._steps[bopt]
        
        if drug == "ACE":
            drug_features = ObservationFeatures(parameters = {"Drug_MW": 0.354, "Drug_LogP": 0.391,  "Drug_TPSA": 0.067})

        # Get the trials data
        trials, _ = ax_client.get_next_trials(max_trials=num_of_trials, fixed_features=drug_features)

        # Prepare the trial data for DataFrame
        trials_data = []
        for trial_index, parameters in trials.items():
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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
    def get_iteration_number():

        current_dir = os.getcwd()

        folder_name = os.path.basename(current_dir)

        match = re.search(r"iteration_(\d+)", folder_name)
        if match:
            return int(match.group(1))
        else:
            raise ValueError("Wrong file")
    

    # Data normalization
    @staticmethod
    def normalize(data):

        df=data.copy()
        df['Size'] = df['Size'].apply(lambda x: min(1, x / 1000))
        df['Size_STD'] = df['Size_STD']/1000



        df['Complexity'] = df['Complexity'].apply(lambda x: x / 12)

        df['Solu'] = df['Solu'].apply(lambda x: x / 2000)
        df['Solu_STD'] = df['Solu_STD'].apply(lambda x: x / 2000)
        
        return df
    
    # Data denormalization
    @staticmethod
    def denormalize(data):

        df=data.copy()
        df['Size'] = df['Size'].apply(lambda x: x * 1000)
        df['Size_STD'] = df['Size_STD'].apply(lambda x: x * 1000)


        df['Complexity'] = df['Complexity'].apply(lambda x: x * 12)

        df['Solu'] = df['Solu'].apply(lambda x: x * 2000)
        df['Solu_STD'] = df['Solu_STD'].apply(lambda x: x * 2000)
        
        return df

