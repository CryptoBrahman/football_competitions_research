from flatlib import aspects
from flatlib.tools import arabicparts


moon_asc_aspect = aspects.getAspect(chart.get(const.MOON), chart.get(const.MARS), const.MAJOR_ASPECTS)
print('moon_asc_aspect: ', moon_asc_aspect)

moon_asps = dyn.immediateAspects(const.MOON, const.MAJOR_ASPECTS)

asc.orb

GenericList.get(self, ID)