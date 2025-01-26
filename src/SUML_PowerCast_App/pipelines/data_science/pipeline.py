"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, node
from .perform_analysis import perform_analysis

def create_pipeline() -> Pipeline:
    """
    Creates a Kedro pipeline that runs the data analysis step.

    Args:
        **kwargs: Additional keyword arguments (currently unused).
    
    Returns:
        Pipeline: A Kedro pipeline object containing the perform_analysis node.
    """
    return Pipeline([
        node(
            func=perform_analysis,
            inputs="power_consumption_raw",
            outputs=None,
            name="perform_analysis_node"
        )
    ])
