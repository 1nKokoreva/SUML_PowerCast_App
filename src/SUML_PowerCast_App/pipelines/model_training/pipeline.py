"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, node, pipeline

from .split_data import split_data
from .train_models import train_models
from .evaluate_models import evaluate_models


def create_pipeline() -> Pipeline:
    """
    Creates the main pipeline for the model training process.

    Args:
        **kwargs: Additional keyword arguments (not used in this pipeline).
    
    Returns:
        Pipeline: A Kedro pipeline that includes data splitting, model training, 
                  and model evaluation nodes.
    """
    return pipeline([
        node(
            func=split_data,
            inputs=["power_consumption_raw", "parameters"],
            outputs=["X_train", "X_dev", "X_test", "Y_train", "Y_dev", "Y_test"],
            name="split_data_node"
        ),
        node(
            func=train_models,
            inputs=["X_train", "Y_train", "X_dev", "Y_dev", "parameters"],
            outputs="trained_models",
            name="train_models_node"
        ),
        node(
            func=evaluate_models,
            inputs=["trained_models", "X_test", "Y_test", "parameters"],
            outputs=["model_metrics", "best_models"],
            name="evaluate_models_node"
        )
    ])
