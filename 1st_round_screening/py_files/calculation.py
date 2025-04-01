import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class BatchCalculation:
    # Set up the experimental parameters
    organic_stock_conc = 20
    properties = {
        "Setup": {
            "Organic mix vol": 350,  # µL
            "Aqueous mix vol": 1000,  # µL

            "Organic phase vol": 30,  # µL
            "Aqueous phase vol": 270,  # µL
            
            "Organic batch size": 600,  # (Drug + P + SL + LL) µg <= 600 due to the stock solution conc and organic phase vol
            "Aqueous batch size": 2700,  # (S + Water) µg == 2700 due to the stock solution conc and aqueous phase vol
        },
        
        "Drug": {"Stock solution conc": organic_stock_conc},
        "P_1": {"Stock solution conc": organic_stock_conc},
        "P_2": {"Stock solution conc": organic_stock_conc},
        "P_3": {"Stock solution conc": organic_stock_conc},
        "SL_1": {"Stock solution conc": organic_stock_conc},
        "SL_2": {"Stock solution conc": organic_stock_conc},
        "SL_3": {"Stock solution conc": organic_stock_conc},
        "LL_1": {"Stock solution conc": organic_stock_conc},
        "LL_2": {"Stock solution conc": organic_stock_conc},
        "LL_3": {"Stock solution conc": organic_stock_conc},

        # 10 mg/mL <=> 10 µg/µL <=> 1% w/v%
        "S_1": {"Stock solution conc": 10},
        "S_2": {"Stock solution conc": 10},
        "S_3": {"Stock solution conc": 10},
        "Water": {"Stock solution conc": 10},
    }

    organic_cols_to_convert = ['Drug', 'SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3']
    aqueous_cols_to_convert = ['S_1', 'S_2', 'S_3', 'Water']



    # Convert the target ratio to the transfer volume (organic)
    @staticmethod
    def organic_converter(target_ratio, stock_solution_conc):
        batch_size = BatchCalculation.properties["Setup"]["Organic batch size"]
        phase_volume = BatchCalculation.properties["Setup"]["Organic phase vol"]
        mix_vol = BatchCalculation.properties["Setup"]["Organic mix vol"]

        target_mass = target_ratio * batch_size
        mix_conc = target_mass / phase_volume
        mix_mass = mix_conc * mix_vol
        transfer_vol = mix_mass / stock_solution_conc

        return transfer_vol

    # Convert the target ratio to the transfer volume (aqueous)
    @staticmethod
    def aqueous_converter(target_ratio, stock_solution_conc):
        batch_size = BatchCalculation.properties["Setup"]["Aqueous batch size"]
        phase_volume = BatchCalculation.properties["Setup"]["Aqueous phase vol"]
        mix_vol = BatchCalculation.properties["Setup"]["Aqueous mix vol"]

        target_mass = target_ratio * batch_size
        mix_conc = target_mass / phase_volume
        mix_mass = mix_conc * mix_vol
        transfer_vol = mix_mass / stock_solution_conc

        return transfer_vol


    # Convert the target ratio to the transfer volume (all)
    @staticmethod
    def converter(dataset):
        transfer_df = dataset.copy()
        for col in BatchCalculation.organic_cols_to_convert:
            transfer_df[col] = BatchCalculation.organic_converter(
                dataset[col], BatchCalculation.properties[col]["Stock solution conc"]
            )


        for col in BatchCalculation.aqueous_cols_to_convert:
            transfer_df[col] = BatchCalculation.aqueous_converter(
                dataset[col], BatchCalculation.properties[col]["Stock solution conc"]
            )


        organic_mix_vol = BatchCalculation.properties["Setup"]["Organic mix vol"]

        transfer_df["Solvent"] = organic_mix_vol - (
            transfer_df["Drug"]
            + transfer_df["P_1"]
            + transfer_df["P_2"]
            + transfer_df["P_3"]
            + transfer_df["SL_1"]
            + transfer_df["SL_2"]
            + transfer_df["SL_3"]
            + transfer_df["LL_1"]
            + transfer_df["LL_2"]
            + transfer_df["LL_3"]
        )

        transfer_df = transfer_df.round(2)
        return transfer_df

    # Write the transfer volume to OT2 protocols
    @staticmethod
    def update_transfer_script(script_path, excel_data_path, output_path):
        # Read the script
        with open(script_path, 'r') as file:
            script_lines = file.readlines()

        # Columns to update in the script
        transfer_columns = ['Drug', 'SL_1', 'SL_2', 'SL_3', 
                            'LL_1', 'LL_2', 'LL_3', 
                            'P_1', 'P_2', 'P_3', 
                            'S_1', 'S_2', 'S_3', 
                            'Water']

        # Map Excel column names to script variable names
        transfer_mapping = {col: f"{col}_transfer" for col in transfer_columns}

        # Load Excel data into a dictionary {col: [values]}
        excel_data = pd.read_excel(excel_data_path)
        transfer_data = {col: excel_data[col].dropna().tolist() for col in transfer_columns}

        # Prepare updated script lines
        updated_lines = []
        for line in script_lines:
            stripped_line = line.strip()
            for col, var in transfer_mapping.items():
                if stripped_line.startswith(f"{var} ="):
                    # Capture leading indentation
                    leading_whitespace = line[:len(line) - len(line.lstrip())]
                    # Format values from Excel data
                    formatted_values = ", ".join(map(str, transfer_data[col]))
                    line = f"{leading_whitespace}{var} = [{formatted_values}]\n"
                    break  # No need to check further columns
            updated_lines.append(line)



        with open(output_path, 'w', encoding='utf-8') as file:
            for line in updated_lines:
                    file.write(line)

        with open(output_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.lstrip('\ufeff')
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return output_path

    # Obtain the formulation parameters and formulation complexity
    @staticmethod 
    def parameters_and_complexity(iteration):

        file_path_unprocessed = 'data/unlabeled_' + str(iteration) + '.xlsx'
        file_path_processed = 'data/unlabeled_processed_' + str(iteration) + '.xlsx'
        
        unprocessed = pd.read_excel(file_path_unprocessed)
        results = pd.read_excel(file_path_processed)

        # List of columns to check for non-zero values
        columns_to_check = ['SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3', 'S_1', 'S_2', 'S_3']

        # Calculate the Complexity column as the count of non-zero entries in the specified columns
        unprocessed['Complexity'] = unprocessed[columns_to_check].apply(lambda row: (row != 0).sum(), axis=1)


        results['Complexity'] = unprocessed['Complexity'].values
        results['Complexity_STD'] = 0

        to_drop = ["Solu", "Solu_STD", "Size", "Size_STD", "PDI", "PDI_STD"]
        results = results.drop(to_drop, axis=1)

        return results


    # Obtain the size and PDI data
    @staticmethod 
    def size_raw(iteration):

        size_raw = pd.read_csv("results/iteration_" + str(iteration) + "_size.csv", encoding="latin-1")
        size_raw.rename(columns={'Diameter (nm)': 'Size'}, inplace=True)

        size_raw = size_raw[["Data Quality", "Item", "Size", "PD Index"]]
        
        return size_raw



    # Process the data based on the formulation quality: 1 Good; 0 Bad
    @staticmethod
    def process_formulations(df):
        # Initialize lists to store results
        formulations = []
        mean_size = []
        std_size = []
        mean_pdi = []
        std_pdi = []
        formulation_quality = []

        
        # Iterate over the DataFrame in chunks of 3 rows
        for i in range(0, len(df), 3):
            group = df.iloc[i:i+3]
            good_quality_data = group[group['Data Quality'] == 'Good']
            good_count = len(good_quality_data)
            
            if good_count == 3:
                # All three are good
                formulations.append(f'Formulation {i//3 + 1}')
                mean_size.append(good_quality_data['Size'].mean())
                std_size.append(good_quality_data['Size'].std())
                mean_pdi.append(good_quality_data['PD Index'].mean())
                std_pdi.append(good_quality_data['PD Index'].std())

                formulation_quality.append(1)
            elif good_count == 2:
                # Two are good
                formulations.append(f'Formulation {i//3 + 1}')
                mean_size.append(good_quality_data['Size'].mean())
                std_size.append(good_quality_data['Size'].std())
                mean_pdi.append(good_quality_data['PD Index'].mean())
                std_pdi.append(good_quality_data['PD Index'].std())

                formulation_quality.append(1)
            else:
                # One or none are good
                formulations.append(f'Formulation {i//3 + 1}')
                mean_size.append(1000)
                std_size.append(0)
                mean_pdi.append(1)
                std_pdi.append(0)
                formulation_quality.append(0)

        
        # Create the new DataFrame
        result_df = pd.DataFrame({
            'Formulation': formulations,
            'Size': mean_size,
            'Size_STD': std_size,
            'PDI': mean_pdi,
            'PDI_STD': std_pdi,
            'Formulation Quality': formulation_quality,
        })
        
        return result_df

