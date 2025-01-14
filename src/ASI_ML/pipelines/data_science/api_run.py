import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
from autogluon.tabular import TabularPredictor

class WeatherInput(BaseModel):
    datetime: str
    temperature: float
    humidity: float
    wind_speed: float
    general_diffuse_flows: float
    diffuse_flows: float
    target_zone: Optional[int] = None  # Zone to predict; 1, 2, or 3


def api_run(best_models: Dict[str, TabularPredictor]):
    if not best_models or not all(isinstance(model, TabularPredictor) for model in best_models.values()):
        raise ValueError("Invalid or missing models for the API.")

    app = FastAPI()

    @app.get("/", tags=["intro"])
    async def index():
        return {"message": "Welcome to the Weather Prediction API"}

    @app.post("/predict", tags=["prediction"], status_code=200)
    async def get_predictions(input_data: WeatherInput):
        # Prepare data for prediction
        X_new = pd.DataFrame([{
            "Datetime": input_data.datetime,
            "Temperature": input_data.temperature,
            "Humidity": input_data.humidity,
            "WindSpeed": input_data.wind_speed,
            "GeneralDiffuseFlows": input_data.general_diffuse_flows,
            "DiffuseFlows": input_data.diffuse_flows
        }])

        # Preprocess Datetime if necessary
        # X_new["Datetime"] = pd.to_datetime(X_new["Datetime"])
        # X_new["Hour"] = X_new["Datetime"].dt.hour
        # X_new["DayOfWeek"] = X_new["Datetime"].dt.dayofweek

        # Predict for the specified zone or all zones
        if input_data.target_zone:
            zone_key = f"PowerConsumption_Zone{input_data.target_zone}"

            if zone_key not in best_models:
                raise HTTPException(status_code=404, detail=f"Model for {zone_key} not found.")
            prediction = best_models[zone_key].predict(X_new)
            return {"zone": input_data.target_zone, "prediction": prediction.tolist()}
        else:
            predictions = {
                zone: model.predict(X_new).tolist()
                for zone, model in best_models.items()
            }
            return {"predictions": predictions}

    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
