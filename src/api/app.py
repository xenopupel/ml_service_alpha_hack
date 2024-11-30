import logging

from fastapi import FastAPI, HTTPException

from src.ml_model.predict import ModelPredictor
from src.api.contracts import InputData, OutputData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

predictor = ModelPredictor('src/ml_model/trained_models/model_stub.cbm')

@app.post("/predict/", response_model=OutputData)
async def make_prediction(data: InputData):
    try:
        data_dict = data.model_dump()
        prediction = predictor.predict(data_dict)
        return OutputData(model_output=prediction)
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Сервис предсказаний работает!"}








