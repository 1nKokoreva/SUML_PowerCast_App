from kedro.pipeline import Pipeline
from ASI_ML.pipelines.data_science import pipeline as ds_pipeline
from ASI_ML.pipelines.app_run import pipeline as app_pipeline
from ASI_ML.pipelines.model_training import pipeline as model_training_pipeline
def register_pipelines():
    return {
        "ds": ds_pipeline.create_pipeline(),
        "app": app_pipeline.create_pipeline(),
        "model_training": model_training_pipeline.create_pipeline(),
        "full": Pipeline(
            model_training_pipeline.create_pipeline().nodes + app_pipeline.create_pipeline().nodes
        ),
        "__default__": Pipeline(
            ds_pipeline.create_pipeline().nodes+ model_training_pipeline.create_pipeline().nodes + app_pipeline.create_pipeline().nodes
        )
    }
