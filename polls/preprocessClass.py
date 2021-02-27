from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler, MinMaxScaler, QuantileTransformer, MaxAbsScaler, RobustScaler, PowerTransformer

class PreProcess(BaseEstimator):

    def __init__(self, classifier_type: str = 'Min-Max Scaler'):

        self.classifier_type = classifier_type
    
    def fit(self, X,y=None):
        if self.classifier_type == 'Standard Scaler':
            self.classifier_ = StandardScaler()
        elif self.classifier_type == 'Min-Max Scaler':
            self.classifier_ = MinMaxScaler()
        elif self.classifier_type == 'Max-Abs Scaler':
            self.classifier_ = MaxAbsScaler()
        elif self.classifier_type == 'Robust Scaler':
            self.classifier_ = RobustScaler()
        elif self.classifier_type == 'Quantile Transformer (Uniform)':
            self.classifier_ = QuantileTransformer(output_distribution="uniform")
        elif self.classifier_type == 'Quantile Transformer (Normal)':
            self.classifier_ = QuantileTransformer(output_distribution="normal")
        elif self.classifier_type == 'Power Transformer':
            self.classifier_ = PowerTransformer(method="yeo-johnson")
        else:
            raise ValueError('Unkown classifier type.')
        self.classifier_.fit(X)
        return self
    def transform(self,X,y=None):
        return self.classifier_.transform(X)
