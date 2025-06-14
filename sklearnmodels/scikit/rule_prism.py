import sys

from scipy.odr import Output
from sklearn.base import BaseEstimator
from sklearn.utils import compute_class_weight
from sklearnmodels.backend import Input
from sklearnmodels.backend.core import Dataset
from sklearnmodels.backend.factory import DEFAULT_BACKEND
from sklearnmodels.rules.oner import OneR
from sklearnmodels.rules.prism import PRISM
from sklearnmodels.scikit.nominal_model import NominalClassifier

import numpy as np
import pandas as pd

eps = 1e-16


class PRISMClassifier(NominalClassifier, BaseEstimator):
    def __init__(
        self,
        max_rule_length: int = sys.maxsize,
        max_rules_per_class: int = sys.maxsize,
        min_rule_support=10,
        max_error_per_rule=eps,
        backend=DEFAULT_BACKEND,
        class_weight: np.ndarray | None = None,
    ):
        super().__init__(backend=backend, class_weight=class_weight)
        self.max_rule_length = max_rule_length
        self.max_rules_per_class = max_rules_per_class
        self.min_rule_support = min_rule_support
        self.max_error_per_rule = max_error_per_rule

    def make_model(self, d: Dataset, class_weight: np.ndarray):
        return PRISM(
            class_weight,
            self.max_rule_length,
            self.max_rules_per_class,
            self.min_rule_support,
            self.max_error_per_rule,
        )
