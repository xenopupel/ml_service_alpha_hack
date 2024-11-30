import pandas as pd
from catboost import CatBoostClassifier
import json
import random
import numpy as np
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

path_to_json = "D:\Vscode_projects\Alpha_hack\data\dataset.json"
with open(path_to_json, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# 2. Assign Target Variable
# For demonstration, we'll assign the target variable randomly
possible_outputs = ["PayControl", "QDSToken", "QDSMobile"]
for item in data_list:
    item['model_output'] = random.choice(possible_outputs)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.json_normalize(data_list)

# 3. Feature Engineering

# Handle 'availableMethods' (list of methods)
mlb = MultiLabelBinarizer()
available_methods_encoded = mlb.fit_transform(df['availableMethods'])
available_methods_df = pd.DataFrame(available_methods_encoded, columns=mlb.classes_)

# Remove 'availableMethods' and append the one-hot encoded version
df = df.drop('availableMethods', axis=1)
df = pd.concat([df, available_methods_df], axis=1)

# Encode categorical variables
categorical_cols = ['segment', 'role', 'currentMethod', 'model_output']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Convert boolean 'mobileApp' to integers
df['mobileApp'] = df['mobileApp'].astype(int)

# Rename nested signature columns for clarity
df = df.rename(columns={
    'signatures.common.mobile': 'signatures_common_mobile',
    'signatures.common.web': 'signatures_common_web',
    'signatures.special.mobile': 'signatures_special_mobile',
    'signatures.special.web': 'signatures_special_web'
})

# Remove identifiers that are not useful for prediction
df = df.drop(['clientId', 'organizationId'], axis=1)

# Handle any missing values if present
df = df.fillna(0)

# 4. Train the Model

# Separate features and target
X = df.drop('model_output', axis=1)
y = df['model_output']

# Initialize and train the CatBoostClassifier
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
