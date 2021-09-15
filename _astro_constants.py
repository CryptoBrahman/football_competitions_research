import pandas as pd

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.dignities import essential


class AstrologicalPoints:
    
    @staticmethod
    def charts_calculate(df: pd.DataFrame, date:str, utc_time:str, lon:str, lat:str):

        dates = df.apply(lambda x: Datetime(x[date], x[utc_time], '+00:00'), axis=1)
        posits = df.apply(lambda x: GeoPos(x[lon], x[lat]), axis=1)
        df_dates_posits =  pd.concat([dates, posits], axis=1, keys=['dates', 'posits'])
        charts = df_dates_posits.apply(lambda x: Chart(x['dates'], x['posits']), axis=1)
        return charts
    
    @staticmethod
    def calculate_astro_objects(charts: pd.Series, name_of_object: str):
        objects = charts.map(lambda x: x.get(getattr(const, name_of_object)))
        return objects
    
    @staticmethod
    def ruler_of_object(col_object: pd.Series):
        rulers_name = col_object.map(lambda x: essential.ruler(getattr(x, 'sign')))
        return rulers_name
    
    @staticmethod
    def chart_object_attributes(df: pd.DataFrame, col_charts: str, col_obj_names: str):
        object_attributes = df.apply(lambda x: x[col_charts].get(x[col_obj_names]), axis=1)
        return object_attributes
