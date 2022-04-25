import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/') 

import pandas as pd
from itertools import combinations
from numpy import arange, isclose

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
    
    active_planets      = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    
    singles_degrees     = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    
    aspekts_degrees     = {'Con':0, 'Sixt':60, 'Sque':90, 'Trin':120, 'Opp':180}


class GeneralMethods:
    
    @staticmethod
    def degree_transform(point: float):
        x = point // 1
        y = point % 1 * 0.6
        z = round(x + y, 2)
        return z
    
    @staticmethod
    def plus_minus_obj_lon_deg(obj_lon: float, deg: int, sinlge: str):
        if sinlge != '+' and sinlge != '-':
            print("Unsuported value in sinlge(-,+)")
        
        if sinlge == '+' and obj_lon + deg < 360:
            obj_lon_deg_plus = obj_lon + deg
        elif sinlge == '+':
            obj_lon_deg_plus = abs(360 - obj_lon - deg)
        else:
            obj_lon_deg_plus = None
        
        if sinlge == '-' and obj_lon - deg < 0:
            obj_lon_deg_minus = 360 - abs(obj_lon - deg)
        elif sinlge == '-':
            obj_lon_deg_minus = abs(obj_lon - deg)   
        else:
            obj_lon_deg_minus = None
        
        if obj_lon_deg_plus is not None:
            return obj_lon_deg_plus
        else:
            return obj_lon_deg_minus
            
    @staticmethod
    def equal_different_sing_feature(singles_degrees: list, include_lon: float, obj_lon: float, deg: int):
        all_sings_feature = []
        include_lon = round(include_lon, 2)
        obj_lon = round(obj_lon, 2)
        
        obj_lon_deg_plus = GeneralMethods.plus_minus_obj_lon_deg(obj_lon, deg, '+')
        obj_lon_deg_minus = GeneralMethods.plus_minus_obj_lon_deg(obj_lon, deg, '-')

        for ind, x in  enumerate(singles_degrees):
            if ind < len(singles_degrees)-1 and \
            isclose(include_lon, arange(x, singles_degrees[ind+1], 0.01)).any() and \
            (isclose(obj_lon_deg_plus, arange(x, singles_degrees[ind+1], 0.01)).any() or \
             isclose(obj_lon_deg_minus, arange(x, singles_degrees[ind+1], 0.01)).any()):
                all_sings_feature.append(1)
            else:
                all_sings_feature.append(0)
            
            if 1 in all_sings_feature:
                sings_feature = 'equal'
            else:
                sings_feature = 'diff'
            
        return sings_feature 
    
    
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
     

class AspectsCalculate:
    
    def __init__(self, sr: pd.Series):
        self.sr = sr
        self.col_name_ids = 'transform_id'
    
    def cols(self):
        self.list_objs = []
        for obj in self.sr: 
            if hasattr(obj, 'lon'):
                self.list_objs.append(obj)
        return self.list_objs
        
    def list_ids(self):
        self._ids = [x[1] for x in self.sr[self.col_name_ids]]
        return self._ids 
    
    def unique_objects(self):
        used = set()
        self.unique_objs = [x for x in self.list_objs if x.id not in used and (used.add(x.id) or True)]
        return self.unique_objs
    
    def zeroing_some_longspeed(self):
        all_objects = []
        for obj in self.unique_objs:
            if hasattr(obj,'lonspeed') and obj.meanMotion() == 0:
                obj.lonspeed = 0
            all_objects.append(obj)
        self.unique_objs =  all_objects  
        return  self.unique_objs
    

    
    
    # def arrange_orbs_longitude(self):
    #     self.orbs_arrange = []
    #     for obj in self.unique_objs:
    #         if obj.orb() != 0:
    #             start_orb = float(f'{obj.lon - obj.orb():.2f}')
    #             end_orb = float(f'{obj.lon + obj.orb():.2f}')
    #             tuple_orbs = (obj.id, round(obj.lon, 2), start_orb, end_orb)
    #             self.orbs_arrange.append(tuple_orbs)
    #     return self.orbs_arrange
    
#     @staticmethod
#     def house_type_orb_conuction(lon_house: float, lon_obj: float):
#         if lon_house <= lon_obj and lon_house // 100 == lon_obj // 100:
#             type_con = 'in'
#             orb_con = lon_obj - lon_house
#         elif lon_house >= lon_obj and lon_house // 100 == lon_obj // 100:
#             type_con = 'out'
#             orb_con = lon_house - lon_obj
#         else:
#             if lon_house > lon_obj:
#                 type_con = 'in'
#                 orb_con = abs(lon_house - lon_obj - 360)
#             else:
#                 type_con = 'out'
#                 orb_con = abs(lon_house - lon_obj + 360)
        
#         type_con = type_con
#         orb_con = GeneralMethods.degree_transform(orb_con)
        
#         return type_con, orb_con
    
#     def houses_conuctions(self):
#         singles_degrees = [x for x in AstrologicalConstants.singles_degrees]
        
#         self.all_houses_conuctions = []
#         for obj in self.unique_objs:
#             for id_orbs in self.orbs_arrange:
#                 if not obj.orb():
#                     if id_orbs[3] > 360 and \
#                     (isclose(round(obj.lon, 2), arange(id_orbs[2], 359.99, 0.01)).any() or isclose(round(obj.lon, 2), arange(0, id_orbs[3] - 360, 0.01)).any()):
#                         type_con, orb_con = AspectsCalculate.house_type_orb_conuction(obj.lon, id_orbs[1])
#                         sing = GeneralMethods.equal_different_sing_feature(singles_degrees, obj.lon, id_orbs[1])

#                     elif id_orbs[2] < 0 and \
#                     (isclose(round(obj.lon, 2), arange(360 + id_orbs[2], 359.99, 0.01)).any() or isclose(round(obj.lon, 2), arange(0, id_orbs[3], 0.01)).any()):
#                         type_con, orb_con = AspectsCalculate.house_type_orb_conuction(obj.lon, id_orbs[1])
#                         sing = GeneralMethods.equal_different_sing_feature(singles_degrees, obj.lon, id_orbs[1])

#                     elif isclose(round(obj.lon, 2), arange(id_orbs[2], id_orbs[3], 0.01)).any():
#                         type_con, orb_con = AspectsCalculate.house_type_orb_conuction(obj.lon, id_orbs[1])
#                         sing = GeneralMethods.equal_different_sing_feature(singles_degrees, obj.lon, id_orbs[1])
#                     else:
#                         type_con, orb_con, sing = None, None, None
                    
#                     houses_conuctions = {'type': 'Con', 'pos': type_con, 'sing': sing, 'f_point': obj.id, 's_point': id_orbs[0], 'orb': orb_con}   
                    
#                     if houses_conuctions['pos'] != None:
#                         self.all_houses_conuctions.append(houses_conuctions) 
                
#         return self.all_houses_conuctions
    
#     @staticmethod
#     def object_data(objects: list, name_obj: str):
#         for obj in objects:
#             if obj.id == name_obj:
#                 obj_id, obj_lon, obj_orb = obj.id, obj.lon, obj.orb()
#                 return obj_id, obj_lon, obj_orb
    
    # @staticmethod
    # def remove_moon_obj(objects: list):
    #     objs_wt_moon = [x for x in objects if x.id != 'Moon']
    #     return objs_wt_moon
    
    # @staticmethod
    # def remove_houses_obj(objects: list):
    #     objs_wt_houses = [x for x in objects if x.orb()]
    #     return objs_wt_houses
    
#     def moon_aspekts(self):
#         singles_degrees = [x for x in AstrologicalConstants.singles_degrees]
#         self.all_moon_aspekts = []
    
#         moon_id, moon_lon, moon_orb = AspectsCalculate.object_data(self.unique_objs, 'Moon')
#         objects = AspectsCalculate.remove_moon_obj(self.unique_objs)
#         objects = AspectsCalculate.remove_houses_obj(self.unique_objs)

#         for obj in self.unique_objs:
#             for type_asp , deg in AstrologicalConstants.aspekts_degrees.items():
#                 if moon_lon + moon_orb + deg > 360 and \
#                 isclose(round(obj.lon, 2), arange(moon_lon + deg - 360, moon_lon + moon_orb + deg - 360, 0.01)).any():
#                     asp = type_asp
#                     type_con = 'conv'
#                     orb_con = moon_lon + moon_orb + deg - 360 - obj.lon
#                     orb_con = GeneralMethods.degree_transform(orb_con)
#                     sing = GeneralMethods.equal_different_sing_feature(singles_degrees, moon_lon + deg, obj.lon)

#                 elif isclose(round(obj.lon, 2), arange(moon_lon + deg, moon_lon + moon_orb + deg, 0.01)).any():
#                     asp = type_asp
#                     type_con = 'conv'
#                     orb_con = moon_lon + moon_orb + deg - obj.lon
#                     orb_con = GeneralMethods.degree_transform(orb_con)
#                     sing = GeneralMethods.equal_different_sing_feature(singles_degrees, moon_lon + deg, obj.lon)

#                 elif moon_lon + deg > 360 and \
#                 isclose(round(obj.lon, 2), arange(moon_lon + deg - 1 - 360, moon_lon + deg - 360, 0.01)).any():
#                     asp = type_asp
#                     type_con = 'diver'
#                     orb_con = moon_lon + deg - 360 - obj.lon
#                     orb_con = - GeneralMethods.degree_transform(orb_con)
#                     sing = GeneralMethods.equal_different_sing_feature(singles_degrees, moon_lon + deg, obj.lon)

#                 elif isclose(round(obj.lon, 2), arange(moon_lon + deg - 1, moon_lon + deg, 0.01)).any():
#                     asp = type_asp
#                     type_con = 'diver'
#                     orb_con = moon_lon + deg - obj.lon
#                     orb_con = - GeneralMethods.degree_transform(orb_con)
#                     sing = GeneralMethods.equal_different_sing_feature(singles_degrees, moon_lon + deg, obj.lon)    

#                 else:
#                     asp, type_con, orb_con, sing = None, None, None, None

#                 moon_aspects = {'type': asp, 'pos': type_con, 'sing': sing, 'f_point': 'Moon', 's_point': obj.id, 'orb': orb_con}

#                 if moon_aspects['type'] != None:
#                     self.all_moon_aspekts.append(moon_aspects)

#         return self.all_moon_aspekts 
    
    @staticmethod
    def remove_name_from_typle(tuple_list: list, name: str):
        name_list = [x[0] for x in tuple_list]
        if name in name_list:
            name_index = name_list.index(name)
            tuple_list.pop(name_index) 
            return tuple_list

    
    
    
    def join_aspects(self):
        self.all_aspects = self.all_houses_conuctions.copy()
        self.all_aspects.append(self.all_moon_aspekts)
        return self.all_aspects
            
    
    def conbine_class_methods(self):
        self.cols()
        self.list_ids()
        self.unique_objects()
        return self.zeroing_some_longspeed()
        # self.houses_conuctions()
        # return self.moon_aspekts()
        # return self.join_aspects()

        # self.arrange_orbs_longitude()