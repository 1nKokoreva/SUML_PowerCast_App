from kedro.pipeline import Pipeline
from ASI_ML.pipelines.data_science import pipeline as ds_pipeline

def register_pipelines():
    return {
        "ds": ds_pipeline.create_pipeline(),
        "__default__": ds_pipeline.create_pipeline(),
    }
