import logging

from fastapi import FastAPI, HTTPException, Query
from typing import List
from src.api.contracts import InputData, OutputData
from src.processing.processing import get_processor
from src.processing.preprocessing_data import preprocess_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

processor = get_processor()

@app.post("/predict", response_model=OutputData)
async def make_prediction(data: InputData):
    try:
        data_dict = data.model_dump()
        preprocessed_data = preprocess_data(data_dict)
        prediction = processor.process(preprocessed_data)
        return OutputData(recommendedMethod=prediction)
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
    
@app.post("/predict-with-context", response_model=OutputData)
async def make_prediction_with_context(
    data: InputData,
    is_new: bool,
    usecase: str
):
    try:
        data_dict = data.model_dump()
        preprocessed_data = preprocess_data(data_dict, is_new=is_new, usecase=usecase)
        prediction = processor.process(preprocessed_data)
        return OutputData(recommendedMethod=prediction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Сервис предсказаний работает!"}








