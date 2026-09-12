"""
Pytest suite for the machine-learning folder's IQR outlier capper.

Covers `python/advanced_projects/machine_learning/data_outliers/data_outlier.py`,
which exposes a custom scikit-learn transformer (OutlierCapper). The notebook
(.ipynb) versions hold the exploration; the .py file is the durable, testable
module, so it is imported once (conftest.load_module) and exercised like any
estimator.

The module lives under a nested package (machine_learning/data_outliers) that
is not on sys.path, so it is loaded by file path via `load_module()` in a
session-scoped fixture rather than a plain `import` statement.
"""

import pandas as pd
import pytest

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from tests.test_advanced_projects.conftest import load_module

_DATA = pd.DataFrame(
    {
        "value_a": [1, 2, 3, 4, 5, 100],
        "value_b": [10, 20, 30, 40, 50, 60],
    }
)

# IQR bounds for _DATA with the default factor of 1.5 (pandas linear
# interpolation over the quantiles).
# value_a: Q1=2.25 Q3=4.75 -> lower=2.25-2.5*1.5=-1.5 upper=4.75+2.5*1.5=8.5
# value_b: Q1=22.5 Q3=47.5  -> lower=22.5-25*1.5=-15.0 upper=47.5+25*1.5=85.0
_EXPECTED_LOWER = pd.Series({"value_a": -1.5, "value_b": -15.0})
_EXPECTED_UPPER = pd.Series({"value_a": 8.5, "value_b": 85.0})


@pytest.fixture(scope="session")
def outlier_module():
    """Load data_outlier.py once so OutlierCapper keeps a stable identity."""
    return load_module("machine_learning/data_outliers/data_outlier.py")


class TestOutlierCapperBasics:
    """Structural sanity - name, inheritance, constructor default."""

    def test_is_sklearn_estimator(self, outlier_module):
        assert isinstance(outlier_module.OutlierCapper(), BaseEstimator)
        assert isinstance(outlier_module.OutlierCapper(), TransformerMixin)

    def test_default_factor_is_1_5(self, outlier_module):
        assert outlier_module.OutlierCapper().factor == 1.5

    def test_custom_factor_stored(self, outlier_module):
        assert outlier_module.OutlierCapper(factor=3.0).factor == 3.0


class TestOutlierCapperFit:
    """Boundary computation during fit()."""

    def test_fit_returns_self(self, outlier_module):
        capper = outlier_module.OutlierCapper()
        assert capper.fit(_DATA) is capper

    def test_bounds_match_hand_computed_iqr(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)

        pd.testing.assert_series_equal(capper.lower_bound_, _EXPECTED_LOWER)
        pd.testing.assert_series_equal(capper.upper_bound_, _EXPECTED_UPPER)

    def test_fit_accepts_y_parameter(self, outlier_module):
        y = pd.Series([0, 1, 0, 1, 0, 1])
        capper = outlier_module.OutlierCapper().fit(_DATA, y=y)
        assert hasattr(capper, "lower_bound_")

    def test_higher_factor_widens_bounds(self, outlier_module):
        default = outlier_module.OutlierCapper(factor=1.5).fit(_DATA)
        lenient = outlier_module.OutlierCapper(factor=3.0).fit(_DATA)

        assert (lenient.lower_bound_ <= default.lower_bound_).all()
        assert (lenient.upper_bound_ >= default.upper_bound_).all()


class TestOutlierCapperTransform:
    """Clipping behaviour during transform()."""

    def test_transform_clips_outlier_upwards(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)

        out = capper.transform(pd.DataFrame({"value_a": [50], "value_b": [10]}))
        assert float(out.iloc[0]["value_a"]) == pytest.approx(8.5)

    def test_transform_clips_outlier_downwards(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)

        out = capper.transform(pd.DataFrame({"value_a": [-50], "value_b": [10]}))
        assert float(out.iloc[0]["value_a"]) == pytest.approx(-1.5)

    def test_transform_leaves_inliers_untouched(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)

        clean = pd.DataFrame({"value_a": [3], "value_b": [40]})
        out = capper.transform(clean)
        assert float(out.iloc[0]["value_a"]) == pytest.approx(3.0)
        assert float(out.iloc[0]["value_b"]) == pytest.approx(40.0)

    def test_transform_returns_dataframe(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)
        assert isinstance(capper.transform(_DATA), pd.DataFrame)

    def test_transform_full_dataset_no_missing_values(self, outlier_module):
        capper = outlier_module.OutlierCapper().fit(_DATA)
        out = capper.transform(_DATA)
        assert not out.isna().any().any()


class TestOutlierCapperPipeline:
    """Integration inside a scikit-learn Pipeline."""

    def test_usable_in_pipeline(self, outlier_module):
        pipeline = Pipeline([("cap", outlier_module.OutlierCapper())])
        out = pipeline.fit_transform(_DATA)
        assert isinstance(out, pd.DataFrame)
        assert out.shape == _DATA.shape

    def test_pipeline_outlier_neutralised(self, outlier_module):
        pipeline = Pipeline([("cap", outlier_module.OutlierCapper())])
        out = pipeline.fit_transform(_DATA)

        assert float(out["value_a"].max()) == pytest.approx(8.5)
        assert float(out["value_a"].min()) == pytest.approx(1.0)