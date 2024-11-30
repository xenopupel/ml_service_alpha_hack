from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Сервис предсказаний работает!"}
    print("Тест корневой ручки прошел успешно.")

def test_predict():
    input_data = {
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
        }
    
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200, f"Статус-код ответа: {response.status_code}"
    output_data = response.json()
    assert 'model_output' in output_data, "В ответе должен быть ключ 'model_output'"
    assert output_data['model_output'] in ["PayControl", "QDSToken", "QDSMobile"], "Неверное значение 'model_output'"
    print("Тест ручки /predict/ прошел успешно.")

if __name__ == "__main__":
    test_root()
    test_predict()
