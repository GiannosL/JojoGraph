import pandas as pd
from pathlib import Path
import os


def validate_path(filename):
    """
    doc
    """
    my_file = Path(filename)

    if my_file.exists():
        return my_file
    else:
        raise FileNotFoundError(f'File not found in path: {my_file}')


def parse_interactions(my_file):
    """
    doc
    """
    df = pd.read_csv(my_file, sep=';')
    char_a = df['Character-A'].tolist()
    char_b = df['Character-B'].tolist()
    interaction_types = df['Interaction-type'].tolist()

    #
    interaction_list = []
    int_type_dict = {}
    for i, a in enumerate(char_a):
        interaction_list.append((a, char_b[i]))
        int_type_dict[(a, char_b[i])] = interaction_types[i]
        int_type_dict[(char_b[i], a)] = interaction_types[i]
    
    return interaction_list, int_type_dict


def parse_characters(my_file):
    """
    doc
    """
    df = pd.read_csv(my_file, sep=';')
    characters = df['Name'].tolist()
    categories = df['Category'].tolist()

    #
    character_dict = {}
    for i, char in enumerate(characters):
        character_dict[char] = categories[i]

    return character_dict


def parse_colors(my_file='data/colors/color_map.csv'):
    """
    doc
    """
    df = pd.read_csv(my_file, sep=';')
    colors = df['Color'].tolist()
    categories = df['Category'].tolist()
    my_dict = {}
    for i in range(len(colors)):
        my_dict[categories[i]] = colors[i]
    
    return my_dict

def get_image_names() -> list:
    images=os.listdir('data/node-images/')
    character_images_names=[x.split('.jpeg')[0] for x in images]
    return character_images_names

