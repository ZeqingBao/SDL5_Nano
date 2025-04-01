from opentrons import protocol_api

metadata = {
    'author':'Zeqing Bao',
    'description':'SDLNano_Feb 2025',
    'apiLevel': '2.10'
}


def run(protocol: protocol_api.ProtocolContext):

    # Set up pipette tips (this should be done before setting up pipettes)
    p300t_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul','9')
    p300t_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul','10')
#    p300t_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul','11')
    
    # Set up Pipettes
    p300 = protocol.load_instrument ('p300_single_gen2', 'left',tip_racks=[p300t_1,p300t_2]) 
    p300_8 = protocol.load_instrument ('p300_multi_gen2', 'right',tip_racks=[p300t_1,p300t_2])

    # Set up pipette aspirating and dispensing flow rate
    p300.flow_rate.aspirate = 277.4
    p300.flow_rate.dispense = 277.4
    p300_8.flow_rate.aspirate = 277.4
    p300_8.flow_rate.dispense = 277.4
    p300.flow_rate.blow_out = 500
    p300_8.flow_rate.blow_out = 500


    safe_transfer_vol = 100
    surfactant_safe_transfer_vol = 150
    NP_aqueous_vol = 270
    NP_organic_vol = 30
    mixing_vol = 50
    
    # Set up Labwares
    lipid_drug_stock = protocol.load_labware('allenlab_8_wellplate_20000ul', '1')
    polymer_aqueous_stock = protocol.load_labware('allenlab_8_wellplate_20000ul', '4')
    stock_solution_mix = protocol.load_labware('allenlabresevoir_96_wellplate_2200ul','5')
#    loading_plate = protocol.load_labware('agilent_96_wellplate_500ul','6')
    size_plate = protocol.load_labware('corning_96_wellplate_360ul_flat','3')
    LNP = protocol.load_labware('corning_96_wellplate_360ul_flat','2')
    water_res = protocol.load_labware('nest_1_reservoir_290ml','6')
#    drug_extaction_solvent_res = protocol.load_labware('nest_1_reservoir_290ml','7')

    organic_components = ['Drug', 'SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3']
    aqueous_components = ['S_1', 'S_2', 'S_3', 'Water']

    SL_1_loc = lipid_drug_stock['A1']
    SL_2_loc = lipid_drug_stock['A2']
    SL_3_loc = lipid_drug_stock['A3']

    LL_1_loc = lipid_drug_stock['B1']
    LL_2_loc = lipid_drug_stock['B2']
    LL_3_loc = lipid_drug_stock['B3']
    Drug_loc = lipid_drug_stock['B4']

    P_1_loc = polymer_aqueous_stock['A1']    
    P_2_loc = polymer_aqueous_stock['A2']
    P_3_loc = polymer_aqueous_stock['A3']
    Water_loc = water_res['A1']

    S_1_loc = polymer_aqueous_stock['B1']    
    S_2_loc = polymer_aqueous_stock['B2']
    S_3_loc = polymer_aqueous_stock['B3']
    
#    Solvent_loc = drug_extaction_solvent_res['A1']


    Drug_transfer = [47.25, 85.05, 65.45, 0.0, 84.7, 48.65, 43.4, 83.65, 73.15, 84.7, 50.4, 40.95, 74.2, 113.4, 57.75, 15.05]
    SL_1_transfer = [0.0, 0.0, 40.95, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.4, 0.0, 0.0, 57.75, 0.0]
    SL_2_transfer = [0.0, 65.45, 0.0, 0.0, 84.7, 78.4, 112.35, 0.0, 73.15, 24.85, 108.85, 50.4, 0.0, 67.9, 57.75, 0.0]
    SL_3_transfer = [7.0, 10.15, 6.65, 0.0, 8.4, 6.3, 5.25, 5.6, 11.55, 7.35, 3.85, 1.4, 16.8, 0.0, 26.25, 7.0]

    LL_1_transfer = [11.2, 14.7, 11.2, 4.9, 11.9, 12.6, 6.3, 10.15, 11.55, 16.45, 4.55, 11.55, 20.3, 17.15, 34.65, 18.9]
    LL_2_transfer = [32.55, 51.8, 41.65, 0.0, 84.7, 46.9, 78.75, 83.65, 44.45, 112.35, 57.05, 43.4, 31.15, 113.4, 57.75, 39.2]
    LL_3_transfer = [78.75, 88.9, 65.45, 86.1, 75.95, 78.4, 103.6, 74.2, 73.15, 78.4, 108.85, 50.4, 93.1, 38.15, 57.75, 32.2]

    P_1_transfer = [16.1, 0.0, 0.0, 86.1, 0.0, 78.4, 0.0, 0.0, 0.0, 0.0, 16.45, 50.4, 0.0, 0.0, 0.0, 53.2]
    P_2_transfer = [78.75, 34.3, 65.45, 86.1, 0.0, 0.0, 0.0, 9.1, 63.35, 0.0, 0.0, 50.4, 21.7, 0.0, 0.0, 92.05]
    P_3_transfer = [78.75, 0.0, 53.9, 86.1, 0.0, 0.0, 0.0, 83.65, 0.0, 25.9, 0.0, 0.0, 93.1, 0.0, 0.0, 92.05]

    S_1_transfer = [741, 333, 683, 400, 132, 500, 0, 333, 0, 359, 511, 500, 913, 0, 0, 972]
    S_2_transfer = [49, 183, 153, 201, 434, 0, 435, 333, 459, 319, 81, 0, 0, 352, 500, 0]
    S_3_transfer = [210, 0, 40, 400, 0, 0, 59, 333, 0, 0, 191, 0, 0, 296, 0, 28]

    Water_transfer = [0, 484, 124, 0, 434, 500, 507, 0, 541, 323, 217, 500, 87, 352, 500, 0]


    component_data = {
        'Drug': {'loc': Drug_loc, 'transfer': Drug_transfer},
        'SL_1': {'loc': SL_1_loc, 'transfer': SL_1_transfer},
        'SL_2': {'loc': SL_2_loc, 'transfer': SL_2_transfer},
        'SL_3': {'loc': SL_3_loc, 'transfer': SL_3_transfer},

        'LL_1': {'loc': LL_1_loc, 'transfer': LL_1_transfer},
        'LL_2': {'loc': LL_2_loc, 'transfer': LL_2_transfer},
        'LL_3': {'loc': LL_3_loc, 'transfer': LL_3_transfer},
        'P_1': {'loc': P_1_loc, 'transfer': P_1_transfer},
        'P_2': {'loc': P_2_loc, 'transfer': P_2_transfer},
        'P_3': {'loc': P_3_loc, 'transfer': P_3_transfer},
        'Water': {'loc': Water_loc, 'transfer': Water_transfer},
        'S_1': {'loc': S_1_loc, 'transfer': S_1_transfer},
        'S_2': {'loc': S_2_loc, 'transfer': S_2_transfer},
        'S_3': {'loc': S_3_loc, 'transfer': S_3_transfer}
    }


    # safe transfer
    def safe_transfer(pipette, source, volume, to, max_volume):

        if volume <= max_volume:
            pipette.transfer(volume, source, to, new_tip='never')
        if volume > max_volume:
            steps = volume // max_volume
            remainder = volume % max_volume
            if remainder > 0:
                steps = steps + 1
            steps_volume = volume/steps
            for i in range(int(steps)):
                pipette.transfer(steps_volume, source, to, blow_out=True, blowout_location='destination well', new_tip='never')


        

    def matrix(pipette, stock, destination, volume, start_column, aqueous_or_organic= 'organic', rows=8, columns=2):
        letters = ['A','B','C','D','E','F','G','H']
        numbers = ['1','2','3','4','5','6','7','8','9','10','11','12']
        i=0

        if (aqueous_or_organic == 'organic'):
            pipette.pick_up_tip()
        for x in range (rows):
            if (aqueous_or_organic == 'aqueous'):
                pipette.pick_up_tip()
            for y in range (start_column, start_column + columns):
               character = letters[x]
               num = numbers[y]
               if (aqueous_or_organic == 'organic'):
                   if (volume[i]>0):
                       safe_transfer(pipette,stock,volume[i],destination[character + num],safe_transfer_vol)   
               if (aqueous_or_organic == 'aqueous'):
                   if (volume[i]>0):
                       safe_transfer(pipette,stock,volume[i],destination[character + num],surfactant_safe_transfer_vol)  
                       pipette.dispense(300)
               i=i+1
            if (aqueous_or_organic == 'aqueous'):
                pipette.drop_tip()

        if (aqueous_or_organic == 'organic'):
            pipette.drop_tip()

    def aqueous_organic_phase_prep (aqueous_or_organic):

        # Position of pipette aspirating and dispensing position (distance (mm) above the labware bottom)
        p300.well_bottom_clearance.dispense = 30
        p300.well_bottom_clearance.aspirate = 3


        if aqueous_or_organic == 'aqueous':

            components = aqueous_components
            start_column = 2

        if aqueous_or_organic == 'organic':

            components = organic_components
            start_column = 0


        # Process aqueous components
        for component in components:

            stock_loc = component_data[component]['loc']
            stock_vol = component_data[component]['transfer']


            matrix(
                pipette=p300,
                stock = stock_loc,
                destination = stock_solution_mix,
                volume = stock_vol,
                start_column=start_column,
                aqueous_or_organic = aqueous_or_organic
            )



        if aqueous_or_organic == 'organic':
            p300_8.well_bottom_clearance.dispense = 4
            p300_8.well_bottom_clearance.aspirate = 3

            for i in range(start_column, start_column+2):
                p300_8.pick_up_tip()
                p300_8.mix(5, 50, stock_solution_mix.rows()[0][i])
                p300_8.drop_tip()

        if aqueous_or_organic == 'aqueous':
            p300_8.well_bottom_clearance.dispense = 10
            p300_8.well_bottom_clearance.aspirate = 3
            for i in range(start_column, start_column+2):
                p300_8.pick_up_tip()
                p300_8.mix(5, 100, stock_solution_mix.rows()[0][i])
                for j in range (0,3):
                    p300_8.transfer(NP_aqueous_vol, stock_solution_mix.rows()[0][i], LNP.rows()[0][(i-2)*3+j],blow_out=True, blowout_location='destination well', new_tip='never')
                    p300_8.dispense(300)
                p300_8.drop_tip()


    # Formulation: inject 30 uL of organic phase to 270 of aqueous phase and mix them
    def formulation():

        # Position of pipette aspirating and dispensing position (distance (mm) above the labware bottom)  
        p300_8.well_bottom_clearance.dispense = 4
        p300_8.well_bottom_clearance.aspirate = 4

        for i in range(0,2):
            for j in range (0,3):
                p300_8.pick_up_tip()
                p300_8.transfer(NP_organic_vol, stock_solution_mix.rows()[0][i],LNP.rows()[0][i*3+j],mix_after=(20, mixing_vol),new_tip='never')
                p300_8.drop_tip()


    def transfer_for_loading_size(type):

        # Position of pipette aspirating and dispensing position (distance (mm) above the labware bottom)  
        p300_8.well_bottom_clearance.dispense = 4
        p300_8.well_bottom_clearance.aspirate = 4

        # if type == 'loading':
        #     NP_vol = 20
        #     dilution_factor = 12
        #     dilutant_loc = Solvent_loc
        #     analysis_plate = loading_plate
        #     repeat = 2
        #     mixing_time = 10

        if type == 'size':
            NP_vol = 20
            dilution_factor = 10
            dilutant_loc = Water_loc
            analysis_plate = size_plate
            repeat = 1
            mixing_time = 3

        dilutant_vol = NP_vol * (dilution_factor - 1)

        p300_8.pick_up_tip()
        for n in range(repeat):
            for i in range(6):
                p300_8.transfer(dilutant_vol/repeat, dilutant_loc, analysis_plate.rows()[0][i],blow_out=True, blowout_location='destination well',new_tip='never')
                p300_8.dispense(300)
        p300_8.drop_tip()

        for i in range(0,6):
            p300_8.pick_up_tip()
            p300_8.transfer(NP_vol, LNP.rows()[0][i], analysis_plate.rows()[0][i], new_tip='never', mix_after=(mixing_time, mixing_vol))
            p300_8.drop_tip() 



    # Step 1: ~30 min
#    protocol.pause("Decap Loc4: B1/B2/B3")
    aqueous_organic_phase_prep ('aqueous')

    # # Step 2: ~16 min
    # protocol.pause("Decap Loc4: A1/A2/A3; Loc1: ALL")
    # aqueous_organic_phase_prep ('organic')

    # # Step 3: ~10 min
    # formulation ()
    # transfer_for_loading_size ('size')


