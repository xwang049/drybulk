import pandas as pd
import streamlit as st
import plotly.graph_objects as go

file_path = 'Filtered_CY2024.csv'

cy_data = pd.read_csv(file_path)


st.title("Interactive Sankey Diagram for CY Data")
st.write("Use the dropdown filters to dynamically generate a Sankey diagram. By default, Carrier Name is not selected.")


selected_data = cy_data[['Carrier Name', 'Port', 'Destination']]


carrier_filter = st.multiselect(
    "Select Carrier Names (Default: None):",
    options=selected_data['Carrier Name'].unique(),
    default=[]
)


port_filter = st.multiselect(
    "Select Ports:",
    options=selected_data['Port'].unique(),
    default=selected_data['Port'].unique()
)


destination_filter = st.multiselect(
    "Select Destinations:",
    options=selected_data['Destination'].unique(),
    default=selected_data['Destination'].unique()
)


filtered_data = selected_data[
    ((selected_data['Carrier Name'].isin(carrier_filter)) | (len(carrier_filter) == 0)) &  # Carrier Name 可为空
    (selected_data['Port'].isin(port_filter)) &
    (selected_data['Destination'].isin(destination_filter))
]


sankey_data = filtered_data.groupby(['Carrier Name', 'Port', 'Destination']).size().reset_index(name='Count')


unique_carriers = sankey_data['Carrier Name'].unique()
unique_ports = sankey_data['Port'].unique()
unique_destinations = sankey_data['Destination'].unique()

all_nodes = list(unique_carriers) + list(unique_ports) + list(unique_destinations)
node_dict = {node: i for i, node in enumerate(all_nodes)}

sankey_data['Source'] = sankey_data['Carrier Name'].map(node_dict)
sankey_data['Intermediate'] = sankey_data['Port'].map(node_dict)
sankey_data['Target'] = sankey_data['Destination'].map(node_dict)


fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes
    ),
    link=dict(
        source=list(sankey_data['Source']) + list(sankey_data['Intermediate']),
        target=list(sankey_data['Intermediate']) + list(sankey_data['Target']),
        value=list(sankey_data['Count']) + list(sankey_data['Count'])
    )
)])


fig.update_layout(
    title_text="Sankey Diagram with Filtered Data (Default: No Carrier Names)",
    font_size=10,
    width=1400,
    height=800
)


st.plotly_chart(fig, use_container_width=True)
