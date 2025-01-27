"""
Module for performing exploratory data analysis (EDA) on a dataset.
"""

import matplotlib.pyplot as plt
import seaborn as sns

def perform_analysis(data):
    """
    Perform basic data inspection, handle missing values visualization,
    plot histograms, and create a correlation heatmap for numeric features.

    Args:
        data (pd.DataFrame): The input dataset to be analyzed.

    Returns:
        pd.DataFrame: The original or modified dataset after dropping any unwanted columns.
    """

    # Remove 'ID' column if it exists
    if 'ID' in data.columns:
        data = data.drop(columns=['ID'])

    # Basic inspection
    print(data)
    print(data.head())
    print(data.info())
    print(data.describe())

    # Check and visualize missing values
    print(data.isnull().sum())
    sns.heatmap(data.isnull(), cbar=False)
    plt.show()

    # Plot histograms for numeric columns
    data.hist(bins=50, figsize=(10, 8))
    plt.show()

    # Compute and plot correlation matrix
    numeric_data = data.select_dtypes(include=['number'])
    correlation_matrix = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.show()

    return data
