import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/')

from flatlib import aspects
from flatlib.tools import arabicparts
from flatlib.chart import Chart

moon_asc_aspect = aspects.getAspect(chart.get(const.MOON), chart.get(const.MARS), const.MAJOR_ASPECTS)
objects = charts.map(lambda x: arabicparts.getPart(getattr(arabicparts, name_of_object), x))
import swisseph as sw