from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd

from data.load_data import load_data

data = load_data()


def prepare_regression_data(start_year, end_year):
    df = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)].copy()
    df = df[['Genre', 'Publisher', 'Platform', 'NA Sales']].dropna()

    for col in ['Genre', 'Publisher', 'Platform']:
        df[col] = LabelEncoder().fit_transform(df[col])

    X = df[['Genre', 'Publisher', 'Platform']]
    y = df['NA Sales']
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_regression_model(start_year, end_year):
    X_train, X_test, y_train, y_test = prepare_regression_data(start_year, end_year)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    importances = model.feature_importances_
    return {
        'features': ['Genre', 'Publisher', 'Platform'],
        'importances': [round(val, 3) for val in importances]
    }


def prepare_classification_data(start_year, end_year):
    df = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)].copy()
    df = df[['Genre', 'Publisher', 'Platform', 'NA Sales']].dropna()
    df['BestSeller'] = (df['NA Sales'] > 0.2).astype(int)

    encoders = {}
    for col in ['Genre', 'Publisher', 'Platform']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df[['Genre', 'Publisher', 'Platform']]
    y = df['BestSeller']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        'accuracy': round(accuracy_score(y_test, y_pred), 3),
        'precision': round(precision_score(y_test, y_pred, zero_division=0), 3),
        'recall': round(recall_score(y_test, y_pred, zero_division=0), 3),
        'f1_score': round(f1_score(y_test, y_pred, zero_division=0), 3),
        'conf_matrix': confusion_matrix(y_test, y_pred).tolist()
    }

    return model, encoders, metrics


def get_prediction(model, encoders, genre, publisher, platform):
    input_data = {
        'Genre': encoders['Genre'].transform([genre])[0],
        'Publisher': encoders['Publisher'].transform([publisher])[0],
        'Platform': encoders['Platform'].transform([platform])[0]
    }
    df_input = pd.DataFrame([input_data])
    return model.predict(df_input)[0]
