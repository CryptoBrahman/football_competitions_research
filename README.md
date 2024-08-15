# football_competitions_research
1) Install pacadges:
a) sudo apt-get install python3.9-dev
b) pip install jupyter jupyterlab pyswisseph bs4 pandas
    p.s. need instalation "pyswisseph" for flatlib module, no "swisseph". 

c) how pycharm add own modules:
    If your own module is in the same path, you need mark the path as Sources Root. In the project explorer, 
    right-click on the directory that you want import. Then select Mark Directory As and select Sources Root.

# Create new columns for each object, five clasess for favorite's advantsge and orbs's approuch  -----++++++
# Will change aspect's values from least to lagest and vice versa (1 - 5, 5 - 1) for ml alrorithm. ----------
# Find decision for rulers the opposite by values: ('ruler_asc'-'ruler_ic), ('ruler_dsc'-'ruler_mc) - for one planet. --------
# Change 'moon_conv_denide' aspect on 'moon_conv_compl' or 'moon_conv_compl_weak' for matches with time duration more than 100 min. -------
# Create 'all_asps', 'main_asps' and ' addition_asps' - columns. -------


1) Get list games by date and parsing every event for game by leagues, create two dataframes 'df_games' and 'df_events': - games_api_parser.ipynb 
2) Create 'df_comp_tabs_lgs' on during date for every league with team's statistic: - parsing_competition_tables.ipynb
3) Combine game, countries and teams cities at one dataframe, find teams without cities and add new data after manual fix: -concatinate_data_coef_pow.ipynb
4) Parsing new teams data(city, country) from soccer365: - parsing_teams_data.ipynb
5) Manual fixing new team data in csv file: - parsing_teams_data.ipynb
6) Add new team data(city, country) in 'df_teams_data : - teams_data.ipynb
7) Return in -concatinate_data_coef_pow.ipynb and add new team data
8) Parsing geolocation data with geocords, manual fix errors in cities, countries names and teams data. Add new unique citie's in coords df : -geolocation_data.ipynb
9) Calculate astrological aspects for each game: - astroaspects.ipynb
10) Concatinate and prepare files with aspects: - concatinate_prepare_aspect_files.ipynb 
11) Aspects statistic research, fix some errors in moons orbs, get features importance, create df for other ml servers: - statistic_research.ipynb

.)
games_api_parser.ipynb           - data parsing by days from 'soccer365.me/ru' cite and create df 
                          
.)
parsing_competition_tables.ipynb - parsed statistic tables with country's competitions by years from cite 'soccer365.me/ru'.
                                   create df['team_name','pos','pld','w','d','l','gf','ga','+/-','pts','comp_id','season_id'] 
                                   and parsing countries names by ids.
.)
concatinate_data_fav_pre.ipynb -   concatinate all dataframes with games, events, season results tables and cities statistic.
                                   create df_top_ligues: 74706 rows, df_second_ligues: 125237 rows, from 'pickle_files/all_matches': 
                                   df['game_id', 'ligue_header', 'comp_id', 'season_id', 'game_utc', 'game_title','goals', 'game_status'].
.)
parsing_teams_data.ipynb          - script for teams ids parsing and geting info 'city', 'country' and work after manual correcting.
.)
geolocation_data.ipynb            - create 'df_world_cities' with lat, lon cordinate and geopy.geocoders library.
                                    df['country','city','latitude','longitude','lat','lon']
.) 
astroaspects.ipynb                - for getting games aspects submit: df[game_id', 'time', 'lon', 'long'] columns.

  
.)
code_examples.ipynb              - python code examles.
.)
astro_constants.py               - class methods for geting astro aspects.
.)
html_parser.py                   - class methods for site parsing.
.)
teams_data.ipynb                 - create dataframe: df_teams_data['teams', 'countries', 'cities'] columns and add following data.
                                   1918 - rows and change different no 'utf-8' symbols.
.)
statistic_research.ipynb         - file for aspect's statistic research

.)
old_files/astrological_data.ipynb - code examples from flatlib library.




