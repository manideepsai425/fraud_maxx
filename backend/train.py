import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
import pickle
import os

base_dir = os.path.dirname(__file__)
dataset_path = os.path.join(base_dir, '..', 'dataset', 'Fraud.csv')
data = pd.read_csv(dataset_path)

# Handle missing values
data.fillna(data.mean(numeric_only=True), inplace=True)
data.fillna(data.mode().iloc[0], inplace=True)

# Drop ID columns (not useful for prediction)
X = data.drop(['Transaction_ID', 'User_ID', 'Fraudulent'], axis=1)
y = data['Fraudulent']

# Encode categorical columns
categorical_cols = ['Transaction_Type', 'Device_Used', 'Location', 'Payment_Method']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Scale numerical features
scaler = StandardScaler()
numerical_cols = ['Transaction_Amount', 'Time_of_Transaction', 'Previous_Fraudulent_Transactions', 
                  'Account_Age', 'Number_of_Transactions_Last_24H']
X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train model
model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Save model and preprocessors
model_path = os.path.join(base_dir, 'model.pkl')
scaler_path = os.path.join(base_dir, 'scaler.pkl')
encoders_path = os.path.join(base_dir, 'label_encoders.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

with open(encoders_path, 'wb') as f:
    pickle.dump(label_encoders, f)

print(f"Model saved to {model_path}")
print(f"Scaler saved to {scaler_path}")
print(f"Label encoders saved to {encoders_path}")
print(f"Feature columns: {X.columns.tolist()}")