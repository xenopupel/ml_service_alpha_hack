import pytest
from fastapi.testclient import TestClient
from src.api.app import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Сервис предсказаний работает!"}

@pytest.mark.parametrize(
    "endpoint, input_data, params, expected_status, allowed_methods",
    [
        (
            "/predict/",
            {
                "clientId": "client123",
                "organizationId": "org456",
                "segment": "Малый бизнес",
                "role": "ЕИО",
                "organizations": 1,
                "currentMethod": "SMS",
                "mobileApp": True,
                "signatures": {
                    "common": {
                        "mobile": 10,
                        "web": 5
                    },
                    "special": {
                        "mobile": 2,
                        "web": 1
                    }
                },
                "availableMethods": ["SMS", "QDSToken"],
                "claims": 0
            },
            None,
            200,
            ["PayControl", "QDSToken", "QDSMobile", "NoRecommendedMethod"]
        ),
        (
            "/predict-with-context/",
            {
                "clientId": "client789",
                "organizationId": "org789",
                "segment": "Средний бизнес",
                "role": "Сотрудник",
                "organizations": 2,
                "currentMethod": "PayControl",
                "mobileApp": False,
                "signatures": {
                    "common": {
                        "mobile": 5,
                        "web": 15
                    },
                    "special": {
                        "mobile": 2,
                        "web": 5
                    }
                },
                "availableMethods": ["SMS", "PayControl"],
                "claims": 2
            },
            {"is_new": False, "usecase": "big_money"},
            200,
            ["PayControl", "QDSToken", "QDSMobile", "NoRecommendedMethod"]
        ),
    ],
    ids=["TestPredict", "TestPredictWithContext"]
)
def test_predict_endpoints(client, endpoint, input_data, params, expected_status, allowed_methods):
    if params:
        response = client.post(endpoint, json=input_data, params=params)
    else:
        response = client.post(endpoint, json=input_data)
    assert response.status_code == expected_status
    output_data = response.json()
    assert 'recommendedMethod' in output_data
    assert output_data['recommendedMethod'] in allowed_methods