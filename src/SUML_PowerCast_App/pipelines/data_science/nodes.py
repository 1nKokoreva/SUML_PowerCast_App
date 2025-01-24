# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import wandb
# from sklearn.model_selection import RandomizedSearchCV, train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# def perform_analysis(data):
#     # Load and inspect data
#     print(data.head())
#     print(data.info())
#     print(data.describe())

#     # Check for missing values
#     print(data.isnull().sum())
#     sns.heatmap(data.isnull(), cbar=False)
#     plt.show()

#     # Plot histograms
#     data.hist(bins=50, figsize=(10, 8))
#     plt.show()

#     numeric_data = data.select_dtypes(include=['number'])
#     correlation_matrix = numeric_data.corr()
#     plt.figure(figsize=(10, 8))
#     sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
#     plt.show()

#     return data

# def split_data(data, parameters):
#     X = data[['Temperature', 'Humidity', 'WindSpeed', 'GeneralDiffuseFlows', 'DiffuseFlows']]
#     Y = data[['PowerConsumption_Zone1', 'PowerConsumption_Zone2', 'PowerConsumption_Zone3']]

#     X_train, X_temp, Y_train, Y_temp = train_test_split(
#         X, Y, test_size=parameters["test_size"], random_state=parameters["random_state"]
#     )
#     X_dev, X_test, Y_dev, Y_test = train_test_split(
#         X_temp, Y_temp, test_size=0.5, random_state=parameters["random_state"]
#     )

#     return X_train, X_dev, X_test, Y_train, Y_dev, Y_test

# def train_models(X_train, Y_train, X_dev, Y_dev, parameters):
#     # Initialize W&B run
#     wandb.init(
#         project=parameters['wandb']['project'],
#         entity=parameters['wandb']['entity'],
#         name='train_models',
#         config=parameters  # Logs all parameters
#     )

#     models = {
#         'LinearRegression': LinearRegression(),
#         'DecisionTreeRegressor': DecisionTreeRegressor(random_state=parameters["random_state"]),
#         'RandomForestRegressor': RandomForestRegressor(random_state=parameters["random_state"])
#     }

#     param_distributions = parameters["hyperparameters"]
#     n_iter = parameters["n_iter"]
#     cv_folds = parameters["cv_folds"]

#     tuned_models = {}

#     for model_name, model in models.items():
#         print(f"Configuring parameters for {model_name}")

#         search = RandomizedSearchCV(
#             estimator=model,
#             param_distributions=param_distributions[model_name],
#             n_iter=n_iter,
#             scoring='neg_mean_absolute_error',
#             cv=cv_folds,
#             random_state=parameters["random_state"],
#             n_jobs=-1
#         )

#         search.fit(X_dev, Y_dev)
#         best_model = search.best_estimator_
#         tuned_models[model_name] = best_model

#         # Log hyperparameters and metrics to W&B
#         wandb.log({
#             f"{model_name}_best_params": search.best_params_,
#             f"{model_name}_best_score": -search.best_score_
#         })

#         print(f"Best parameters for {model_name}: {search.best_params_}")
#         print(f"Best MAE for {model_name}: {-search.best_score_:.2f}")

#     # Train models on the full training data
#     for model_name, model in tuned_models.items():
#         model.fit(X_train, Y_train)
#         print(f"{model_name} model trained.")

#     wandb.finish()

#     return tuned_models


# def evaluate_models(models, X_test, Y_test, parameters):
#     # Initialize W&B run
#     wandb.init(
#         project=parameters['wandb']['project'],
#         entity=parameters['wandb']['entity'],
#         name='evaluate_models'
#     )

#     results = {}
#     for name, model in models.items():
#         predictions = model.predict(X_test)
#         mae = mean_absolute_error(Y_test, predictions)
#         mse = mean_squared_error(Y_test, predictions)
#         r2 = r2_score(Y_test, predictions)
#         results[name] = {'MAE': mae, 'MSE': mse, 'R2': r2}

#         # Log evaluation metrics to W&B
#         wandb.log({
#             f"{name}_MAE": mae,
#             f"{name}_MSE": mse,
#             f"{name}_R2": r2
#         })

#     results_df = pd.DataFrame(results).T
#     print(results_df)

#     # Optionally, log the results DataFrame as a table
#     wandb.log({"evaluation_results": wandb.Table(dataframe=results_df)})

#     wandb.finish()

#     return results_df

