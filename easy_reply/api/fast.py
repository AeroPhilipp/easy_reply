import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from easy_reply.interface.main import embed_prompt, merge_prompt_with_favorites, predict_movie
from pathlib import Path
from easy_reply.params import *

app = FastAPI()
#load pickle model

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict(
        prompt: str,
        fav_list,
        weight_n: float,
        weight_fav: float
    ):
    """
    gives a list of n_recom recommendations based on the prompt
    """
    # generate output list

    movie_list = predict_movie(prompt, fav_list.split("_"), float(weight_n), float(weight_fav))
    # load list of titles

    return {"Our recommendation is": movie_list}


@app.get("/")
def root():
    return {"message": "Welcome to the MovieRecommendation API"}

# # Define a root `/` endpoint
# @app.get('/')
# def index():
#     return {'ok': True}
