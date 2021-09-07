from typing import List
from numpy import arange, isclose
import swisseph as swe
from flatlib import aspects
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.tools import arabicparts
from flatlib.protocols import behavior
from flatlib.tools.chartdynamics import ChartDynamics
from flatlib.ephem import ephem
from flatlib.dignities import essential

date = Datetime('2015/03/13', '17:00', '+00:00')
pos = GeoPos('38n32', '8w54')
chart = Chart(date, pos)
aspect = aspects.getAspect(sun, moon, const.MAJOR_ASPECTS)
parsSpirit = arabicparts.getPart(arabicparts.PARS_SPIRIT, chart)

factors = behavior.compute(chart)
for factor in factors:
    print(factor)

class AstrologicalPoints:
    degree_of_zodiac = {'Ari': 30, 'Tau': 60, 'Gem': 90, 'Cnc': 120, 'Leo': 150, 'Vir': 180,
                        'Lib': 210, 'Sco': 240, 'Sgr': 270, 'Cap': 300, 'Aqr': 330, 'Psc': 360
                        }
    points_del_keys_for_antes = ['Suz', 'Uuz', 'VAs', 'VDs', 'VMc', 'VIc', 'Asc', 'Dsc', 'Mcc', 'Icc']

    planets = ['Sun', 'Lun', 'Mer', 'Ven', 'Mar', 'Jup', 'Sat', 'Chi', 'Ura', 'Nep', 'Plu']

    dict_of_aspects = {'joint':0, 'sextile':60, 'square':90, 'trin':120, 'opposition':180}

    colors_of_zodiac = {'Ari': 'Light', 'Tau': 'Dark', 'Gem': 'Dark', 'Cnc': 'Light', 'Leo': 'Light', 'Vir': 'Dark',
                        'Lib': 'Dark', 'Sco': 'Light', 'Sgr': 'Light', 'Cap': 'Dark', 'Aqr': 'Dark', 'Psc': 'Light'}

    def __init__(self):
        self.points = {}
        self.points_for_antes = {}
        self.points_with_antes = {}
        self.aspects = {}
        self.aspects_with_zodiac = {}
        self.color_aspects_zodiac = {}

    def get_points(self):
        with open('/home/brahman/.wine/drive_c/ZET 9/Wrk/Pars.txt', "r", encoding='utf-8', errors='ignore') as file:
            arr_rows: List[str] = [row.strip() for row in file]
            arr_rows.remove(arr_rows[0])
        i = 0
        points = {}
        while i < (len(arr_rows)):
            key_for_row = (arr_rows[i][-3:])
            value_of_row = (arr_rows[i][-8:-5])
            float_from_row = (arr_rows[i][-17:-14])+'.'+(arr_rows[i][-14:-12])
            float_from_row = float(float_from_row)
            if value_of_row in AstrologicalPoints.degree_of_zodiac:
                float_from_row = round(float_from_row + int(AstrologicalPoints.degree_of_zodiac[value_of_row] - 30), 2)
            points[key_for_row] = float_from_row
            i = i + 1
        self.points = points
        return self.points

    def add_antes(self):
        points_for_antes = {}
        for key, value in self.points.items():
            if key not in AstrologicalPoints.points_del_keys_for_antes:
                antis_name = 'A' + key
                if isclose(value, arange(0, 180, 0.01)).any():
                    antis_value = round(180 - value, 2)
                else:
                    antis_value = round((360 - value) + 180, 2)
                points_for_antes.setdefault(antis_name, antis_value)
        self.points_for_antes = points_for_antes
        return self.points_for_antes

    def add_antes_in_points(self):
        points = self.points
        for key, value in self.points_for_antes.items():
            points.setdefault(key, value)
        self.points_with_antes = points
        return self.points_with_antes

    def get_aspects_for_planets(self, aspected_point, degree_of_proximity):
        aspects = {}
        value_aspected_point = aspected_point
        aspect_point = self.points.pop(aspected_point)
        for call_asp, degree in AstrologicalPoints.dict_of_aspects.items():
            for key, values in self.points.items():
                if isclose(values, arange(degree + aspect_point - degree_of_proximity,
                                          degree + aspect_point + degree_of_proximity, 0.01)).any():
                    proximity_of_aspect = round(values - (degree + aspect_point), 2)
                    call_asp = call_asp + '_with_' + value_aspected_point
                    list_asp = [call_asp, proximity_of_aspect]
                    aspects.setdefault(key,list_asp)
        self.aspects = aspects
        return self.aspects

    def get_zodiac_with_point(self):
        aspects_with_zodiac = {}
        for key_point, value_point in self.points.items():
            if key_point in set(self.aspects.keys()):
                for key_zodiac, value_zodiac in self.degree_of_zodiac.items():
                    if isclose(value_point, arange(0, value_zodiac, 0.01)).any():
                        aspects_with_zodiac.setdefault(key_point, key_zodiac)
        for key_pz, value_pz in aspects_with_zodiac.items():
            if self.aspects.get(key_pz):
                aspects_with_zodiac[key_pz] = [self.aspects[key_pz], value_pz]
        self.aspects_with_zodiac = aspects_with_zodiac
        return self.aspects_with_zodiac

    def get_color_for_zodiac(self):
        color_aspects_zodiac = {}
        for key, value in self.aspects_with_zodiac.items():
            for color_key, color_value in AstrologicalPoints.colors_of_zodiac.items():
                if value[1] == color_key:
                    value[1] = [value[1], color_value]
            color_aspects_zodiac.setdefault(key, value)
        print(color_aspects_zodiac)
        return self.color_aspects_zodiac


class_points = AstrologicalPoints()

get_points = class_points.get_points()
# antes_points = class_points.add_antes()
# points = class_points.add_antes_in_points()
get_aspects_fifth_house = class_points.get_aspects_for_planets('Sun', 2)
get_zodiac = class_points.get_zodiac_with_point()
get_color = class_points.get_color_for_zodiac()