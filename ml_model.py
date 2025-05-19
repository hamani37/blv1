import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

class TradingAIAutoLearn:
    def __init__(self):
        self.model = None
        self.training_data = pd.DataFrame()
        self.signal_count = 0
        self.accuracy = 0.0
        self.model_file = "trading_model.pkl"
        
        try:
            self.model = joblib.load(self.model_file)
        except:
            pass

    def add_training_data(self, data):
        new_row = pd.DataFrame([{
            'rsi': data['rsi'],
            'macd_diff': data['macd_diff'],
            'variation': data['variation_1m'],
            'signal_type': data['signal_type'],
            'target': 1 if ((data['signal_type'] == 'LONG' and data['variation_1m'] >= 0.5) or 
                           (data['signal_type'] == 'SHORT' and data['variation_1m'] <= -0.5)) else 0
        }])
        
        self.training_data = pd.concat([self.training_data, new_row])
        self.signal_count += 1
        
        if self.signal_count % 50 == 0:
            self._train_model()

    def _train_model(self):
        X = pd.get_dummies(self.training_data[['rsi', 'macd_diff', 'variation', 'signal_type']])
        y = self.training_data['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3
        )
        self.model.fit(X_train, y_train)
        self.accuracy = self.model.score(X_test, y_test)
        joblib.dump(self.model, self.model_file)

    def predict(self, features):
        if self.model:
            X = pd.DataFrame([[
                features['rsi'],
                features['macd_diff'],
                features['variation']
            ]], columns=['rsi', 'macd_diff', 'variation'])
            return self.model.predict_proba(X)[0][1]
        return 0.0

    @property
    def model_ready(self):
        return self.model is not None
