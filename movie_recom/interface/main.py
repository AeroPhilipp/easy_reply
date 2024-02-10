import numpy as np
import pandas as pd

from pathlib import Path
from colorama import Fore, Style

from movie_recom.params import *
from movie_recom.ml_logic.encoders import mini_lm_encode, bert_encode
from movie_recom.ml_logic.data import get_data, save_data
from movie_recom.ml_logic.model import fit_n_nearest_neighbors, predict_n_nearest_neighbors
from movie_recom.ml_logic.preprocessor import shorten_synopsis
import requests


def embed_data():
    """
    load the data and shorten the synopsis
    embed the data
    """
    # get the data from data.get_raw_data
    df = get_data("raw_data/mpst_full_data.csv")
    # Process data
    # shorten the synopsis with preprocessor.shorten_synopsis
    df = shorten_synopsis(max_len=500, df=df)
    # embed the synopsis with encoders and saves it
    df_encoded, df_index = mini_lm_encode(df)
    save_data(df_encoded, 'processed_data/data_embedded.csv')
    save_data(df_index, 'processed_data/data_titlenames.csv')


def embed_prompt(prompt: str) -> pd.DataFrame:
    """
    embed the prompt
    """
    #put it into a dataframe
    prompt_df = pd.DataFrame({'title': ['prompt'], 'plot_synopsis': [prompt]})
    #embed the prompt with encoders.mini_lm_encode
    prompt_embedded, df_index = mini_lm_encode(prompt_df)
    return prompt_embedded

def fit_model(n_neighbors: int = 10):
    '''
    fit the model
    '''
    # get the embedded data
    df_embedded = get_data("processed_data/data_embedded.csv")
    # fit the model with model.fit_n_nearest_neighbors
    fit_n_nearest_neighbors(n=n_neighbors, df_embedded=df_embedded)

def predict(prompt: str = 'love story in sweden without happy ending', n_neighbors: int = 5) -> list:
    '''
    get the prompt and recommend movies based on it
    '''
    # get the embedded prompt
    prompt_embedded = embed_prompt(prompt)

    # find the nearest neighbors with model.find_n_nearest_neighbors
    recom_list = predict_n_nearest_neighbors(n_neighbors=n_neighbors, prompt_embedded=prompt_embedded)
    # print(recom_list)
    return recom_list

def call_api():
    url = 'http://localhost:8000/predict'

    params = {
        'prompt': 'Love story in England without happy ending', # 0 for Sunday, 1 for Monday, ...
        'n_recom': 7
    }

    response = requests.get(url, params=params)
    response.json() #=> {wait: 64}
    # print(response.json())

def test():
    pass

if __name__ == '__main__':
    pass
    # test()
