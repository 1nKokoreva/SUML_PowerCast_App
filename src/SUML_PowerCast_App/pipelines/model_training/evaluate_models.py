"""
Module that provides functions for evaluating trained models using common regression metrics.
"""

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_models(predictors, x_test, y_test, _parameters):
    """
    Evaluate a set of predictors on the given test data, save their performance, and return the results.

    Args:
        predictors (dict): A dictionary where keys are target columns and values are trained model objects.
        x_test (pd.DataFrame): Feature data for testing.
        y_test (pd.DataFrame): True target data for testing.
        _parameters (dict): Additional parameters for evaluation (currently unused).

    Returns:
        tuple: A tuple containing:
            - results_df (pd.DataFrame): DataFrame with MAE, MSE, and R2 metrics for each target.
            - predictors (dict): The same dictionary of predictors, possibly updated.
    """

    results = {}
    best_models = {}  # Dictionary to store the best models for each target zone

    for target_column, predictor in predictors.items():
        print(f"\n{'='*20} Evaluating AutoGluon model for target: {target_column} {'='*20}\n")

        predictions = predictor.predict(x_test)
        true_values = y_test[target_column]

        mae = mean_absolute_error(true_values, predictions)
        mse = mean_squared_error(true_values, predictions)
        r2_value = r2_score(true_values, predictions)

        results[target_column] = {
            'MAE': mae,
            'MSE': mse,
            'R2': r2_value
        }

        print(f"  MAE: {mae:.2f}")
        print(f"  MSE: {mse:.2f}")
        print(f"  R2: {r2_value:.2f}")

        # Save the model for the current target column
        model_path = f"data/06_models/{target_column}_model.pkl"
        predictor.save(model_path)
        print(f"\nModel for {target_column} saved to {model_path}")

        # Store the model in the dictionary
        best_models[target_column] = predictor

    # Create a DataFrame with evaluation metrics
    results_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
    results_df.rename(columns={'index': 'Target'}, inplace=True)

    print("\nFinal Evaluation Results:\n")
    print(results_df)

    return results_df, predictors
