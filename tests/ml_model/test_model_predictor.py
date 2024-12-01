import pytest
from src.ml_model.predict import ModelPredictor
from src.processing.preprocessing_data import preprocess_data
from pydantic import ValidationError
from src.api.contracts import InputData, SignatureCounts, Signatures

@pytest.fixture
def model_predictor():
    return ModelPredictor(model_path='src\ml_model\\trained_models\model_stub.cbm')

def test_predictor_valid_data(model_predictor):
    input_data = InputData(
        clientId="123",
        organizationId="456",
        segment="Средний бизнес",
        role="ЕИО",
        organizations=5,
        currentMethod="SMS",
        mobileApp=True,
        signatures=Signatures(
            common=SignatureCounts(mobile=10, web=20),
            special=SignatureCounts(mobile=5, web=15),
        ),
        availableMethods=["SMS", "PayControl"],
        claims=3
    )
    processed_data = preprocess_data(input_data.model_dump(), is_new=True, usecase='setting')

    predicted_method = model_predictor.predict(processed_data)
    assert predicted_method in ["PayControl", "QDSMobile", "QDSToken"]

def test_invalid_data():
    with pytest.raises(ValidationError):
        InputData(
            clientId="123",
            organizationId="456",
            segment="Invalid Segment",
            role="Invalid Role",
            organizations=5,
            currentMethod="Invalid Method",
            mobileApp=True,
            signatures=Signatures(
                common=SignatureCounts(mobile=10, web=20),
                special=SignatureCounts(mobile=5, web=15),
            ),
            availableMethods=["SMS", "PayControl"],
            claims=3
        )

def test_edge_cases(model_predictor):
    edge_data = InputData(
        clientId="123",
        organizationId="456",
        segment="Крупный бизнес",
        role="Сотрудник",
        organizations=0,
        currentMethod="QDSMobile",
        mobileApp=False,
        signatures=Signatures(
            common=SignatureCounts(mobile=0, web=0),
            special=SignatureCounts(mobile=0, web=0),
        ),
        availableMethods=["QDSMobile"],
        claims=0
    )

    processed_data = preprocess_data(edge_data.model_dump(), is_new=False, usecase='basic')
    predicted_method = model_predictor.predict(processed_data)
    assert predicted_method in ["PayControl", "QDSMobile", "QDSToken"]
