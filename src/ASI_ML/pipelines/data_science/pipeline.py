from kedro.pipeline import Pipeline, node
from .perform_analysis import perform_analysis
def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=perform_analysis,
            inputs="power_consumption_raw_db",
            outputs=None,
            name="perform_analysis_node"
        )
    ])