"""
This is a boilerplate pipeline 'app_run'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, node, pipeline
from .api_run import api_run

def create_pipeline() -> Pipeline:
    """
    Creates a Kedro pipeline that runs the api_run node to start the API
    using the best_models input.

    Returns:
        Pipeline: The constructed pipeline for running the API.
    """
    return pipeline([
        node(
            func=api_run,
            inputs=["best_models"],
            outputs=None,
            name="api_node"
        )
    ])
