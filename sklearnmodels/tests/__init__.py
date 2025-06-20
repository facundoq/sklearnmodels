# Authors: scikit-learn-contrib developers
# License: BSD 3 clause

from sklearn.pipeline import Pipeline
from sklearn.tree import BaseDecisionTree

from sklearnmodels.scikit.nominal_model import NominalModel
from sklearn.tree import _tree


def get_model_complexity(model: NominalModel | BaseDecisionTree) -> int:
    if isinstance(model, NominalModel):
        return model.model_.complexity()
    elif isinstance(model, Pipeline):
        estimator_model = model[-1]
        if isinstance(estimator_model, BaseDecisionTree):
            tree: _tree.Tree = model[-1].tree_
            return tree.n_leaves

    raise ValueError(f"Unsupported model {model}")
