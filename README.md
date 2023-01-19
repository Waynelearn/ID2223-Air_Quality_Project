# ID2223-Air_Quality_Project

Project description:

The goal of the project is to build a scalable AQI prediction service.

We use both historical weather data and AQI data to predict AQI in Singapore for the next 7 days.

## Hugging Face Spaces URL: 
https://huggingface.co/spaces/WayneLinn/Singapore_Air_Quality_Prediction


## Date Source/ Model

1. Training data from: (updated everyday with daily feature pipeline)

    1. Historical AQI data from webscrpping (1 month)
    1. Historical weather data from VisualCrossing (1 month)
2. Daily data from
    1. AQI from  World Air Quality Index
    1. weather data from VisualCrossing

3. Model: XGBoost
    1. input
    2. output

## Pipeline

1. `Backfill__weather_feature_pipeline.py`: Backfilling with acquired dataset
1. `Backfill_aqi_feature_pipeline.py`

Daily upload new feature
1. `AQI_feature_pipeline_daily.py` : Daily upload new feature
1. `Weather_feature_pipeline_daily.py`

Training
1. `Training_pipeline.py`

Inference
1. `Inference_Pipeline.py`
    1. Will upload predicted AQI to Hopsworks

Others
1. `Weather_API_utility.py`: define functions to get weather data from API

1. `Training_data_transformation.py` : feature engineering (drop unnecessary columns, discard row with NAN)

1. `Drawing.py`: attempts for visualizing prediciton, but discarded






