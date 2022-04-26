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
     

class ObjectsPrepare:
    
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
    
    def conbine_class_methods(self):
        self.cols()
        self.list_ids()
        self.unique_objects()
        return self.zeroing_some_longspeed()

    
class AspectsPrepare:
    
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
        
        obj_lon_deg_plus = AspectsPrepare.plus_minus_obj_lon_deg(obj_lon, deg, '+')
        obj_lon_deg_minus = AspectsPrepare.plus_minus_obj_lon_deg(obj_lon, deg, '-')

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
    
    @staticmethod
    def remove_objects(objects: list, remove_objs: list):
        list_wt_objs = [x for x in objects if x.id not in remove_objs]
        return list_wt_objs
    
    @staticmethod
    def orb_calculate(include_lon: float, obj_lon: float, deg: int):
        obj_lon_deg_plus = AspectsPrepare.plus_minus_obj_lon_deg(obj_lon, deg, '+')
        obj_lon_deg_minus = AspectsPrepare.plus_minus_obj_lon_deg(obj_lon, deg, '-')

        orb_plus = abs(include_lon - obj_lon_deg_plus)
        orb_minus = abs(include_lon - obj_lon_deg_minus)

        if obj_lon_deg_plus == obj_lon_deg_minus:
            orb_plus = 360 - orb_plus
        if orb_plus < orb_minus:
            return round(orb_plus, 2)
        else:
            return round(orb_minus, 2)
        
    @staticmethod
    def pos_neg_obj_lon_deg(obj_lon: float, deg: int):
        pos_obj_lon_deg = obj_lon + deg
        neg_obj_lon_deg = obj_lon - deg

        if pos_obj_lon_deg >= 360:
            pos_obj_lon_deg = abs(360 - pos_obj_lon_deg)
        if neg_obj_lon_deg < 0:
            neg_obj_lon_deg = abs(360 + neg_obj_lon_deg)  

        return pos_obj_lon_deg, neg_obj_lon_deg
    
    @staticmethod
    def transform_list_type(list_blocks: list):
        all_list_blocks = []
        for block in list_blocks:
            if type(block[0]) is list:
                all_list_blocks.append(block[0]) 
                all_list_blocks.append(block[1]) 
            else:
                all_list_blocks.append(block)
        return all_list_blocks 
    
    @staticmethod
    def remove_list_dubles(list_blocks: list):
        for ind, block in enumerate(list_blocks):
            if list_blocks.count(block) > 1:
                list_blocks.pop(ind)
                AspectsPrepare.remove_list_dubles(list_blocks)
                
    @staticmethod
    # for check all blocks transformation (obj_lon: 245, 235, 115, 125, obj_orb: 10, deg: 120)
    def pos_neg_points_orb(obj_lon: float, obj_orb: int, deg: int, before_point_asp = 'no'):
        pos_obj_lon_deg, neg_obj_lon_deg = AspectsPrepare.pos_neg_obj_lon_deg(obj_lon, deg)

        bef_pos_point_orb = pos_obj_lon_deg - obj_orb
        bef_neg_point_orb = neg_obj_lon_deg - obj_orb
        aft_pos_point_orb = pos_obj_lon_deg + obj_orb
        aft_neg_point_orb = neg_obj_lon_deg + obj_orb

        block_1 = [bef_pos_point_orb, pos_obj_lon_deg] 
        block_2 = [pos_obj_lon_deg,   aft_pos_point_orb] 
        block_3 = [bef_neg_point_orb, neg_obj_lon_deg]
        block_4 = [neg_obj_lon_deg,   aft_neg_point_orb]

        if bef_pos_point_orb < 0:
            block_1 = [[360 + bef_pos_point_orb, 359.99], [0, pos_obj_lon_deg]] 
        if aft_pos_point_orb >= 360:
            block_2 = [[pos_obj_lon_deg, 359.99], [0, aft_pos_point_orb - 360]]     
        if bef_neg_point_orb < 0:    
            block_3 = [[360 + bef_neg_point_orb, 359.99], [0, neg_obj_lon_deg]]
        if aft_neg_point_orb >= 360:
            block_4 = [[neg_obj_lon_deg, 359.99], [0, aft_neg_point_orb - 360]]  

        if before_point_asp == 'no': 
            obj_lon_degs = [block_2, block_4]
        elif before_point_asp == 'yes':
            obj_lon_degs = [block_1, block_3]
        else:
            return 'Unsuported value in before_point_asp'

        obj_lon_degs = AspectsPrepare.transform_list_type(obj_lon_degs)
        AspectsPrepare.remove_list_dubles(obj_lon_degs)

        return obj_lon_degs   
    
    @staticmethod
    def switching_ranges_with_orb(include_lon: float, obj_lon: float, obj_orb: int, deg: int, before_point_asp = 'no'):
        obj_lon_degs = AspectsPrepare.pos_neg_points_orb(obj_lon, obj_orb, deg, before_point_asp)

        for lon_degs in obj_lon_degs:
            if isclose(round(include_lon, 2), arange(lon_degs[0], lon_degs[1], 0.01)).any():
                orb_con = AspectsPrepare.orb_calculate(include_lon, obj_lon, deg)
                return orb_con 

    @staticmethod         
    def object_data(objects: list, name: str):
        for obj in objects:
            if obj.id == name:
                if 'meanMotion' not in dir(obj):
                    obj_house = 1
                    obj_lonsp = 0
                else:
                    obj_house = 0
                    obj_lonsp = obj.lonspeed

                obj_id, obj_lon, obj_orb = obj.id, obj.lon, obj.orb()
                return obj_id, obj_lon, obj_orb, obj_lonsp, obj_house
            
    @staticmethod
    def house_type_approuch(incl_lon: float, incl_lonsp: float, obj_lon: float):
        if obj_lon <= incl_lon and round(obj_lon/100) == round(incl_lon/100):
            pos = 'in'
        elif obj_lon >= incl_lon and round(obj_lon/100) == round(incl_lon/100):
            pos = 'out'
        else:
            if  obj_lon >= incl_lon:
                pos = 'in'
            else:
                pos = 'out'

        if incl_lonsp == 0:
            type_appr = pos + '_stat'
        elif (pos == 'in' and incl_lonsp < 0) or (pos == 'out' and incl_lonsp > 0):
            type_appr = pos + '_conv'
        else:
            type_appr = pos + '_diver'

        return type_appr
    
    @staticmethod
    def left_right_semi_circle(incl_lon: float, obj_lon: float, deg: int):
        obj_lon_deg = obj_lon + deg

        if obj_lon_deg > 360:
            obj_lon_deg = abs(360 - obj_lon_deg)

        if obj_lon_deg <= 180 and isclose(round(incl_lon, 2), arange(obj_lon_deg, obj_lon_deg + 180, 0.01)).any():
            incl_lon_pos = 'right'
        elif obj_lon_deg > 180 and (isclose(round(incl_lon, 2), arange(obj_lon_deg, 359.99, 0.01)).any() or \
        isclose(round(incl_lon, 2), arange(0, 360 - obj_lon_deg, 0.01)).any()):
            incl_lon_pos = 'right'
        else:
            incl_lon_pos = 'left'
        return incl_lon_pos 
    
    @staticmethod
    def type_approach(incl_lon: float, incl_lonsp: float, obj_lon: float, obj_lonsp: float, obj_house: int, deg: int):    
        incl_lon_pos = AspectsPrepare.left_right_semi_circle(incl_lon, obj_lon, deg)

        if obj_house == 1:
            type_appr = AspectsPrepare.house_type_approuch(incl_lon, incl_lonsp, obj_lon)
        else:
            if incl_lon_pos == 'left':
                l1_lonsp = incl_lonsp
                l2_lonsp = obj_lonsp 
            else:
                l1_lonsp = obj_lonsp 
                l2_lonsp = incl_lonsp 

            if incl_lonsp == obj_lonsp:
                type_appr = 'stat'

            elif (l1_lonsp == 0 and l2_lonsp > 0)  or \
                 (l1_lonsp < 0  and l2_lonsp == 0) or \
                 (l1_lonsp < 0  and l2_lonsp > 0)  or \
                 (l2_lonsp > l1_lonsp > 0) or \
                 (l1_lonsp < l2_lonsp < 0): # -0.2 speedly than -0.1
                 type_appr = 'diver'
            elif (l1_lonsp == 0 and l2_lonsp < 0)  or \
                 (l1_lonsp > 0  and l2_lonsp == 0) or \
                 (l1_lonsp > 0  and l2_lonsp < 0)  or \
                 (l1_lonsp > l2_lonsp > 0) or \
                 (l2_lonsp < l1_lonsp < 0):
                 type_appr = 'conv'
            else:
                 type_appr = 'no'

        return type_appr   
    
    @staticmethod
    def type_orb_calculate(obj_orb: int, before_point_asp = 'no', after_orb ='const', before_orb ='const'):
        if (after_orb !='const' and type(after_orb) is not int) or (before_orb !='const' and type(before_orb) is not int):
            return 'Unsuported value in conv_orb or diver_orb'

        if before_point_asp == 'no' and after_orb != 'const' and before_orb == 'const':
            orb = after_orb
        elif before_point_asp == 'yes' and after_orb == 'const' and before_orb != 'const':
            orb = before_orb 
        else:
            orb = obj_orb
        return orb
    
    @staticmethod
    def object_aspects(id_obj: str, unique_objs: list, remove_objs: list, aspekts_degrees: dict, before_point_asp = 'no', after_orb ='const', before_orb ='const'):
        singles_degrees = AstrologicalConstants.singles_degrees
        all_aspekts = []
        objects_cp = unique_objs.copy()

        obj_id, obj_lon, obj_orb, obj_lonsp, obj_house = AspectsPrepare.object_data(objects_cp, id_obj)
        obj_orb = AspectsPrepare.type_orb_calculate(obj_orb, before_point_asp, after_orb, before_orb)    
        objects_cp = AspectsPrepare.remove_objects(objects_cp, [id_obj] + remove_objs)

        for incl_obj in objects_cp:
            for type_asp, deg in aspekts_degrees.items():

                orb_con = AspectsPrepare.switching_ranges_with_orb(incl_obj.lon, obj_lon, obj_orb, deg, before_point_asp)
                if orb_con:
                    asp = type_asp
                    type_appr = AspectsPrepare.type_approach(incl_obj.lon, incl_obj.lonspeed, obj_lon, obj_lonsp, obj_house, deg)
                    orb_con = AspectsPrepare.degree_transform(orb_con)
                    sing = AspectsPrepare.equal_different_sing_feature(singles_degrees, incl_obj.lon, obj_lon, deg)
                else:
                    asp, type_appr, orb_con, sing = None, None, None, None

                point_aspects = {'f_point': id_obj, 's_point': incl_obj.id, 'type': asp, 'approach': type_appr, 'sing': sing, 'orb': orb_con}

                if point_aspects['type'] != None:
                    all_aspekts.append(point_aspects)

        return all_aspekts

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    