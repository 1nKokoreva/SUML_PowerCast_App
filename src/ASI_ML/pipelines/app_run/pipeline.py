"""
This is a boilerplate pipeline 'app_run'
generated using Kedro 0.19.10
"""
from kedro.pipeline import Pipeline, node
from .api_run import api_run
from kedro.pipeline import Pipeline, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=api_run,
            inputs=["best_models"],
            outputs=None,
            name="api_node"
        )])
