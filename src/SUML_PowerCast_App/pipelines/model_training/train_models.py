import pandas as pd
from autogluon.tabular import TabularPredictor

def train_models(X_train, Y_train, X_dev, Y_dev, parameters):

    print("Parameters received:", parameters)

    if 'autogluon' not in parameters or 'model_path' not in parameters['autogluon']:
        raise ValueError("The 'model_path' key is missing in the 'autogluon' section of parameters.")

    model_path_base = parameters['autogluon']['model_path']

    predictors = {}

    for target_column in Y_train.columns:
        print(f"\nTraining AutoGluon for target: {target_column}")

        train_data = pd.concat([X_train, Y_train[target_column]], axis=1)
        dev_data = pd.concat([X_dev, Y_dev[target_column]], axis=1)

        predictor = TabularPredictor(
            label=target_column,
            eval_metric=parameters['autogluon'].get('eval_metric', 'mean_absolute_error')
        ).fit(
            train_data=train_data,
            time_limit=parameters['autogluon'].get('time_limit', 3600)
        )

        performance = predictor.evaluate(dev_data)
        print(f"Performance for {target_column}: {performance}")

        model_path = f"{model_path_base}/{target_column}"
        predictor.save(model_path)
        print(f"AutoGluon model for {target_column} saved at {model_path}")

        predictors[target_column] = predictor

    return predictors
