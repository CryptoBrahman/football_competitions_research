import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/') 

import pandas as pd
import pylunar
import re
from numpy import arange, isclose
from copy import deepcopy

from flatlib import const
from flatlib.tools import arabicparts
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.dignities import essential
from flatlib.object import GenericObject


class AstrologicalConstants:
    
    houses_objects      = ['asc', 'desc', 'mc', 'ic']
    
    houses              = ['Asc', 'IC', 'Desc', 'MC']
    
    rulers_constants    = ['ASC', 'DESC', 'MC', 'IC', 'PARS_FORTUNA']
    
    necessary_constants = ['SUN', 'MOON', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO', 'CHIRON', 'NORTH_NODE', 'SOUTH_NODE']

    main_objects        = ['moon', 'sun', 'saturn', 'uranus', 'neptune', 'pluto', 'chiron', 'north_node', 'south_node']
                           
    ruler_objects       = ['ruler_asc', 'ruler_desc', 'ruler_mc', 'ruler_ic', 'ruler_pars_fortuna', 
                           'ruler_pars_spirit', 'ruler_pars_glory', 'ruler_pars_crest', 'ruler_pars_rock']
    
    pars_objects        = ['pars_fortuna', 'pars_spirit', 'pars_glory', 'pars_crest', 'pars_rock']
    
    for_antes_objects   = ['moon', 'ruler_asc', 'ruler_desc', 'ruler_mc', 'ruler_ic', 'pars_fortuna', 'pars_spirit', 'uranus', 
                           'neptune', 'pluto', 'chiron', 'north_node', 'south_node', 'ruler_pars_fortuna', 'ruler_pars_spirit']
    
    pars_constants      = ['PARS_SPIRIT', 'PARS_GLORY', 'PARS_CREST', 'PARS_ROCK']
    
    active_planets      = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    
    singles_degrees     = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    
    aspekts_degrees     = {'Con':0, 'Sixt':60, 'Sque':90, 'Trin':120, 'Opp':180}

    parts               = ['Pars Fortuna', 'Antes Pars Fortuna', 'Pars Spirit', 'Antes Pars Spirit', 'Pars Glory', 'Pars Crest', 'Pars Rock']

    nakshatras          = {'Ashwini':(0, 13.33), 'Bharani':(13.33, 26.66), 'Krittika':(26.66, 39.99), 'Rohini':(39.99, 53.33), 'Mrigashirsha':(53.33, 66.66), 
                          'Ardra':(66.66, 79.99), 'Punarvasu':(79.99, 93.33), 'Pushya':(93.33, 106.66), 'Ashlesha':(106.66, 119.99), 'Magha':(119.99, 133.33), 
                          'Purva Phalguni':(133.33, 146.66), 'Uttara Phalguni':(146.66, 159.99), 'Hasta':(159.99, 173.33), 'Chitra':(173.33, 186.66), 
                          'Swati':(186.66, 199.99), 'Vishakha':(199.99, 213.33), 'Anuradha':(213.33, 226.66), 'Jyeshta':(226.66, 239.99), 'Mula':(239.99, 253.33), 
                          'Purva Ashadha':(253.33, 266.66),      
                          'Uttara Ashadha':(266.66, 276.66), 'Abhijit':(276.66, 280.88), 'Shravana':(280.88, 293.33), # 21-23 != 13.33
                          'Dhanistha':(293.33, 306.66), 'Shatabhisha':(306.66, 319.99), 'Purva Bhadrapada':(319.99, 333.33), 'Uttara Bhadrapada':(333.33, 346.66), 
                          'Revathi':(346.66, 360)} 
    
    
class MoonDaysCalculate:
    ''' Example lat - lon, datetime Y,M,D H,m,0
    mi = pylunar.MoonInfo((42, 21, 0), (-71, 3, 0))
    mi.update((2016, 8, 4, 1, 45, 0))
    int(mi.age()) '''

    @staticmethod
    def geocoords_transform(df: pd.DataFrame, col_coords: str):
        tr_num = df[col_coords].map(lambda x: (int(str(x).split('.')[0]), int(divmod(abs(x), 1)[1] * 0.6 * 100), 0))
        return tr_num

    @staticmethod
    def date_time_transform(df: pd.DataFrame, col_coords: str):
        date_splt = df[col_coords].map(lambda x: (pd.to_numeric(x[:10].split('.')[2]),
                                                  pd.to_numeric(x[:10].split('.')[1]),
                                                  pd.to_numeric(x[:10].split('.')[0]),
                                                  pd.to_numeric(x[11:16].split(':')[0]),
                                                  pd.to_numeric(x[11:16].split(':')[1]), 0))
        return date_splt

    @staticmethod
    # Tuple lat example: (42, 21, 0), date_time: (2016, 8, 4, 1, 45, 0)
    def moon_day_calculate(lat: tuple, lon: tuple, date_time: tuple):
        mi = pylunar.MoonInfo(lat, lon)
        mi.update(date_time)
        return int(mi.age())
    
    @staticmethod
    def calculate_moon_mansions(nakshatras: dict, lon: int) -> str:
        for key, val in nakshatras.items():
            if lon > val[0] and lon < val[1]:
                return key 
    
    @staticmethod     
    # minus sing "1w7" of lon and "8s10" of lat
    def transform_lat_lon_to_nimeric(x: str) -> float:
        a = re.split('[a-z]',str(x))[0]
        b = re.split('[a-z]',str(x))[1]
        if re.findall('w', str(x)) or re.findall('s', str(x)):
            val = str(-abs(int(a))) +'.'+ str(b)
        else:
            val =  str(a) +'.'+ str(b)
        return float(val) 


class AstrologicalPoints:
    
    @staticmethod
    def dates_posits_calculate(df: pd.DataFrame, date:str, utc_time:str, lat:str, lon:str):
        dates           = df.apply(lambda x: Datetime(x[date], x[utc_time], '+00:00'), axis=1)
        posits          = df.apply(lambda x: GeoPos(x[lat], x[lon]), axis=1)
        df_dates_posits = pd.concat([dates, posits], axis=1, keys=['dates', 'posits'])
        return df_dates_posits
    
    @staticmethod
    def charts_calculate(df_dates_posits: pd.DataFrame):
        charts = df_dates_posits.apply(lambda x: Chart(x['dates'], x['posits'], hsys=const.HOUSES_PLACIDUS), axis=1) 
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

    # 08_23
    # @staticmethod
    # def ruler_of_object(col_object: pd.Series):
    #     rulers_name = col_object.map(lambda x: essential.ruler(getattr(x, 'sign')))
    #     return rulers_name

    @staticmethod
    def ruler_of_object(col_object: pd.Series, sr_charts: pd.Series):
        rulers_name = map(lambda x: essential.ruler(getattr(x[1], 'sign')) \
                        if essential.ruler(getattr(x[1], 'sign')) != 'Moon' \
                        else essential.ruler(getattr(sr_charts[x[0]].get(const.MOON),'sign')), enumerate(col_object))

        return pd.Series(rulers_name)
    
    @staticmethod
    def chart_object_attributes(df: pd.DataFrame, col_charts: str, col_obj_names: str):
        object_attributes = df.apply(lambda x: x[col_charts].get(x[col_obj_names]), axis=1)
        return object_attributes

    @staticmethod
    def antes_objects_calc(df: pd.DataFrame, col_for_antes: str):
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
            if hasattr(obj, 'lonspeed') and obj.meanMotion() == 0:
                obj.lonspeed = 0
            all_objects.append(obj)
        self.unique_objs = all_objects
        return self.unique_objs
    
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
        objects_cp = objects.copy()
        
        for r_obj in remove_objs:
            for obj in objects:
                if obj.id == r_obj:
                    objects_cp.remove(obj) 
                    
        return  objects_cp           
    
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
    def transform_blocks_list_type(list_blocks: list):
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

        obj_lon_degs = AspectsPrepare.transform_blocks_list_type(obj_lon_degs)
        AspectsPrepare.remove_list_dubles(obj_lon_degs)
        
        return obj_lon_degs   
    
    @staticmethod
    def switching_ranges_with_orb(include_lon: float, obj_lon: float, obj_orb: int, deg: int, before_point_asp = 'no'):
        obj_lon_degs = AspectsPrepare.pos_neg_points_orb(obj_lon, obj_orb, deg, before_point_asp)
        
        for lon_degs in obj_lon_degs:
            if isclose(round(include_lon, 2), arange(round(lon_degs[0], 2), round(lon_degs[1], 2), 0.01)).any():
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
    def left_right_semi_circle(incl_lon: float, obj_lon: float, obj_orb: int, deg: int, before_point_asp='no'):
        obj_lon_degs = AspectsPrepare.pos_neg_points_orb(obj_lon, obj_orb, deg, before_point_asp)
        all_incl_lon = []
        
        for obj_ld in obj_lon_degs:
            if isclose(round(incl_lon, 2), arange(round(obj_ld[0], 2), round(obj_ld[1], 2), 0.01)).any() and before_point_asp == 'no':
                all_incl_lon.append(1)
            else:
                all_incl_lon.append(0)
            
            if 1 in all_incl_lon:
                incl_lon_pos = 'right'
            else:
                incl_lon_pos = 'left'
            
        return incl_lon_pos 
    
    @staticmethod
    def type_approach(incl_lon: float, incl_lonsp: float, obj_lon: float, obj_lonsp: float, obj_orb: int, obj_house: int, deg: int, before_point_asp='no'):    
        incl_lon_pos = AspectsPrepare.left_right_semi_circle(incl_lon, obj_lon, obj_orb, deg, before_point_asp) 
        
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
        
        unique_objs = AspectsPrepare.remove_objects(unique_objs, remove_objs)
        objects = unique_objs.copy()
        list_ids = [x.id for x in unique_objs]
    
        if id_obj in list_ids:
        
            obj_id, obj_lon, obj_orb, obj_lonsp, obj_house = AspectsPrepare.object_data(objects, id_obj)
            obj_orb = AspectsPrepare.type_orb_calculate(obj_orb, before_point_asp, after_orb, before_orb)
            objects = AspectsPrepare.remove_objects(objects, [obj_id])
            
            for incl_obj in objects:
                for type_asp, deg in aspekts_degrees.items():
                    orb = AspectsPrepare.switching_ranges_with_orb(incl_obj.lon, obj_lon, obj_orb, deg, before_point_asp)
                    if orb:
                        asp = type_asp
                        type_appr = AspectsPrepare.type_approach(incl_obj.lon, incl_obj.lonspeed, obj_lon, obj_lonsp, obj_orb, obj_house, deg, before_point_asp)
                        tr_orb = AspectsPrepare.degree_transform(orb)
                        sing = AspectsPrepare.equal_different_sing_feature(singles_degrees, incl_obj.lon, obj_lon, deg)
                    else:
                        asp, type_appr, tr_orb, sing = None, None, None, None
                    
                    point_aspects = {'f_point': id_obj, 's_point': incl_obj.id, 'type': asp, 'approach': type_appr, 'sing': sing, 'orb': orb, 'tr_orb': tr_orb, 
                                     'longs': [round(obj_lon, 2), round(incl_obj.lon, 2)], 'bp_asp': before_point_asp}

                    if point_aspects['type'] != None:
                        all_aspekts.append(point_aspects)
                        
            return all_aspekts

    @staticmethod
    def transform_dict_list_type(list_dicts: list):
        list_dicts_cp = deepcopy(list_dicts)
        all_dict = []
        
        for var in list_dicts_cp:
            if var != [] and var != None:
                while len(var) != 0:
                    x = var.pop()
                    all_dict.append(x)    
        
        return all_dict
    
    @staticmethod
    # The Moon can't be ruler
    def find_rulers_and_pars(tuple_list: list):
        rulers_dict = dict()

        for var in tuple_list:
            var_list = var[0].split('_&_')
            for obj in var_list:
                if obj.startswith('ruler_'):
                    rulers_dict[obj] = var[1]

        list_objs = set(list(rulers_dict.values()))
        points = dict()
        all_ruler_points = dict()

        for obj in list_objs:
            if obj == 'Moon':
                continue
            incl_obj = []
            incl_part = []
            for key, val in rulers_dict.items():
                if obj == val:
                    incl_obj.append(key)
                    ch_key = key.replace('ruler_','').replace('_', ' ').title()
                    if ch_key in ['Ic', 'Mc']:
                        ch_key = ch_key.upper()
                    incl_part.append(ch_key)
                    points[obj] = (incl_obj, incl_part)
                    all_ruler_points.update(points)

        return all_ruler_points  
    
    @staticmethod
    def find_rulers_parses_aspects(list_aspects: list, tuple_list: list):
        rulers_dict = AspectsPrepare.find_rulers_and_pars(tuple_list)
        rulers_aspects = []

        for key, values in rulers_dict.items():

            for asp in list_aspects:
                if asp['f_point'] == key or asp['s_point'] == key:
                    for val in values[1]:
                        if asp['f_point'] == val or asp['s_point'] == val: 
                            rulers_aspects.append(asp)
                            # ind = values[1].index(val)
                            # asp['charact'] = values[0][ind]
                            # asp['all_characts'] = values[0]

        return rulers_aspects 
    
    @staticmethod
    def find_houses_rulers(tuple_list: list):
        houses = AstrologicalConstants.houses
        rulers = AspectsPrepare.find_rulers_and_pars(tuple_list)
    
        houses_ruls = []
        for key, val in rulers.items():
            if any(x in houses for x in val[1]):
                houses_ruls.append(key)
    
        return houses_ruls
    
    @staticmethod
    def find_other_long_in_range_long_orb(objects: object, f_point: str, f_point_lon: float, s_point: str, asp_orb: int, asp_type: str, asp_sing: str,
                                          before_point_asp = 'no'):
        objs_longs = [{'id': x.id, 'lon': x.lon} for x in objects]
        all_find = []
        all_ids = []

        for obj in objs_longs:
            if obj['id'] == f_point or obj['id'] == s_point:
                continue

            asp_deg = AstrologicalConstants.aspekts_degrees.get(asp_type)
            obj_lon_degs = AspectsPrepare.pos_neg_points_orb(f_point_lon, asp_orb, asp_deg, before_point_asp)

            if any(isclose(round(obj['lon'], 2), arange(round(x[0], 2), round(x[1], 2), 0.01)).any() for x in obj_lon_degs):
                all_find.append(1)
                all_ids.append(obj['id'])
            else:
                all_find.append(0)

        if 1 in all_find:
            return ['yes', all_ids]
        else:
            return ['no', all_ids]
    
    @staticmethod
    def find_moon_parts_conv_aspects(list_aspects: list):
        parts = AstrologicalConstants.parts
        all_moon_asps = []

        for asp in list_aspects:
            if asp['f_point'] == 'Moon' and asp['s_point'] in parts and asp['approach'] == 'conv' and asp['sing'] == 'equal':
                all_moon_asps.append(asp)

        return all_moon_asps
    
    @staticmethod
    def supplement_houses_and_parts_rulers_aspects(objects: object, list_aspects: list, tuple_list: list):
        find_asps = AspectsPrepare.find_rulers_parses_aspects(list_aspects, tuple_list)
        mp_aspects = AspectsPrepare.find_moon_parts_conv_aspects(list_aspects)
        houses_ids = AstrologicalConstants.houses

        for asp in find_asps:
            if asp['sing'] == 'diff':
                if asp['f_point'] in houses_ids:
                    approach = asp['approach'] + '_weak'
                else:
                    approach = asp['approach'] + '_denide'

                asp['approach'] = approach
                asp['den_point'] = ['diff_sing']
            else: 
                find_long = AspectsPrepare.find_other_long_in_range_long_orb(objects, asp['f_point'], asp['longs'][0], asp['s_point'], asp['orb'], 
                                                          asp['type'], asp['sing'], asp['bp_asp'])
                type_appr = asp['approach'].split('_')

                if any(asp['f_point'] == mp_asp['s_point'] or asp['s_point'] == mp_asp['s_point'] for mp_asp in mp_aspects) and \
                asp['f_point'] not in houses_ids:
                    for mp_aspect in mp_aspects:
                        if asp['f_point'] == mp_aspect['s_point'] or asp['s_point'] == mp_aspect['s_point']:
                            approach = asp['approach'] + '_denide'

                            asp['approach'] = approach
                            asp['den_point'] = ['Moon', [mp_aspect['type'], mp_aspect['tr_orb']]]

                elif 'conv' in type_appr: 
                    if find_long[0] == 'yes':
                        if asp['f_point'] in houses_ids:
                            approach = asp['approach'] + '_weak'
                        else:   
                            approach = asp['approach'] + '_denide'
                    else:   
                        approach = asp['approach'] + '_compl'

                    asp['approach'] = approach
                    asp['den_point'] = find_long[1]

                elif 'diver' in type_appr:
                    if asp['f_point'] in houses_ids:
                        approach = asp['approach'] + '_weak'
                    else:
                        if find_long[0] == 'yes':
                            approach = asp['approach'] + '_denide'
                        else:   
                            approach = asp['approach'] + '_weak'

                    asp['approach'] = approach
                    asp['den_point'] = find_long[1]      

    @staticmethod                
    def supplement_conv_stat_aspects(objects: object, list_aspects: list):
        characts = ['conv', 'stat', 'in_conv', 'in_stat', 'out_conv', 'out_stat', 'out_diver', 'in_diver']

        for asp in list_aspects:
            if asp['f_point'] == 'Moon':
                continue
            if asp['approach'] not in characts:
                continue

            if asp['sing'] == 'diff':
                if asp['approach'] in characts[2:]:
                    approach = asp['approach'] + '_weak'
                else: 
                    approach = asp['approach'] + '_denide'

                asp['approach'] = approach
                asp['den_point'] = ['diff_sing']
                continue 
            else:
                find_long = AspectsPrepare.find_other_long_in_range_long_orb(objects, asp['f_point'], asp['longs'][0], asp['s_point'], asp['orb'], 
                                                              asp['type'], asp['sing'], asp['bp_asp'])
                if find_long[0] == 'yes': 
                    approach = asp['approach'] + '_weak'

                    asp['approach'] = approach
                    asp['den_point'] = find_long[1]
                else:
                    continue
     
    @staticmethod
    def moon_unite_converge_aspects_orbs(list_aspects: list):   
        moon_asps = []

        for asp in list_aspects:
            if asp['f_point'] != 'Moon':
                continue    
            if asp['approach'] == 'conv': 
                var = [asp['s_point'], asp['type'], asp['orb']]
                moon_asps.append(var)

        return moon_asps
    
    @staticmethod
    # return list all points aspected 'Con' type and all types for active planets aspected beefore 
    def find_moon_other_longs_in_range_with_degs(objects: object, f_point: str, f_point_lon: float, s_point: str, asp_orb: int, asp_sing: str):
        main_points = AstrologicalConstants.active_planets + ['Pars Fortuna']
        antes_main_points = ['Antes '+ x for x in main_points]
        degs = AstrologicalConstants.aspekts_degrees.keys()
        all_find_longs = []

        for deg in degs:
            find_long = AspectsPrepare.find_other_long_in_range_long_orb(objects, f_point, f_point_lon, s_point, asp_orb, deg, asp_sing)
            if find_long[0] == 'yes':
                find_long[1].append(deg)
                all_find_longs.append(find_long[1])

        den_points = []
        for var in all_find_longs:
            if var[-1:] == ['Con']:
                var.pop()
                while len(var) > 0:
                    den_points.append(var.pop())
            else:
                var.pop()
                for v in var:
                    if v in main_points + antes_main_points:
                        den_points.append(v)

        return den_points 
    
    @staticmethod
    def supplement_moon_complete_denide_weak_aspects(objects: object, list_aspects: list, tuple_list: list):
        houses_ruls = AspectsPrepare.find_houses_rulers(tuple_list)
        antes_hruls = ['Antes '+ rul for rul in houses_ruls] 
        parses      = ['Pars Fortuna', 'Antes Pars Fortuna']

        for asp in list_aspects:
            if asp['f_point'] != 'Moon':
                continue
            if asp['sing'] == 'diff':
                approach = 'moon_'+ asp['approach'] +'_denide'

                asp['approach'] = approach
                asp['den_point'] = ['diff_sing']

            if asp['tr_orb'] > 5.1:
                approach = 'moon_'+ asp['approach'] +'_denide'

                asp['approach'] = approach
                asp['den_point'] = ['more_orb']

            if asp['approach'] == 'diver':
                find_long = AspectsPrepare.find_other_long_in_range_long_orb(objects, asp['f_point'], asp['longs'][0], asp['s_point'], asp['orb'], 
                                                                             asp['type'], asp['sing'], asp['bp_asp'])
                if find_long[0] == 'yes':
                    approach = 'moon_'+ asp['approach'] +'_weak'

                    asp['approach'] = approach
                    asp['den_point'] = find_long[1]
                else:
                    approach = 'moon_'+ asp['approach']

                    asp['approach'] = approach
                    asp['den_point'] = find_long[1]

            if asp['approach'] == 'conv':
                moon_asps = AspectsPrepare.moon_unite_converge_aspects_orbs(list_aspects)

                if len(moon_asps) > 0:
                    moon_orbs        = [x[2] for x in moon_asps]
                    spoints          = [x[0] for x in moon_asps]
                    main_moon_orbs   = [x[2] for x in moon_asps if x[0] in houses_ruls + parses]
                    antes_house_orbs = [x[2] for x in moon_asps if x[0] in antes_hruls]

                if asp['s_point'] not in houses_ruls + antes_hruls + parses:
                    approach = 'moon_'+ asp['approach']
                    asp['approach'] = approach
                else:
                    spoints_cp = spoints.copy()
                    spoints_cp.remove(asp['s_point'])

                    if (asp['s_point'] in parses and all(asp['orb'] <= orb for orb in moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and asp['type'] == 'Con' and all(asp['orb'] <= orb for orb in moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and all(asp['orb'] <= orb for orb in moon_orbs) and all(x not in houses_ruls + parses for x in spoints_cp)):                   
                        approach = 'moon_'+ asp['approach']+ '_clear_compl'
                        asp['approach'] = approach

                    elif (asp['s_point'] in parses and all(asp['orb'] <= orb for orb in main_moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and asp['type'] == 'Con' and all(asp['orb'] <= orb for orb in main_moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and all(asp['orb'] <= orb for orb in main_moon_orbs) and \
                    all(sp not in houses_ruls + parses for sp in spoints_cp)): 
                        find_longs = AspectsPrepare.find_moon_other_longs_in_range_with_degs(objects, asp['f_point'], asp['longs'][0], asp['s_point'],
                                                                                             asp['orb'], asp['sing'])
                        approach = 'moon_'+ asp['approach']+ '_compl'
                        asp['approach'] = approach
                        asp['den_point'] = [find_longs, ['not_ruls']] 

                    elif (asp['s_point'] in parses and any(asp['orb'] > orb for orb in main_moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and asp['type'] == 'Con' and any(asp['orb'] > orb for orb in main_moon_orbs)) or \
                    (asp['s_point'] in houses_ruls and all(asp['orb'] >= orb for orb in main_moon_orbs) and \
                    any(sp in houses_ruls + parses for sp in spoints_cp)) or \
                    (asp['s_point'] in antes_hruls and all(asp['orb'] >= orb for orb in antes_house_orbs) and \
                    all(sp not in houses_ruls + parses for sp in spoints_cp)):
                        find_longs = AspectsPrepare.find_moon_other_longs_in_range_with_degs(objects, asp['f_point'], asp['longs'][0], asp['s_point'],
                                                                                             asp['orb'], asp['sing'])
                        approach = 'moon_'+ asp['approach']+ '_compl_weak'
                        asp['approach'] = approach

                        if asp['s_point'] in antes_hruls:
                            asp['den_point'] = [find_longs,['antes_ruls']]
                        else:    
                            asp['den_point'] = [find_longs,['with_ruls']] 

                    else:
                        approach = 'moon_'+ asp['approach'] 
                        asp['approach'] = approach

    @staticmethod
    def aspects_rulers_characteristic(tuple_list: list, list_aspects: list):
        main_rulers         = AstrologicalConstants.ruler_objects[:5]
        second_rulers       = AstrologicalConstants.ruler_objects[5:]
        antes_main_rulers   = ['antes_'+ x for x in main_rulers]
        antes_second_rulers = ['antes_'+ x for x in second_rulers]

        char_list = []
        for var in tuple_list:
            char = var[0].split('_&_')
            char.append(var[1])
            char_list.append(char)

        for asp in list_aspects:
            fmain_ch, fsec_ch, smain_ch, ssec_ch = [], [], [], []
            for var in char_list:
                if asp['f_point'] == ''.join(var[-1:]):
                    for v in var:
                        if v in main_rulers + antes_main_rulers:
                            fmain_ch.append(v)
                        elif v in second_rulers + antes_second_rulers:
                            fsec_ch.append(v)

                    asp['fmain_ch'] = fmain_ch
                    asp['fsec_ch']  = fsec_ch

                elif asp['s_point'] == ''.join(var[-1:]):
                    for v in var:
                        if v in main_rulers + antes_main_rulers:
                            smain_ch.append(v)
                        elif v in second_rulers + antes_second_rulers:
                            ssec_ch.append(v)

                    asp['smain_ch'] = smain_ch
                    asp['ssec_ch']  = ssec_ch
       
    @staticmethod
    def scale_orb_characteristic(list_aspects: list):
        for asp in list_aspects:
            if asp['f_point'] == 'Moon':
                continue
            if asp['tr_orb'] <= 0.2:
                asp['orb_char'] = 'max'
            elif asp['tr_orb'] > 0.2 and asp['tr_orb'] <= 1:
                asp['orb_char'] = 'mid_max'
            elif asp['tr_orb'] > 1 and asp['tr_orb'] <= 1.3:
                asp['orb_char'] = 'middle' 
            elif asp['tr_orb'] > 1.3 and asp['tr_orb'] <= 2:
                asp['orb_char'] = 'mid_min' 
            elif asp['tr_orb'] > 2:
                asp['orb_char'] = 'min' 
                        
    @staticmethod
    def moon_scale_orb_characteristic(list_aspects: list):
        for asp in list_aspects:
            if asp['f_point'] != 'Moon':
                continue
            if asp['tr_orb'] <= 0.3:
                asp['orb_char'] = 'max'
            elif asp['tr_orb'] > 0.3 and asp['tr_orb'] <= 1:
                asp['orb_char'] = 'mid_max'
            elif asp['tr_orb'] > 1 and asp['tr_orb'] <= 2.5:
                asp['orb_char'] = 'middle' 
            elif asp['tr_orb'] > 2.5 and asp['tr_orb'] <= 4:
                asp['orb_char'] = 'mid_min' 
            elif asp['tr_orb'] > 4:
                asp['orb_char'] = 'min' 
                
    
class AspectsClearing:
    
    @staticmethod
    def remove_duplicate_aspects(list_dicts: list):
        for val in list_dicts:
            if list_dicts.count(val) > 1:
                list_dicts.remove(val)

    @staticmethod
    # Save aspect with 'bp_asp':'no'
    def remove_equal_asp_besides_bp_asp(list_dicts: list):
        fs_points = [[val['f_point'], val['s_point']] for val in list_dicts]
        del_vals = []
        for i, point in enumerate(fs_points):
            if fs_points.count(point) > 1 and list_dicts[i]['bp_asp'] == 'yes':
                del_vals.append(list_dicts[i])
        for x in del_vals:
            list_dicts.remove(x)

    @staticmethod
    def remove_mirror_aspects(list_dicts: list):
        list_dicts_cp = list_dicts.copy()
        for val in list_dicts:
            for val_cp in list_dicts_cp:
                if val['f_point'] == val_cp['s_point'] and val_cp['f_point'] == val['s_point']:
                    list_dicts.remove(val_cp)

    @staticmethod
    # Only for natural points in list.
    def create_possibly_antes_aspects(list_points: list):
        possibly_asps = []
        for points in list_points:
            aspects = [[points[0], 'Antes '+ points[1]], ['Antes '+ points[1], points[0]],
                       ['Antes '+ points[0], points[1]], [points[1], 'Antes '+ points[0]],
                       [points[0], 'Antes '+ points[0]], ['Antes '+ points[0], points[0]],
                       [points[1], 'Antes '+ points[1]], ['Antes '+ points[1], points[1]],
                       ['Antes '+ points[0], 'Antes '+ points[1]], 
                       ['Antes '+ points[1], 'Antes '+ points[0]]]

            possibly_asps.append(aspects)

        all_possibly_asps = []
        for asp in possibly_asps:
            while len(asp) > 0:
                var = asp.pop()
                all_possibly_asps.append(var)

        return  all_possibly_asps
    
    @staticmethod 
    # Check example: 'Mercury.lon = 179, 'Antes Mercury'.lon = 358,  'Chirone.lon = 359, 'Antes Chirone'.lon = 180 - with five aspects's anteses 
    def remove_antes_unimportant_aspects(list_aspects: list):
        natural_asps = []

        for asp in list_aspects:
            if asp['f_point'] == 'Moon':
                continue
            if not asp['f_point'].startswith('Antes') and not asp['s_point'].startswith('Antes'):  
                natural_asps.append([asp['f_point'], asp['s_point']])

        nat_dict = AspectsClearing.create_possibly_antes_aspects(natural_asps)

        for asp in list_aspects[:]:   
            if [asp['f_point'], asp['s_point']] in nat_dict:
                list_aspects.remove(asp)
    
    @staticmethod
    def remove_node_opposition(list_dicts: list):
        list_dicts_cp = list_dicts.copy()
        node_list = ['North Node', 'South Node']

        for val in list_dicts[:]:
            for val_cp in list_dicts_cp:
                if (val['f_point'] in node_list or val['s_point'] in node_list) and \
                (val_cp['f_point'] in node_list or val_cp['s_point'] in node_list):
                    if val['f_point'] == val_cp['f_point'] and val['s_point'] == val_cp['s_point'] and val['type'] == 'Opp':
                        list_dicts.remove(val_cp)
    
    @staticmethod
    def remove_antes_with_own_nat_point_aspects(list_dicts: list):
        for val in list_dicts[:]:
            if val['f_point'] == 'Antes '+ val['s_point'] or 'Antes '+ val['f_point'] == val['s_point']:
                list_dicts.remove(val)
    
    @staticmethod
    # If natural points aspect don't exist. Save houses ruler's aspects.
    def remove_mirror_antes_aspects(list_aspects: list, tuple_list: list): 
        houses_ruls = AspectsPrepare.find_houses_rulers(tuple_list)

        cut_names = []
        for ind, asp in enumerate(list_aspects):
            if asp['f_point'] == 'Moon':
                continue
            if asp['f_point'].startswith('Antes'):    
                cut_names.append([ind, asp['f_point'].split('Antes ')[1], asp['s_point']])
            elif asp['s_point'].startswith('Antes'):    
                cut_names.append([ind, asp['f_point'], asp['s_point'].split('Antes ')[1]])

        cut_names_cp = cut_names.copy()
        find_asps = []

        for names in cut_names[:]:
            cut_names_cp.remove(names)
            for names_cp in cut_names_cp:
                if names[1] == names_cp[1] and names[2] == names_cp[2] or \
                names[1] == names_cp[2] and names[2] == names_cp[1]:
                    find_asps.append([list_aspects[names[0]], list_aspects[names_cp[0]]])        

        for f_asp in find_asps:
            if (f_asp[0]['f_point'] in houses_ruls or f_asp[0]['s_point'] in houses_ruls) and \
            (f_asp[1]['f_point'] in houses_ruls or f_asp[1]['s_point'] in houses_ruls):
                list_aspects.remove(f_asp[0])
            elif (f_asp[0]['f_point'] in houses_ruls or f_asp[0]['s_point'] in houses_ruls) and \
            (f_asp[1]['f_point'] not in houses_ruls or f_asp[1]['s_point'] not in houses_ruls):
                list_aspects.remove(f_asp[1])
            elif (f_asp[1]['f_point'] in houses_ruls or f_asp[1]['s_point'] in houses_ruls) and \
            (f_asp[0]['f_point'] not in houses_ruls or f_asp[0]['s_point'] not in houses_ruls):
                list_aspects.remove(f_asp[0])   
            else:
                list_aspects.remove(f_asp[0])
    
    @staticmethod
    def remove_mirror_houses_antes_conuction(list_aspects: list): 
        houses = AstrologicalConstants.houses

        list_aspects_cp = list_aspects.copy()
        for asp in list_aspects[:]:
            if asp['f_point'] not in houses:
                continue
            for asp_cp in list_aspects_cp:
                if asp_cp['f_point'] not in houses:
                    continue
                if (asp['f_point'] in ['Asc', 'Desc'] and not asp['s_point'].startswith('Antes')) and \
                (asp_cp['f_point'] in ['Asc', 'Desc'] and 'Antes '+ asp['s_point'] == asp_cp['s_point']):
                    list_aspects.remove(asp_cp)
                elif (asp['f_point'] in ['IC', 'MC'] and not asp['s_point'].startswith('Antes')) and \
                (asp_cp['f_point'] in ['IC', 'MC'] and 'Antes '+ asp['s_point'] == asp_cp['s_point']):
                    list_aspects.remove(asp_cp)
    
    @staticmethod
    def remove_houses_one_nodes_conuction(list_aspects: list): 
        houses = AstrologicalConstants.houses
        node_list = ['North Node', 'South Node']

        node_asps = []
        list_aspects_cp = list_aspects.copy()
        for asp in list_aspects:
            if asp['f_point'] not in houses:
                continue
            if (asp['f_point'] in ['Asc', 'Desc'] and asp['s_point'] in node_list):
                node_asps.append(asp)
            elif (asp['f_point'] in ['IC', 'MC'] and asp['s_point'] in node_list):
                node_asps.append(asp)
        
        if node_asps:
            if all(n_asp['den_point'] == [] for n_asp in node_asps):
                list_aspects.remove(node_asps[0])
            elif all(n_asp['den_point'] != [] for n_asp in node_asps):
                list_aspects.remove(node_asps[0])   
            else:
                for n_asp in node_asps:
                    if n_asp['den_point'] != []:
                        list_aspects.remove(n_asp)
    
    
class AspectsCalculate:
    
    def aspects_calculate(df: pd.DataFrame, row_number: int):
        objects = ObjectsPrepare(df.iloc[row_number]).conbine_class_methods()
        tuple_list = df.transform_id[row_number]

        all_aspects = []

        houses_remove_objs = []
        moon_remove_objs   = ['Asc', 'Desc', 'MC', 'IC', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'North Node', 'South Node', 'Antes Moon','Antes Uranus', 
                              'Antes Neptune', 'Antes Pluto', 'Antes Chiron']
        main_remove_objs   = ['Asc', 'Desc', 'MC', 'IC', 'Moon', 'Antes Moon']
        houses_aspect_degs = {'Con': 0}
        main_aspect_degs   = {'Con': 0, 'Opp': 180}
        moon_aspect_degs   = AstrologicalConstants.aspekts_degrees
        house_ids          = AstrologicalConstants.houses

        house_objs, moon_objs, main_objs = objects.copy(),objects.copy(), objects.copy() 

        moon_asp_after  = AspectsPrepare.object_aspects('Moon', moon_objs, moon_remove_objs, moon_aspect_degs)
        moon_asp_before = AspectsPrepare.object_aspects('Moon', moon_objs, moon_remove_objs, moon_aspect_degs, before_point_asp='yes', before_orb=1)
        all_aspects.append(moon_asp_after)
        all_aspects.append(moon_asp_before)

        for h_obj in house_ids:
            house_asp_after  = AspectsPrepare.object_aspects(h_obj, house_objs, houses_remove_objs, houses_aspect_degs, before_point_asp='no', after_orb=3)
            house_asp_before = AspectsPrepare.object_aspects(h_obj, house_objs, houses_remove_objs, houses_aspect_degs, before_point_asp='yes', before_orb=3)
            all_aspects.append(house_asp_after)
            all_aspects.append(house_asp_before)

        for m_obj in objects:
            main_asp_after  = AspectsPrepare.object_aspects(m_obj.id, main_objs, main_remove_objs, main_aspect_degs, before_point_asp='no', after_orb=3)
            main_asp_before = AspectsPrepare.object_aspects(m_obj.id, main_objs, main_remove_objs, main_aspect_degs, before_point_asp='yes', before_orb=3)
            all_aspects.append(main_asp_after)
            all_aspects.append(main_asp_before)

        for asp in all_aspects:
            if asp != None and any(var['f_point'] == 'Asc' and var['s_point'] == 'Pluto' for var in asp):
                asc_pluto = asp
            else:  
                asc_pluto = []

        if asc_pluto == []:
            for obj in objects:
                if obj.id == 'Asc' or obj.id == 'Pluto':
                    asc_pluto.append(obj) 

            asc_pluto_asp_after  = AspectsPrepare.object_aspects('Asc', asc_pluto, houses_remove_objs, houses_aspect_degs, before_point_asp='no', after_orb=10)
            asc_pluto_asp_before = AspectsPrepare.object_aspects('Asc', asc_pluto, houses_remove_objs, houses_aspect_degs, before_point_asp='yes', before_orb=10)
            all_aspects.append(asc_pluto_asp_after)
            all_aspects.append(asc_pluto_asp_before)

        all_aspects_full = AspectsPrepare.transform_dict_list_type(all_aspects)

        AspectsClearing.remove_duplicate_aspects(all_aspects_full)
        AspectsClearing.remove_equal_asp_besides_bp_asp(all_aspects_full)
        AspectsClearing.remove_mirror_aspects(all_aspects_full)
        AspectsClearing.remove_antes_unimportant_aspects(all_aspects_full)
        AspectsClearing.remove_node_opposition(all_aspects_full)
        AspectsClearing.remove_antes_with_own_nat_point_aspects(all_aspects_full)
        AspectsClearing.remove_mirror_antes_aspects(all_aspects_full, tuple_list)
        AspectsClearing.remove_mirror_houses_antes_conuction(all_aspects_full)

        for asp in all_aspects_full:
            asp['den_point'] = []

        AspectsPrepare.supplement_houses_and_parts_rulers_aspects(objects, all_aspects_full, tuple_list)
        AspectsPrepare.supplement_conv_stat_aspects(objects, all_aspects_full)
        AspectsPrepare.supplement_moon_complete_denide_weak_aspects(objects, all_aspects_full, tuple_list)
        AspectsPrepare.scale_orb_characteristic(all_aspects_full)
        AspectsPrepare.moon_scale_orb_characteristic(all_aspects_full)
        AspectsPrepare.aspects_rulers_characteristic(tuple_list, all_aspects_full)

        AspectsClearing.remove_houses_one_nodes_conuction(all_aspects_full)  

        return all_aspects_full
