import pandas as pd

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.dignities import essential
from flatlib.object import GenericObject


class AstrologicalConstants:
    
    houses_objects      = ['asc', 'desc', 'mc', 'ic']
    
    rulers_constants    = ['ASC', 'DESC', 'MC', 'IC', 'PARS_FORTUNA']
    
    necessary_constants = ['SUN', 'MOON', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO', 'CHIRON', 'NORTH_NODE', 'SOUTH_NODE']
    
    main_objects        = ['moon', 'ruler_asc', 'ruler_desc', 'pars_fortuna', 'ruler_pars_fortuna', 'ruler_mc', 'ruler_ic', 'sun', 
                           'saturn', 'uranus', 'neptune', 'pluto', 'chiron', 'north_node', 'south_node']
    
    antes_objects       = ['pars_fortuna', 'uranus', 'neptune', 'pluto', 'chiron']


class AstrologicalPoints:
    
    @staticmethod
    def charts_calculate(df: pd.DataFrame, date:str, utc_time:str, lon:str, lat:str):

        dates = df.apply(lambda x: Datetime(x[date], x[utc_time], '+00:00'), axis=1)
        posits = df.apply(lambda x: GeoPos(x[lon], x[lat]), axis=1)
        df_dates_posits = pd.concat([dates, posits], axis=1, keys=['dates', 'posits'])
        charts = df_dates_posits.apply(lambda x: Chart(x['dates'], x['posits']), axis=1)
        return charts
    
    @staticmethod
    def calculate_astro_objects(charts: pd.Series, name_of_object: str):
        objects = charts.map(lambda x: x.get(getattr(const, name_of_object)))
        return objects
    
    @staticmethod
    def rulers_col_names(rulers_list: list):
        rulers_col_names = ['ruler_' + str.lower(x) for x in rulers_list]
        return rulers_col_names
    
    @staticmethod
    def ruler_of_object(col_object: pd.Series):
        rulers_name = col_object.map(lambda x: essential.ruler(getattr(x, 'sign')))
        return rulers_name
    
    @staticmethod
    def chart_object_attributes(df: pd.DataFrame, col_charts: str, col_obj_names: str):
        object_attributes = df.apply(lambda x: x[col_charts].get(x[col_obj_names]), axis=1)
        return object_attributes
    
    @staticmethod
    def antes_objects(df: pd.DataFrame, col_for_antes: str):
        antes_objectcs = df[col_for_antes].map(lambda x: GenericObject.antiscia(x))
        return antes_objectcs
     
    @staticmethod
    def chart_unique_ids(df: pd.DataFrame, cols_for_id: list):
        
        unique_ids = df[cols_for_id].apply(lambda x: [i for i in x])
#             unique_ids = set(unique_ids)
#             unique_ids.append(unique_id)
        return unique_ids   

class AstrologicalRules:
    
    @staticmethod
    def main_objects():
        pass
    