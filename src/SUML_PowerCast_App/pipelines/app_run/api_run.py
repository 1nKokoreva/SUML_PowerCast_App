import pandas as pd
import os
from kedro.framework.context import KedroContext
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from autogluon.tabular import TabularPredictor
from multiprocessing import Process
from datetime import datetime
import pymysql
import uvicorn
from kedro.framework.hooks import _create_hook_manager
from kedro.config import OmegaConfigLoader
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "PCP",
    "charset": "utf8mb4",
}

class WeatherInput(BaseModel):
    datetime: str
    temperature: float
    humidity: float
    wind_speed: float
    general_diffuse_flows: float
    diffuse_flows: float
    target_zones: Optional[List[int]] = None  # Zone to predict; 1, 2, or 3

def format_datetime_for_file(input_datetime: str) -> str:
    """
    Converts datetime from `YYYY-MM-DD HH:MM:SS` format to `MM/DD/YYYY HH:MM` format.
    """
    try:
        # Parse the input datetime string
        parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
        # Format to desired output
        return parsed_datetime.strftime("%m/%d/%Y %H:%M")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid datetime format: {str(e)}")


def append_to_csv(file_path, data):
    """
    Appends data to a CSV file, creating it if it doesn't exist.
    """
    df = pd.DataFrame([data])  # Convert single record to DataFrame
    try:
        if not os.path.exists(file_path):
            # Create the file with headers if it doesn't exist
            df.to_csv(file_path, mode='w', index=False, header=True)
        else:
            # Append without headers if the file exists
            df.to_csv(file_path, mode='a', index=False, header=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File operation error: {str(e)}")


def insert_into_database(data):
        """
        Inserts prediction data into the database using pymysql.
        """
        query = """
        INSERT INTO powerconsumption (
            Datetime, Temperature, Humidity, WindSpeed, GeneralDiffuseFlows, DiffuseFlows, 
            PowerConsumption_Zone1, PowerConsumption_Zone2, PowerConsumption_Zone3
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["Datetime"], data["Temperature"], data["Humidity"], data["WindSpeed"],
            data["GeneralDiffuseFlows"], data["DiffuseFlows"],
            data["PowerConsumption_Zone1"], data["PowerConsumption_Zone2"], data["PowerConsumption_Zone3"]
        )

        try:
            connection = pymysql.connect(**DB_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            connection.close()

def getPredictions(input_data: WeatherInput, best_models: Dict[str, TabularPredictor]):
    # Prepare data for prediction
    X_new = pd.DataFrame([{
        "Datetime": input_data.datetime,
        "Temperature": input_data.temperature,
        "Humidity": input_data.humidity,
        "WindSpeed": input_data.wind_speed,
        "GeneralDiffuseFlows": input_data.general_diffuse_flows,
        "DiffuseFlows": input_data.diffuse_flows
    }])

    # Predict for the specified zone or all zones
    all_predictions = {
        zone: model.predict(X_new).tolist()
        for zone, model in best_models.items()
    }

    if input_data.target_zones:
        filtered_predictions = {}
        for zone in input_data.target_zones:
            zone_key = f"PowerConsumption_Zone{zone}"
            if zone_key not in best_models:
                raise HTTPException(status_code=404, detail=f"Model for {zone_key} not found.")
            filtered_predictions[zone_key] = all_predictions[zone_key]
        predictions = filtered_predictions
    else:
        # If no target_zones specified, predict for all zones
        predictions = all_predictions

    # Insert the prediction data into the database
    data_to_insert = {
        "Datetime": input_data.datetime,
        "Temperature": input_data.temperature,
        "Humidity": input_data.humidity,
        "WindSpeed": input_data.wind_speed,
        "GeneralDiffuseFlows": input_data.general_diffuse_flows,
        "DiffuseFlows": input_data.diffuse_flows,
        "PowerConsumption_Zone1": all_predictions.get("PowerConsumption_Zone1", [None])[0],
        "PowerConsumption_Zone2": all_predictions.get("PowerConsumption_Zone2", [None])[0],
        "PowerConsumption_Zone3": all_predictions.get("PowerConsumption_Zone3", [None])[0],
    }


    append_to_csv("data/01_raw/powerconsumption.csv", data_to_insert)
    #insert_into_database(data_to_insert)

    return {"predictions": predictions}

def start_api(best_models: Dict[str, TabularPredictor]):
    """
    Starts the FastAPI server. This function is meant to be run in a separate process.
    """
    if not best_models or not all(isinstance(model, TabularPredictor) for model in best_models.values()):
        raise ValueError("Invalid or missing models for the API.")
    
    app = FastAPI()

    @app.get("/", tags=["intro"])
    async def index():
        return {"message": "Welcome to the Weather Prediction API"}

    @app.post("/predict", tags=["prediction"], status_code=200)
    async def get_predictions(input_data: WeatherInput):
        return getPredictions(input_data, best_models)
        
    @app.get("/update", tags=["update"], status_code=200)
    async def update_model():
        bootstrap_project(".")
        
        try:
            with KedroSession.create(project_path=".") as session:
                session.run(pipeline_name="model_training")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")
        
        return {"message": "Pipeline executed successfully."}


    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)

def api_run(best_models: Dict[str, TabularPredictor]):
    print("Loaded `best_models`:", best_models)
    process = Process(target=start_api, args=(best_models,))
    process.start()
    print("API is running in a separate process...")
    return process