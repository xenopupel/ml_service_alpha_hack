import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder

class ModelPredictor:
    def __init__(self, model_path: str):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.label_encoders = self._initialize_label_encoders()

    def _initialize_label_encoders(self):
        label_encoders = {}
        label_encoders['usecase'] = LabelEncoder()
        label_encoders['usecase'].fit(['base_operation_signature', 'big_operation_signature', 'change_signature_method'])
        label_encoders['segment'] = LabelEncoder()
        label_encoders['segment'].fit(["Малый бизнес", "Средний бизнес", "Крупный бизнес"])
        label_encoders['role'] = LabelEncoder()
        label_encoders['role'].fit(['ЕИО', 'Сотрудник'])
        label_encoders['currentMethod'] = LabelEncoder()
        label_encoders['currentMethod'].fit(["SMS", "PayControl", "QDSToken", "QDSMobile"])
        label_encoders['target'] = LabelEncoder()
        label_encoders['target'].fit(['PayControl', 'QDSMobile', 'QDSToken'])
        return label_encoders

    def predict(self, data: dict) -> str:
        features = self._extract_features(data)
        data_df = pd.DataFrame([features])
        prediction = self.model.predict(data_df)
        prediction_label = self.label_encoders['target'].inverse_transform([int(prediction[0])])[0]
        return prediction_label

    def _extract_features(self, data: dict) -> dict:
        features = {}
        features['usecase'] = self.label_encoders['usecase'].transform([data['usecase']])[0]
        features['segment'] = self.label_encoders['segment'].transform([data['segment']])[0]
        features['role'] = self.label_encoders['role'].transform([data['role']])[0]
        features['currentMethod'] = self.label_encoders['currentMethod'].transform([data['currentMethod']])[0]
        features['mobileApp'] = int(data['mobileApp'])
        features['organizations'] = data['organizations']
        features['common_mobile'] = data['signatures']['common']['mobile']
        features['common_web'] = data['signatures']['common']['web']
        features['special_mobile'] = data['signatures']['special']['mobile']
        features['special_web'] = data['signatures']['special']['web']
        return features
