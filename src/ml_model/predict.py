import pandas as pd
from catboost import CatBoostClassifier

class ModelPredictor:
    def __init__(self, model_path: str):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        print(f"Модель загружена из {model_path}")
    
    def predict(self, data: pd.DataFrame) -> pd.Series:
        predictions = self.model.predict(data)
        return pd.Series(predictions)


if __name__ == "__main__":
    predictor = ModelPredictor('src/ml_model/trained_models/model_stub.cbm')

    # Пример данных
    example_data = pd.DataFrame({
        'feature_0': [0.5, -1.2],
        'feature_1': [1.3, 0.7],
        'feature_2': [-0.8, 0.5],
        'feature_3': [1.5, -0.2],
        'feature_4': [0.1, 0.9],
        'feature_5': [0.4, -0.5],
        'feature_6': [0.7, -1.1],
        'feature_7': [1.0, 0.3],
        'feature_8': [-0.3, 0.8],
        'feature_9': [0.6, 0.4]
    })

    predictions = predictor.predict(example_data)
    print("Предсказания:", predictions.tolist())
