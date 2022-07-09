import analyser_tech as tech
import model_stock as model

PREDICT_5D_REGRESSION = 10010
R_THRESHOLD = 0.7


def calculate_5d_regression(ts_code, trade_date, regression_data):
    predictions = []
    if regression_data is not None and len(regression_data) > 2 and regression_data[0] > R_THRESHOLD:
        pred = model.Prediction()
        pred.ts_code = ts_code
        pred.predict_date = trade_date
        pred.signal_code = tech.CHART_5D_REG
        pred.algorithm_code = PREDICT_5D_REGRESSION
        pred.predict_days = 1
        pred.predict_score = regression_data[0]
        pred.predict_value = regression_data[2]
        pred.value_name = 'DAY CLOSE'
        pred.score_method = 'R Squired'
        predictions.append(pred)
    return predictions
