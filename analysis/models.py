from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from data.load_data import load_data

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
BESTSELLER_THRESHOLD = 0.2


def prepare_data(start_year, end_year, target_col='NA Sales'):
    df = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)].copy()
    df = df[['Genre', 'Publisher', 'Platform', target_col]].dropna()

    encoders = {}
    for col in ['Genre', 'Publisher', 'Platform']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df[['Genre', 'Publisher', 'Platform']]
    y = df[target_col]

    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE), encoders


def create_visualization(ax, data, title, xlabel, ylabel, plot_type='bar', **kwargs):
    if plot_type == 'bar':
        rotation = kwargs.pop('rotation', None)
        sns.barplot(x=data['x'], y=data['y'], ax=ax, **kwargs)

        for i, v in enumerate(data['y']):
            ax.text(i, v, f'{v:.3f}', ha='center', va='bottom')

        if rotation is not None:
            ax.tick_params(axis='x', rotation=rotation)
    elif plot_type == 'heatmap':
        sns.heatmap(data['matrix'], annot=True, fmt='d', cmap='Blues', ax=ax, **kwargs)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def add_metrics_legend(ax, metrics, position=(0.75, 0.98)):
    legend_text = '\n'.join([f'{k}: {v:.3f}' for k, v in metrics.items()])
    ax.text(position[0], position[1], legend_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def train_regression_model(start_year, end_year, ax=None):
    (X_train, X_test, y_train, y_test), _ = prepare_data(start_year, end_year)

    model = RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    importances = model.feature_importances_

    result = {
        'features': ['Genre', 'Publisher', 'Platform'],
        'importances': [round(val, 3) for val in importances],
        'model': model
    }

    if ax is not None:
        create_visualization(
            ax,
            {'x': result['features'], 'y': result['importances']},
            f'Random Forest Regression\nFeature Importances ({start_year}-{end_year})',
            'Feature',
            'Importance',
            color='skyblue' if start_year == 2006 else 'lightgreen',
            rotation=45
        )

        metrics = {
            'R² Score': model.score(X_test, y_test),
            'MSE': ((y_test - model.predict(X_test)) ** 2).mean()
        }
        add_metrics_legend(ax, metrics)

    return result


def prepare_classification_data(start_year, end_year, ax=None):
    (X_train, X_test, y_train, y_test), encoders = prepare_data(start_year, end_year)

    y_train = (y_train > BESTSELLER_THRESHOLD).astype(int)
    y_test = (y_test > BESTSELLER_THRESHOLD).astype(int)

    model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        'accuracy': round(accuracy_score(y_test, y_pred), 3),
        'precision': round(precision_score(y_test, y_pred, zero_division=0), 3),
        'recall': round(recall_score(y_test, y_pred, zero_division=0), 3),
        'f1_score': round(f1_score(y_test, y_pred, zero_division=0), 3)
    }

    if ax is not None:
        conf_matrix = confusion_matrix(y_test, y_pred)
        create_visualization(
            ax,
            {'matrix': conf_matrix},
            f'Random Forest Classification\nConfusion Matrix ({start_year}-{end_year})',
            'Predicted',
            'Actual',
            plot_type='heatmap',
            xticklabels=['Not Best Seller', 'Best Seller'],
            yticklabels=['Not Best Seller', 'Best Seller']
        )
        add_metrics_legend(ax, metrics)

    return model, encoders, metrics


def get_prediction(model, encoders, genre, publisher, platform):
    input_data = {
        'Genre': encoders['Genre'].transform([genre])[0],
        'Publisher': encoders['Publisher'].transform([publisher])[0],
        'Platform': encoders['Platform'].transform([platform])[0]
    }
    return model.predict(pd.DataFrame([input_data]))[0]


def create_model_visualizations():
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Model Analysis Results', fontsize=16, y=0.95)

    train_regression_model(2006, 2011, ax=axes[0, 0])
    train_regression_model(2012, 2016, ax=axes[0, 1])
    prepare_classification_data(2006, 2011, ax=axes[1, 0])
    prepare_classification_data(2012, 2016, ax=axes[1, 1])

    plt.tight_layout()
    plt.savefig('data/model_results.png', dpi=300, bbox_inches='tight')
    plt.close()


data = load_data()
create_model_visualizations()
