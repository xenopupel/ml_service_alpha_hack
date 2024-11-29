from fastapi import FastAPI
import pandas as pd

from ml_model.predict import ModelPredictor

app = FastAPI()

# Инициализация модели при старте приложения
predictor = ModelPredictor('src/ml_model/trained_models/model_stub.cbm')

@app.post("/predict/")
async def make_prediction(data: list):
    df = pd.DataFrame(data)
    predictions = predictor.predict(df)
    return {"predictions": predictions.tolist()}
