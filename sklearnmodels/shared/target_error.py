import abc

import numpy as np
import pandas as pd

from sklearnmodels.backend.core import Dataset, Partition


class TargetError(abc.ABC):
    @abc.abstractmethod
    def __call__(self, d: Dataset) -> float:
        pass

    def average_split(self, partition: list[Dataset]):
        error = 0.0
        n = 0
        for d_branch in partition:
            branch_error = self(d_branch)
            n_branch = d_branch.n
            error += n_branch * branch_error
            n += n_branch
        if n == 0:
            return np.inf
        else:
            return error / n

    @abc.abstractmethod
    def prediction(self, d: Dataset):
        pass

    def __repr__(self):
        return self.__class__.__name__


eps = 1e-32


def log(x, base):
    x[x < eps] = eps
    if base == 2:
        return np.log2(x)
    elif base == 0:
        return np.log(x)
    elif base == 10:
        return np.log10(x)
    else:
        lb = 1 / np.log(base)
        return np.log(x) * lb


class ClassificationError(TargetError):
    def __init__(self, classes: int, class_weight: np.ndarray = None):
        if class_weight is None:
            class_weight = np.ones(classes)

        self.classes = classes
        self.class_weight = class_weight

    def prediction(self, d: Dataset):
        y = d.y
        if len(y) == 0:
            result = np.ones(self.classes) / self.classes
        else:
            if np.issubdtype(y.dtype, object):
                # string classes
                y_cat = pd.Series(data=y.squeeze()).astype("category")
                y = y_cat.cat.codes.to_numpy().reshape(-1, 1)
            # numeric index classes classes
            counts = np.bincount(y, minlength=self.classes)
            result = counts / counts.sum()
            # print(result.dtype,self.class_weight.dtype)
        result *= self.class_weight
        result /= result.sum()
        return result

    def __repr__(self):
        return f"{super().__repr__()}(classes={self.classes})"


class EntropyError(ClassificationError):
    def __init__(self, classes: int, class_weight: np.ndarray = None, base=2):
        super().__init__(classes, class_weight)
        self.base = base

    def __call__(self, d: Dataset):
        p = self.prediction(d)
        # largest_value = log(np.array([self.classes]),self.base)[0]

        return -np.sum(p * log(p, self.classes))


class AccuracyError(ClassificationError):
    def __init__(self, classes: int, class_weight: np.ndarray = None):
        super().__init__(classes, class_weight)

    def __call__(self, d: Dataset):
        p = self.prediction(d)
        i = p.argmax()

        # largest_value = log(np.array([self.classes]),self.base)[0]

        return 1 - np.sum(y == i) / len(y)


class GiniError(ClassificationError):
    def __init__(self, classes: int, class_weight: np.ndarray, base=2):
        super().__init__(classes, class_weight)
        self.base = base

    def __call__(self, d: Dataset):
        p = self.prediction(d)
        # largest_value = log(np.array([self.classes]),self.base)[0]
        return 1 - np.sum(p**2)


class RegressionError(TargetError):
    def prediction(self, d: Dataset):
        return d.mean_y()


class DeviationError(RegressionError):
    def __call__(self, d: Dataset):
        return d.std_y()
