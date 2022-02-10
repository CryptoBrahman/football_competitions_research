import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/') 

import pandas as pd

from flatlib import const
from flatlib.tools import arabicparts
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.dignities import essential
from flatlib.object import GenericObject


class AstrologicalConstants:
    
    houses_objects      = ['asc', 'desc', 'mc', 'ic']
    
    rulers_constants    = ['ASC', 'DESC', 'MC', 'IC', 'PARS_FORTUNA']
    
    necessary_constants = ['SUN', 'MOON', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO', 'CHIRON', 'NORTH_NODE', 'SOUTH_NODE']
    
    main_objects        = ['moon', 'sun', 'saturn', 'uranus', 'neptune', 'pluto', 'chiron', 'north_node', 'south_node'] 
                           
    ruler_objects       = ['ruler_asc', 'ruler_desc', 'ruler_mc', 'ruler_ic', 'ruler_pars_fortuna', 'ruler_antes_pars_fortuna',
                           'ruler_pars_spirit', 'ruler_pars_glory', 'ruler_pars_crest', 'ruler_pars_rock']
    
    pars_objects        = ['pars_fortuna', 'pars_spirit', 'pars_glory', 'pars_crest', 'pars_rock']
    
    for_antes_objects   = ['moon', 'ruler_asc', 'ruler_desc', 'ruler_mc', 'ruler_ic', 'pars_fortuna', 'uranus', 'neptune', 'pluto', 'chiron']
    
    pars_constants      = ['PARS_SPIRIT', 'PARS_GLORY', 'PARS_CREST', 'PARS_ROCK']


class AstrologicalPoints:
    
    @staticmethod
    def charts_calculate(df: pd.DataFrame, date:str, utc_time:str, lon:str, lat:str):

        dates = df.apply(lambda x: Datetime(x[date], x[utc_time], '+00:00'), axis=1)
        posits = df.apply(lambda x: GeoPos(x[lon], x[lat]), axis=1)
        df_dates_posits = pd.concat([dates, posits], axis=1, keys=['dates', 'posits'])
        charts = df_dates_posits.apply(lambda x: Chart(x['dates'], x['posits'],  hsys=const.HOUSES_PLACIDUS), axis=1)
        return charts
    
    @staticmethod
    def calculate_astro_objects(charts: pd.Series, name_of_object: str):
        if name_of_object.startswith('PARS'):
            objects = charts.map(lambda x: arabicparts.getPart(getattr(arabicparts, name_of_object), x))
        else:    
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
    def rename_antes_objects(df: pd.DataFrame, col_antes_for_rename: str):
        for index, row in df[col_antes_for_rename].iteritems():
            row.id = 'Antes ' + str(row.id)            
        
    @staticmethod
    def id_for_aspekts(df: pd.DataFrame, cols_for_id: list):
        all_obj_ids = []
        for index, row in df[cols_for_id].iterrows():
            col_obj_ids = []
            for col, obj_id in row.iteritems():
                col_obj_id = (col, obj_id.id)
                col_obj_ids.append(col_obj_id)  
            all_obj_ids.append(col_obj_ids)
        return all_obj_ids
    

class TransformDoubleValues:   
    
    def __init__(self, tuples_list):
        self.tuples_list = tuples_list
        
    def check_double_values(self):
        all_values = []
        for items in self.tuples_list:
            all_values.append(items[1]) 

            self.double_values = []    
            for val in all_values:
                if all_values.count(val) > 1:
                    self.double_values.append(val)
            self.double_values = list(set(self.double_values))
        return self.double_values

    def check_double_items(self):
        self.double_items = []
        for item in self.tuples_list:
            if item[1] in self.double_values:
                self.double_items.append(item)
        return self.double_items

    def concatinate_id_keys(self):
        self.concat_tuples_list = []
        for val in self.double_values:
            concat_keys = []
            for item in self.double_items:
                if val == item[1]:
                    concat_keys.append(item[0])
            aprsand_keys = '_&_'.join([x for x in concat_keys])
            all_aprsand_keys = (aprsand_keys, val)        
            self.concat_tuples_list.append(all_aprsand_keys)
        return self.concat_tuples_list

    def drop_double_tuple_values(self):
        for item in self.tuples_list:
            if item[1] in self.double_values:
                self.tuples_list.remove(item)
                self.drop_double_tuple_values()
        return self.tuples_list

    def concatinate_tuple_list_id_keys(self):
        for item in self.concat_tuples_list:
            self.tuples_list.append(item)   
        return self.tuples_list
    
    def conbine_class_methods(self):
        self.check_double_values()
        self.check_double_items()
        self.concatinate_id_keys()
        self.drop_double_tuple_values()
        return self.concatinate_tuple_list_id_keys()
     