import sys

from scipy.odr import Output
from sklearn.base import BaseEstimator
from sklearn.utils import compute_class_weight
from sklearnmodels.backend import Input
from sklearnmodels.backend.core import Dataset
from sklearnmodels.backend.factory import DEFAULT_BACKEND
from sklearnmodels.rules.cn2 import CN2
from sklearnmodels.rules.oner import OneR
from sklearnmodels.rules.prism import PRISM
from sklearnmodels.scikit.nominal_model import NominalClassifier, NominalRegressor

import numpy as np
import pandas as pd

eps = 1e-16


class CN2Classifier(NominalClassifier, BaseEstimator):
    def __init__(
        self,
        criterion="entropy",
        max_rule_length: int = sys.maxsize,
        max_rules: int = sys.maxsize,
        min_rule_support=10,
        max_error_per_rule=0.99,
        backend=DEFAULT_BACKEND,
        class_weight: np.ndarray | None = None,
    ):
        super().__init__(backend=backend, class_weight=class_weight)
        self.max_rule_length = max_rule_length
        self.max_rules = max_rules
        self.min_rule_support = min_rule_support
        self.max_error_per_rule = max_error_per_rule
        self.criterion = criterion

    def make_model(self, d: Dataset, class_weight: np.ndarray):
        error = self.build_error(self.criterion, class_weight)
        return CN2(
            error,
            self.max_rule_length,
            self.max_rules,
            self.min_rule_support,
            self.max_error_per_rule,
        )


class CN2Regressor(NominalRegressor, BaseEstimator):
    def __init__(
        self,
        criterion="std",
        max_rule_length: int = sys.maxsize,
        max_rules: int = sys.maxsize,
        min_rule_support=10,
        max_error_per_rule=0.99,
        backend=DEFAULT_BACKEND,
    ):
        super().__init__(backend=backend)
        self.max_rule_length = max_rule_length
        self.max_rules = max_rules
        self.min_rule_support = min_rule_support
        self.max_error_per_rule = max_error_per_rule
        self.criterion = criterion

    def make_model(self, d: Dataset):
        error = self.build_error(self.criterion)
        return CN2(
            error,
            self.max_rule_length,
            self.max_rules,
            self.min_rule_support,
            self.max_error_per_rule,
        )
