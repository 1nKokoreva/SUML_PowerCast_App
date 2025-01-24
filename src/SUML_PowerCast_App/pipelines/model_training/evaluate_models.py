import pandas as pd
import wandb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_models(predictors, X_test, Y_test, parameters):
    wandb.init(
        project=parameters['wandb']['project'],
        entity=parameters['wandb']['entity'],
        name='evaluate_models'
    )

    results = {}
    best_models = {}  # Dictionary to store the best models for each target zone

    for target_column, predictor in predictors.items():
        print(f"\n{'='*20} Evaluating AutoGluon model for target: {target_column} {'='*20}\n")

        predictions = predictor.predict(X_test)

        y_true = Y_test[target_column]

        mae = mean_absolute_error(y_true, predictions)
        mse = mean_squared_error(y_true, predictions)
        r2 = r2_score(y_true, predictions)

        results[target_column] = {
            'MAE': mae,
            'MSE': mse,
            'R2': r2
        }

        wandb.log({
            f"{target_column}/MAE": mae,
            f"{target_column}/MSE": mse,
            f"{target_column}/R2": r2
        })

        print(f"  MAE: {mae:.2f}")
        print(f"  MSE: {mse:.2f}")
        print(f"  R2: {r2:.2f}")

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

    wandb.log({"evaluation_results": wandb.Table(dataframe=results_df)})

    wandb.finish()

    return results_df, predictors
