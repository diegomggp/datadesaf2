from prophet import Prophet
import pandas as pd
import datetime as dt

class MetricAnalyzer:
    def __init__(self, id):
        self.id = id

    def fx__get_metrics(self,json):
        return {'test':'0'}