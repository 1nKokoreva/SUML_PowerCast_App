"""
This module provides FastAPI endpoints and a function to launch the API in a separate process.
It also includes utilities for formatting datetimes, handling CSV/database operations, and
managing predictions from trained AutoGluon models.
"""

import os
from datetime import datetime
from multiprocessing import Process

import pandas as pd
import pymysql
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from autogluon.tabular import TabularPredictor
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

# Remove unused or unneeded imports:
# from kedro.framework.context import KedroContext
# from kedro.framework.hooks import _create_hook_manager
# from kedro.config import OmegaConfigLoader

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "PCP",
    "charset": "utf8mb4",
}


class WeatherInput(BaseModel):
    """
    Represents the expected input data format for weather-based power consumption predictions.
    """
    datetime: str
    temperature: float
    humidity: float
    wind_speed: float
    general_diffuse_flows: float
    diffuse_flows: float
    target_zones: Optional[List[int]] = None  # Zone to predict; e.g., 1, 2, or 3


def format_datetime_for_file(input_datetime: str) -> str:
    """
    Convert datetime from 'YYYY-MM-DD HH:MM:SS' format to 'MM/DD/YYYY HH:MM' format.

    Args:
        input_datetime (str): A date-time string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        str: A reformatted date-time string in the format 'MM/DD/YYYY HH:MM'.

    Raises:
        HTTPException: If the provided date-time string cannot be parsed.
    """
    try:
        parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
        return parsed_datetime.strftime("%m/%d/%Y %H:%M")
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=f"Invalid datetime format: {str(exc)}"
        ) from exc


def append_to_csv(file_path: str, data: Dict) -> None:
    """
    Append data to a CSV file, creating the file with headers if it doesn't exist.

    Args:
        file_path (str): Path to the CSV file.
        data (Dict): A dictionary of data to append as a single row.

    Raises:
        HTTPException: If any file I/O operation fails.
    """
    dataframe = pd.DataFrame([data])
    try:
        if not os.path.exists(file_path):
            dataframe.to_csv(file_path, mode='w', index=False, header=True)
        else:
            dataframe.to_csv(file_path, mode='a', index=False, header=False)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"File operation error: {str(exc)}"
        ) from exc


def insert_into_database(data: Dict) -> None:
    """
    Insert prediction data into the database using PyMySQL.

    Args:
        data (Dict): A dictionary containing the columns to be inserted.

    Raises:
        HTTPException: If a database error occurs.
    """
    query = """
        INSERT INTO powerconsumption (
            Datetime, Temperature, Humidity, WindSpeed, GeneralDiffuseFlows, DiffuseFlows,
            PowerConsumption_Zone1, PowerConsumption_Zone2, PowerConsumption_Zone3
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["Datetime"],
        data["Temperature"],
        data["Humidity"],
        data["WindSpeed"],
        data["GeneralDiffuseFlows"],
        data["DiffuseFlows"],
        data["PowerConsumption_Zone1"],
        data["PowerConsumption_Zone2"],
        data["PowerConsumption_Zone3"]
    )

    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        connection.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}") from exc
    finally:
        connection.close()


def get_predictions(
    input_data: WeatherInput,
    best_models: Dict[str, TabularPredictor]
) -> Dict[str, List[float]]:
    """
    Generate predictions for the specified zones (or all zones) using trained models.

    Args:
        input_data (WeatherInput): The input data structure with weather info.
        best_models (Dict[str, TabularPredictor]): A dictionary of trained models keyed by zone name.

    Returns:
        Dict[str, List[float]]: A dictionary with zone keys and lists of predicted values.
    """
    # Prepare data for prediction
    x_new = pd.DataFrame([{
        "Datetime": input_data.datetime,
        "Temperature": input_data.temperature,
        "Humidity": input_data.humidity,
        "WindSpeed": input_data.wind_speed,
        "GeneralDiffuseFlows": input_data.general_diffuse_flows,
        "DiffuseFlows": input_data.diffuse_flows
    }])

    # Predict for all zones
    all_predictions = {
        zone: model.predict(x_new).tolist()
        for zone, model in best_models.items()
    }

    # Filter predictions if certain target zones are specified
    if input_data.target_zones:
        filtered_predictions = {}
        for zone in input_data.target_zones:
            zone_key = f"PowerConsumption_Zone{zone}"
            if zone_key not in best_models:
                raise HTTPException(
                    status_code=404,
                    detail=f"Model for {zone_key} not found."
                )
            filtered_predictions[zone_key] = all_predictions[zone_key]
        predictions = filtered_predictions
    else:
        predictions = all_predictions

    # Insert the prediction data into the database or CSV
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
    # insert_into_database(data_to_insert)

    return {"predictions": predictions}


def start_api(best_models: Dict[str, TabularPredictor]) -> None:
    """
    Start the FastAPI server, providing endpoints for predictions and pipeline updates.
    This function is intended to run in a separate process.

    Args:
        best_models (Dict[str, TabularPredictor]): Dictionary of trained models by zone key.
    """
    if not best_models or not all(isinstance(model, TabularPredictor) for model in best_models.values()):
        raise ValueError("Invalid or missing models for the API.")

    app = FastAPI()

    @app.get("/", tags=["intro"])
    async def index():
        return {"message": "Welcome to the Weather Prediction API"}

    @app.post("/predict", tags=["prediction"], status_code=200)
    async def predict_endpoint(input_data: WeatherInput):
        """
        Receive weather information and return power consumption predictions.
        """
        return get_predictions(input_data, best_models)

    @app.get("/update", tags=["update"], status_code=200)
    async def update_model():
        """
        Rerun the 'model_training' pipeline to update the trained models on-the-fly.
        """
        bootstrap_project(".")
        try:
            with KedroSession.create(project_path=".") as session:
                session.run(pipeline_name="model_training")
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Pipeline execution failed: {str(exc)}"
            ) from exc
        return {"message": "Pipeline executed successfully."}

    uvicorn.run(app, host="0.0.0.0", port=8000)


def api_run(best_models: Dict[str, TabularPredictor]) -> Process:
    """
    Launch the API in a separate process.

    Args:
        best_models (Dict[str, TabularPredictor]): Dictionary of trained models.

    Returns:
        Process: The process running the FastAPI server.
    """
    print("Loaded `best_models`:", best_models)
    process = Process(target=start_api, args=(best_models,))
    process.start()
    print("API is running in a separate process...")
    return process
