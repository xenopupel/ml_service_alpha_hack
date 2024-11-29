from catboost import CatBoostClassifier
from sklearn.datasets import make_classification
import pandas as pd

# Генерация случайных данных
# 1000 строк, 10 признаков, 2 класса
X, y = make_classification(
    n_samples=1000,     # Количество строк
    n_features=10,      # Количество признаков
    n_informative=5,    # Количество информативных признаков
    n_redundant=0,      # Количество избыточных признаков
    n_classes=2,        # Количество классов
    random_state=42     # Для повторяемости
)

data = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
data['target'] = y

X = data.drop('target', axis=1)
y = data['target']

model = CatBoostClassifier(iterations=100, depth=6, learning_rate=0.1, verbose=10)
model.fit(X, y)

model.save_model('src\ml_model\\trained_models\model_stub.cbm')

print("fake model succesfully trained as 'model_stub.cbm'.")
