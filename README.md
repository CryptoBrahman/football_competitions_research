# football_competitions_research
1) Install pacadges:

a) sudo apt-get install build-essential autoconf libtool pkg-config python-opengl 
python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools 
qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network 
libqt4-dbus python-qt4 python-qt4-gl libgle3 python3-dev

b) pip install pyswisseph
c) copy librares:
   pip freeze --path ~/.local/lib/python3.8/site-packages > ~/Documents/for_python_libraries/requirements.txt
   pip install --user -r ~/Documents/for_python_libraries/requirements.txt

2) changed some methods in library Lat_Lon for python 3.8
3) changed some methods in library flatlib:
a) in file charts.py on 48 string need to replace:
   #IDs = kwargs.get('IDs', const.LIST_OBJECTS_TRADITIONAL)
   IDs = kwargs.get('IDs', const.LIST_OBJECTS)
   for getting attributes of high planets
b) in file arabicparts.py changed 46 string:
   #[const.MOON, const.SUN, const.ASC]   # Nocturnal
   [const.SUN, const.MOON, const.ASC]
   for only Diurnal calculate position PARS_FORTUNA

) Copy libraries with changes in own directory.
"Lat_lon", "flatlib".

При расчетах аспектов учитывать фактор третьего объекта никак не обозначенного в 
карте.