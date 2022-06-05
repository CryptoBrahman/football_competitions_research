# football_competitions_research
1) Install pacadges:
a) sudo apt-get install python3.9-dev
b) pip install jupyter jupyterlab pyswisseph bs4 flatlib latlon3 pandas
       p.s. no "swisseph" - need instalation "pyswisseph" for flatlib module
2) changed some methods in library Lat_Lon for python 3.9 or replace library with changes
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
  Pycharm add own modules:
    If your own module is in the same path, you need mark the path as Sources Root. In the project explorer, 
    right-click on the directory that you want import. Then select Mark Directory As and select Sources Root.

# Create all country's competitions tables file from parsing_competition_tables.ipynb  --------
# Create new columns for each object, five clasess for favorite's advantsge and orbs's approuch  -----++++++
# Will change aspect's values from least to lagest and vice versa (1 - 5, 5 - 1) for ml alrorithm. ----------
# Find decision for rulers the opposite by values: ('ruler_asc'-'ruler_ic), ('ruler_dsc'-'ruler_mc) - for one planet. --------
# Change 'moon_conv_denide' aspect on 'moon_conv_compl' or 'moon_conv_compl_weak' for matches with time duration more than 100 min. -------
# Create 'all_asps', 'main_asps' and ' addition_asps' - columns. -------
# Create features for favorit and pretendent -------


.)
games_api_parser.ipynb           - data parsing by days from 'soccer365.me/ru' cite and create df, find games events with bets coefficients and create: 
                                   df['event_mins', 'event_hts_ats', 'stats_dict', 'city_country', 'viewers', 'weath_temp', 'bets']  
.)
parsing_competition_tables.ipynb - parsed statistic tables with country's competitions by years from cite 'soccer365.me/ru'.
                                   create df['team_name','pos','pld','w','d','l','gf','ga','+/-','pts','comp_id','season_id']         
.)
concatinate_all_data.ipynb.ipynb - concatinate all dataframes with games, events, season results tables and cities statistic.
                                   create df_top_ligues: 74706 rows, df_second_ligues: 125237 rows, from 'pickle_files/all_matches': 
                                   df['game_id', 'ligue_header', 'comp_id', 'season_id', 'game_utc', 'game_title','goals', 'game_status'].
.)
games_statistic.ipynb            - concatenate some files from df: 'all_matches' with df: 'events'.
.)
parsing_teams_ids.ipynb          - script for teams ids parsing and geting info 'city', 'country'.
.)
geolocation_data.ipynb           - create 'df_world_cities' with lat, lon cordinate and geopy.geocoders library.
                                   df['country','city','latitude','longitude','lat','lon']
.) 
astroaspects.ipynb               - for getting games aspects submit: df[game_id', 'time', 'lon', 'long'] columns.

  
.)
code_examples.ipynb              - python code examles.
.)
astro_constants.py               - class methods for geting astro aspects.
.)
html_parser.py                   - class methods for site parsing.
.)
teams_data.ipynb                 - create dataframe: df_teams_data['teams', 'countries', 'cities'] columns, 
                                   1918 - rows and change different no 'utf-8' symbols.


.)
old_files/astrological_data.ipynb - code examples from flatlib library.




