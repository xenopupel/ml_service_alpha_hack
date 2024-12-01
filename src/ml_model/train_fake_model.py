import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder

path_to_df_csv = "D:\Vscode_projects\Alpha_hack\data\dataset_updated_noway.csv"
df = pd.read_csv(path_to_df_csv, sep=';')

# Feature Engineering

categorical_cols = ['usecase', 'segment', 'role', 'currentMethod', 'target']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

df['mobileApp'] = df['mobileApp'].astype(int)
df = df.fillna(0)

# Train the Model
X = df.drop('target', axis=1)
y = df['target']

model = CatBoostClassifier(
    iterations=100,
    depth=6,
    learning_rate=0.1,
    verbose=False,
    random_state=42
)
model.fit(X, y)

model.save_model('src/ml_model/trained_models/model_stub.cbm')

print("Model successfully trained and saved as 'model_stub.cbm'.")
