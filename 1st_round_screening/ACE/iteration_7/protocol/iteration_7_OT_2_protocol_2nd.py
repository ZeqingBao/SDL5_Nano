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


    Drug_transfer = [90.65, 87.5, 76.65, 126.7, 81.9, 90.65, 51.1, 143.85, 80.15, 74.9, 145.95, 117.6, 105.0, 79.1, 165.2, 150.5]
    SL_1_transfer = [0.0, 0.0, 0.0, 50.05, 0.0, 27.65, 0.0, 10.15, 23.1, 0.0, 0.0, 61.95, 80.5, 100.45, 0.0, 44.45]
    SL_2_transfer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    SL_3_transfer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    LL_1_transfer = [0.0, 45.15, 51.45, 0.0, 81.9, 8.4, 88.9, 0.0, 0.0, 74.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    LL_2_transfer = [95.9, 91.35, 88.2, 50.75, 72.8, 94.5, 88.9, 65.8, 95.55, 74.9, 47.25, 52.15, 47.25, 37.45, 51.1, 31.15]
    LL_3_transfer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    P_1_transfer = [1.05, 0.0, 15.4, 3.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.8, 20.3, 0.0, 0.0, 0.0, 0.0, 0.0]
    P_2_transfer = [95.55, 57.75, 58.1, 0.0, 50.4, 59.5, 54.6, 0.0, 70.0, 74.9, 0.0, 0.0, 0.0, 29.4, 0.0, 0.0]
    P_3_transfer = [66.85, 68.25, 60.2, 118.65, 62.65, 68.95, 66.5, 130.2, 81.2, 47.6, 136.5, 117.95, 117.25, 103.95, 133.7, 123.9]

    S_1_transfer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    S_2_transfer = [332, 506, 534, 457, 508, 505, 500, 500, 519, 1000, 433, 500, 462, 447, 417, 454]
    S_3_transfer = [323, 494, 466, 0, 492, 495, 500, 0, 481, 0, 0, 0, 0, 4, 0, 0]

    Water_transfer = [344, 0, 0, 543, 0, 0, 0, 500, 0, 0, 567, 500, 538, 549, 583, 546]


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



    # # Step 1: ~30 min
    # protocol.pause("Decap Loc4: B1/B2/B3")
    # aqueous_organic_phase_prep ('aqueous')

    # # Step 2: ~16 min
    # protocol.pause("Decap Loc4: A1/A2/A3; Loc1: ALL")
    aqueous_organic_phase_prep ('organic')

    # Step 3: ~10 min
    formulation ()
    transfer_for_loading_size ('size')


