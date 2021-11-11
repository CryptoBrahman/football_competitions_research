# football_competitions_research
1) Install pacadges:
a) sudo apt-get install python3.8-dev
b) pip install jupyter jupyterlab pyswisseph bs4 flatlib latlon3 pandas
   
2) changed some methods in library Lat_Lon for python 3.8 or replace library with changes
3) changed some methods in library flatlib:
a) in file charts.py on 48 string need to replace:
   #IDs = kwargs.get('IDs', const.LIST_OBJECTS_TRADITIONAL)
   IDs = kwargs.get('IDs', const.LIST_OBJECTS)
   for getting attributes of high planets
b) in file arabicparts.py changed 46 string:
   #[const.MOON, const.SUN, const.ASC]   # Nocturnal
   [const.SUN, const.MOON, const.ASC]
   for only Diurnal calculate position PARS_FORTUNA
c) Change orbs for planets in props.py.
4) 

При расчетах аспектов учитывать фактор третьего объекта никак не обозначенного в 
карте.