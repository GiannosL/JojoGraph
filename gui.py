import streamlit as st
from source.data.relations import get_relations
from source.data.configuration import parse_configuration


# Jojo parts
JOJO_PART_NAMES = {
    'Phantom blood': 'part_1', 
    'Battle tendency': 'part_2', 
    'Stardust crusaders': 'part_3',
    'Diamond is unbreakable': 'part_4', 
    'Golden wind': 'part_5', 
    'Stone ocean': 'part_6',
    'Steel ball run': 'part_7', 
    'Jojolion': 'part_8', 
    'The Jojolands': 'part_9', 
    '': None
    }

# grab configuration file
config = parse_configuration(filename='data/configuration.yaml')

#
st.set_page_config(page_title="Jojo\'s bizarre adventure", layout="wide")

# select which season to plot
jojo_part = st.selectbox(
    label='Select Jojo part', 
    options=JOJO_PART_NAMES.keys(), 
    index=(len(JOJO_PART_NAMES)-1)
    )

if jojo_part:
    jojo_graph = get_relations(part_number=JOJO_PART_NAMES[jojo_part], 
                               config_dict=config)
    
    jojo_graph_network = jojo_graph.get_plot()
    st.plotly_chart(jojo_graph_network, use_container_width=True)
