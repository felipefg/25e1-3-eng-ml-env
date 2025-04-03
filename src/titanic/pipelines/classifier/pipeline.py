"""
This is a boilerplate pipeline 'classifier'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.prepare_data,
            inputs=['raw_train'],
            outputs='train',
            tags=['preprocessamento']
        ),
        node(
            nodes.logistic_regression_model,
            inputs=[
                'train',
                'params:session_id',
            ],
            outputs='lr_model',
            tags=['treinamento']
        ),
        # node(
        #     nodes.best_model_from_comparison,
        #     inputs=[
        #         'train',
        #         'params:session_id',
        #     ],
        #     outputs='best_model',
        #     tags=['treinamento']
        # ),
        node(
            nodes.plot_roc,
            inputs=[
                'train',
                'lr_model',
                'params:session_id',
                'params:lr_model_roc_filename',
            ],
            outputs=None,
            tags=['report']
        ),
        # node(
        #     nodes.plot_roc,
        #     inputs=[
        #         'train',
        #         'best_model',
        #         'params:session_id',
        #         'params:best_model_roc_filename',
        #     ],
        #     outputs=None,
        #     tags=['report']
        # ),
    ])
