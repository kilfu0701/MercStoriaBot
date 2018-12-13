import os
import pandas as pd

CharactersFile = './data/characters.csv'

class DataContainer(object):

    def __init__(self):
        self.characters = pd.read_csv(os.path.abspath(CharactersFile))

