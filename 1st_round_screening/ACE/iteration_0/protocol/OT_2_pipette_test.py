from opentrons import protocol_api

metadata = {
    'author':'Zeqing Bao',
    'description':'SDLNano_Feb 2025',
    'apiLevel': '2.10'
}


def run(protocol: protocol_api.ProtocolContext):

    # Set up pipette tips (this should be done before setting up pipettes)
    p300t_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul','10')
    p300t_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul','11')
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

    # Set up pipette aspirating and dispensing position 
    safe_transfer_vol = 100
    surfactant_safe_transfer_vol = 150
    NP_aqueous_vol = 270
    NP_organic_vol = 30
    mixing_vol = 50
    
#     # Set up Labwares
#     lipid_drug_stock = protocol.load_labware('allenlab_8_wellplate_20000ul', '4')
#     polymer_aqueous_stock = protocol.load_labware('allenlab_8_wellplate_20000ul', '8')
#     stock_solution_mix = protocol.load_labware('allenlabresevoir_96_wellplate_2200ul','5')
# #    loading_plate = protocol.load_labware('agilent_96_wellplate_500ul','6')
#     size_plate = protocol.load_labware('corning_96_wellplate_360ul_flat','1')
#     LNP = protocol.load_labware('corning_96_wellplate_360ul_flat','2')
#     water_res = protocol.load_labware('nest_1_reservoir_290ml','7')
# #    drug_extaction_solvent_res = protocol.load_labware('nest_1_reservoir_290ml','7')

#     # Define organic/aqueous components
#     organic_components = ['Drug', 'SL_1', 'SL_2', 'SL_3', 'LL_1', 'LL_2', 'LL_3', 'P_1', 'P_2', 'P_3']
#     aqueous_components = ['S_1', 'S_2', 'S_3', 'Water']

#     # Define the stock solution loacations
#     SL_1_loc = lipid_drug_stock['A1']
#     SL_2_loc = lipid_drug_stock['A2']
#     SL_3_loc = lipid_drug_stock['A3']

#     LL_1_loc = lipid_drug_stock['B1']
#     LL_2_loc = lipid_drug_stock['B2']
#     LL_3_loc = lipid_drug_stock['B3']
#     Drug_loc = lipid_drug_stock['B4']

#     P_1_loc = polymer_aqueous_stock['A1']    
#     P_2_loc = polymer_aqueous_stock['A2']
#     P_3_loc = polymer_aqueous_stock['A3']
    

#     S_1_loc = polymer_aqueous_stock['B1']    
#     S_2_loc = polymer_aqueous_stock['B2']
#     S_3_loc = polymer_aqueous_stock['B3']
#     Water_loc = water_res['A1']
    

    def test(pipette):
        pipette.pick_up_tip()
        pipette.drop_tip()



    test(p300)
    test(p300_8)