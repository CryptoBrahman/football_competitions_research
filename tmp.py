import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/')

from flatlib import aspects
from flatlib import arabicparts
from flatlib.chart import Chart

moon_asc_aspect = aspects.getAspect(chart.get(const.MOON), chart.get(const.MARS), const.MAJOR_ASPECTS)

