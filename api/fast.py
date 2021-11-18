from typing import get_args
from TaxiFareModel.params import PATH_TO_LOCAL_MODEL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def index():
    return {"greeting": "Hello world"}



@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):

    # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime(
        "%Y-%m-%d %H:%M:%S UTC")
    key = '2013-07-06 17:18:00'
    key = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
    formatted_key= key.strftime("%Y-%m-%d %H:%M:%S UTC")

    X_pred = pd.DataFrame({
        'key' : [formatted_key],
        "pickup_datetime": [formatted_pickup_datetime],
        'pickup_longitude': [float(pickup_longitude)],
        'pickup_latitude': [float(pickup_latitude)],
        'dropoff_longitude': [float(dropoff_longitude)],
        'dropoff_latitude': [float(dropoff_latitude)],
        'passenger_count': [int(passenger_count)]
    })

    X_pred = X_pred[[
        'key', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude',
        'dropoff_longitude', 'dropoff_latitude', 'passenger_count'
    ]]

    model = joblib.load('model.joblib')
    prediction = model.predict(X_pred)

    return {'prediction': f'{prediction[0]}'}
