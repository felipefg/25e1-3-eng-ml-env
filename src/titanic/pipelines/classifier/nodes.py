"""
This is a boilerplate pipeline 'classifier'
generated using Kedro 0.19.11
"""
import pandas as pd
from pycaret.classification import ClassificationExperiment
from sklearn.metrics import log_loss


def prepare_data(raw_data):

    return (
        raw_data
        [
            ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
        ]
        .join(pd.get_dummies(raw_data['Sex'], prefix="Sex"))
        .join(pd.get_dummies(raw_data['Embarked'], prefix='Embarked'))
        .dropna()
        .assign(Survived=lambda x: x['Survived'].astype(bool))
    )


def best_model_from_comparison(data, session_id):

    exp = ClassificationExperiment()
    exp.setup(data=data, target='Survived', session_id=session_id)

    best_model = exp.compare_models()

    tuned_model = exp.tune_model(best_model, n_iter=10, optimize='AUC')

    return tuned_model


def logistic_regression_model(data, session_id):

    exp = ClassificationExperiment()
    exp.setup(data=data, target='Survived', session_id=session_id)

    model = exp.create_model('lr')

    tuned_model = exp.tune_model(model, n_iter=10, optimize='AUC')

    return tuned_model


def plot_roc(data, model, session_id, output_filename):

    exp = ClassificationExperiment()
    exp.setup(data=data, target='Survived', session_id=session_id)

    exp.plot_model(model, plot='auc', save=output_filename)


def get_metrics(data, model):

    new_data = data.drop(columns=['Survived'])

    y_data = model.predict_proba(new_data)

    metrics_dict = {
        "log_loss": log_loss(data['Survived'].values, y_data[:, 1])
    }

    return {
        key: {'value': val, 'step': 1}
        for key, val in metrics_dict.items()
    }
