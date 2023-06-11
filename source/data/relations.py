import networkx as nx
import plotly.graph_objects as go
from source.utilities.util_functions import validate_path, parse_characters, parse_interactions, parse_colors, get_image_names
import re
import os
from PIL import Image

class Relations:
    def __init__(self, interaction_list, interaction_types, 
                 character_dict, color_dict):
        self.categories = character_dict
        self.colors = color_dict
        self.inter_types = interaction_types
        self.graph = self._get_graph(interactions=interaction_list)

    def _get_graph(self, interactions):
        """
        create a graph from the edgelist
        """
        my_graph = nx.Graph()
        my_graph.add_edges_from(interactions)

        return my_graph
    
    def get_edges(self):
        return self.graph
    
    def _add_images(self, fig):
        # TODO make own class for plot
        xVals = fig['data'][1]['x']
        yVals = fig['data'][1]['y']
        names = fig['data'][1]['text']

        character_images_names= get_image_names()

        for i in range(0, len(xVals)):  

            pattern = r'Name: (.*?)<br>'
            match = re.search(pattern, names[i])
            name = match.group(1) 
      
            if name in character_images_names:
                picture = 'data/node_pictures/' + name + ".jpeg"
                picture= Image.open(picture)
                
                fig.add_layout_image(dict(
                source=picture,
                x=xVals[i],
                y=yVals[i],
                xref="x",
                yref="y",
                sizex=0.1,
                sizey=0.1,
                opacity=0.5,
                layer="below"
            ))
        return fig
        
    
    def get_plot(self):
        #
        positions = self._get_layout()
        
        #
        edges_x, edges_y, edge_text = self._get_edge_traces(pos=positions)
        edge_scatter = go.Scatter(
            x=edges_x,
            y=edges_y,
            mode='lines',
            line={'color':'#FFFDD0'},
            text=edge_text,
            hoverinfo='text'
        ) 
        
        #
        nodes_x, nodes_y, node_texts, node_colors = self._get_node_traces(pos=positions)
        node_scatter = go.Scatter(
            x=nodes_x,
            y=nodes_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(size=12)
        )
        node_scatter.marker.color = node_colors
        node_scatter.text = node_texts

        # Figure plot
        lay = go.Layout(
            title='Jojo graph',
            titlefont_size=16,
            hovermode='closest',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            template='plotly_dark',
            height=800
        )
        fig = go.Figure(
            data=[ edge_scatter, node_scatter],
            layout=lay
        )

        fig = self._add_images(fig=fig)
        
        return fig

    def _get_layout(self, layout='spring'):
        if layout == 'spring':
            return nx.spring_layout(self.graph)
    
    def _get_edge_traces(self, pos):
        """
        doc
        """
        edges_x, edges_y, annot_text = [], [], []

        for edge in self.graph.edges():
            annot_text.append(self.inter_types[edge]) # feature is not working and that's fine
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            edges_x.append(x0)
            edges_x.append(x1)
            edges_x.append(None)
            edges_y.append(y0)
            edges_y.append(y1)
            edges_y.append(None)
        
        return edges_x, edges_y, annot_text
    
    def _get_node_traces(self, pos):
        """
        doc
        """
        nodes_x, nodes_y = [], []
        node_names, node_colors = [], []

        for node in self.graph.nodes():
            x, y = pos[node]
            nodes_x.append(x)
            nodes_y.append(y)
            node_names.append(f'Name: {node}<br>Category: {self.categories[node]}')
            node_colors.append(self.colors[self.categories[node]])
        
        return nodes_x, nodes_y, node_names, node_colors


def get_relations(part_number, config_dict):
    character_file = validate_path(filename=config_dict[part_number]['characters'])
    interaction_file = validate_path(filename=config_dict[part_number]['interactions'])

    interactions_list, interaction_types = parse_interactions(my_file=interaction_file)
    character_categories = parse_characters(my_file=character_file)
    color_dictionary = parse_colors()

    return Relations(interaction_list=interactions_list,
                     interaction_types=interaction_types,
                     character_dict=character_categories,
                     color_dict=color_dictionary)
