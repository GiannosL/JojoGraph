import streamlit as st

from source import JOJO_PART_NAMES
from source.data.relations import get_relations
from source.data.configuration import parse_configuration


# grab configuration file
config = parse_configuration(filename='data/configuration.yaml')

#
st.set_page_config(page_title="Jojo\'s bizarre adventure", layout="wide")

# select which season to plot
_, col2, _ = st.columns([1, 3, 1])
jojo_part = col2.selectbox(
    label='Select Jojo part', 
    options=JOJO_PART_NAMES.keys(), 
    index=(len(JOJO_PART_NAMES)-1)
    )

if jojo_part:
    jojo_graph = get_relations(part_number=JOJO_PART_NAMES[jojo_part], 
                               config_dict=config)
    
    jojo_graph_network = jojo_graph.get_plot()
    st.plotly_chart(jojo_graph_network, use_container_width=True)
