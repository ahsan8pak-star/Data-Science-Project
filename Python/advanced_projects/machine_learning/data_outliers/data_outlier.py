import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierCapper(BaseEstimator, TransformerMixin):
    """
    A custom scikit-learn transformer that caps outliers using the 
    Interquartile Range (IQR) method.
    """
    def __init__(self, factor = 1.5):
        self.factor = factor
        
    def fit(self, X, y = None):
        # Calculate IQR bounds during fit
        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)
        IQR = Q3 - Q1
        self.lower_bound_ = Q1 - (self.factor * IQR)
        self.upper_bound_ = Q3 + (self.factor * IQR)
        return self

    def transform(self, X):
        # Clip values to upper and lower IQR bounds
        return X.clip(lower = self.lower_bound_, upper = self.upper_bound_, axis = 1)

