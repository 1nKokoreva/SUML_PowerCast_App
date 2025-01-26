"""
Module for splitting the dataset into training, validation, and test sets.
"""

from sklearn.model_selection import train_test_split

def split_data(data, parameters):
    """
    Splits the given dataset into training, validation, and test sets.

    Args:
        data (pd.DataFrame): The dataset containing all features.
        parameters (dict): A dictionary of split parameters, for example:
            {
                "test_size": 0.2,
                "random_state": 42
            }

    Returns:
        tuple: A tuple of six elements:
            (x_train, x_dev, x_test, y_train, y_dev, y_test),
            where x_* and y_* represent features and target values for the respective sets.
    """

    x_data = data[['Temperature', 'Humidity', 'WindSpeed', 'GeneralDiffuseFlows', 'DiffuseFlows']]
    y_data = data[['PowerConsumption_Zone1', 'PowerConsumption_Zone2', 'PowerConsumption_Zone3']]

    x_train, x_temp, y_train, y_temp = train_test_split(
        x_data,
        y_data,
        test_size=parameters["test_size"],
        random_state=parameters["random_state"]
    )

    x_dev, x_test, y_dev, y_test = train_test_split(
        x_temp,
        y_temp,
        test_size=0.5,
        random_state=parameters["random_state"]
    )

    return x_train, x_dev, x_test, y_train, y_dev, y_test
