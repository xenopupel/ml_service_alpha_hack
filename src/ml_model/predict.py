import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import numpy as np

class ModelPredictor:
    def __init__(self, model_path: str):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.label_encoders = self._initialize_label_encoders()
        self.mlb = self._initialize_mlb()

    def _initialize_label_encoders(self):
        label_encoders = {}
        label_encoders['segment'] = LabelEncoder()
        label_encoders['segment'].fit(["Малый бизнес", "Средний бизнес", "Крупный бизнес"])
        label_encoders['role'] = LabelEncoder()
        label_encoders['role'].fit(['ЕИО', 'Сотрудник'])
        label_encoders['currentMethod'] = LabelEncoder()
        label_encoders['currentMethod'].fit(["SMS", "PayControl", "QDSToken", "QDSMobile"])
        label_encoders['model_output'] = LabelEncoder()
        label_encoders['model_output'].fit(['PayControl', 'QDSMobile', 'QDSToken'])
        return label_encoders

    def _initialize_mlb(self):
        mlb = MultiLabelBinarizer(classes=["SMS", "PayControl", "QDSToken", "QDSMobile"])
        mlb.fit([['SMS'], ['PayControl'], ['QDSToken'], ['QDSMobile']])
        return mlb

    def predict(self, data: dict) -> str:
        features = self._extract_features(data)
        data_df = pd.DataFrame([features])
        prediction = self.model.predict(data_df)
        prediction_label = self.label_encoders['model_output'].inverse_transform([int(prediction[0])])[0]
        return prediction_label

    def _extract_features(self, data: dict) -> dict:
        features = {}
        # Encode 'segment', 'role', 'currentMethod'
        features['segment'] = self.label_encoders['segment'].transform([data['segment']])[0]
        features['role'] = self.label_encoders['role'].transform([data['role']])[0]
        features['currentMethod'] = self.label_encoders['currentMethod'].transform([data['currentMethod']])[0]
        # Convert 'mobileApp' to int
        features['mobileApp'] = int(data['mobileApp'])
        # Flatten 'signatures' fields
        features['signatures_common_mobile'] = data['signatures']['common']['mobile']
        features['signatures_common_web'] = data['signatures']['common']['web']
        features['signatures_special_mobile'] = data['signatures']['special']['mobile']
        features['signatures_special_web'] = data['signatures']['special']['web']
        # Numeric fields
        features['organizations'] = data['organizations']
        features['claims'] = data['claims']
        # One-hot encode 'availableMethods'
        available_methods = data['availableMethods']
        available_methods_encoded = self.mlb.transform([available_methods])[0]
        for idx, method in enumerate(self.mlb.classes_):
            features[method] = available_methods_encoded[idx]
        return features
