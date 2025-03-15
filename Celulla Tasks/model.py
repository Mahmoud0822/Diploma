import pandas as pd
data = pd.read_csv(r"C:\Users\mahmo\Downloads\first inten project.csv")
from sklearn.model_selection import train_test_split
X = data.drop('booking status', axis=1)
y = data['booking status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)

import joblib


joblib.dump(model, 'hotel_booking_model.pkl')


joblib.dump(X_test.columns.tolist(), 'model_columns.pkl')