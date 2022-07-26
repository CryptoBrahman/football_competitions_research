import sys
sys.path.append('/home/cryptobrahman/Own/football_competitions_research/own_modules/') 
sys.path.append('/mnt/KINGSTON_120/Own/football_competitions_research/own_modules/')

import re
import pickle
import time
import requests
import datetime
import unicodedata
import pandas as pd

from bs4 import BeautifulSoup
from Lat_lon.lat_lon import LatLon, Latitude, Longitude

from  geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Your_Name")


class TableConstant:
    
    top_ligues    = ['12', '13', '14', '15', '16', '17', '18', '419', '420', '454', '456', '474', '483', '485', '550', '554', '560', 
                     '565', '577', '581', '587', '591', '596', '601', '677', '681', '684', '695', '699', '707', '712', '716', '723', '727']
    
    second_ligues = ['419', '424', '435', '436', '437', '444', '446', '449', '450', '457', '459', '464', '473', '477', '491',
                     '493', '496', '498', '500', '502', '504', '507', '512', '516', '518', '523', '532', '539', '540', '542',
                     '544', '545', '546', '548', '551', '555', '562', '567', '576', '585', '586', '589', '595', '599', '602',
                     '606', '621', '622', '625', '626', '628', '632', '634', '636', '637', '642', '646', '647', '648', '653',
                     '654', '655', '657', '659', '660', '667', '672', '674', '675', '676', '679', '685', '687', '691', '692', '697',
                     '700', '703', '704', '714', '715', '720', '721', '725', '727', '733', '735', '747', '761', '912', '1157', '1259'] 



class ParsingDataPrepare:
    
    @staticmethod
    def str_utf_decode(str_obj: str):
        normalized = unicodedata.normalize('NFD', str_obj)
        decode_str = u"".join([c for c in normalized if not unicodedata.combining(c)])
        return decode_str

    @staticmethod
    # number of col_names in list must be equal number of rows df
    def transform_columns_to_rows(df: pd.DataFrame, col_names: list):
        pd_series = pd.DataFrame()
        for i, col in zip(range(df.shape[0]), col_names):
            pd_series[col] = df.stack()[i]
        
        return pd_series
    
    @staticmethod
    # Lat - lon format for  aspects: 'lon':'38n32', '14s42'], 'lat':'8w54', '18e14'.
    # df with 'latitude' and 'longitude' columns
    def lat_lon_calculate(df: pd.DataFrame, col_lat: str, col_lon: str):
        all_lat, all_lon = [], []

        df.reset_index(drop=True, inplace=True)
        df.latitude = pd.to_numeric(df.latitude)
        df.longitude = pd.to_numeric(df.longitude)

        for ind in range(df.shape[0]):
            lat_lon = LatLon(Latitude(df[col_lat][ind]), Longitude(df[col_lon][ind]))
            cords = lat_lon.to_string('d%%H%m%')
            lower_cords = [x.lower() for x in cords]

            all_lat.append(lower_cords[0])
            all_lon.append(lower_cords[1])

        return all_lat, all_lon
    
    @staticmethod
    def find_no_utf_symbols(sr: pd.Series):
        find_symols = r'[^.a-zA-Z0-9)(&"\s>;<=,-/}{\']'
        rare_symbols = sr.map(lambda x: '-'.join(re.findall(find_symols, str(x))))
        rare_symbols = ['-'.join(set(x.split('-'))) for x in list(set(rare_symbols))]
        rare_symbols = [x.split('-') for x in rare_symbols]

        all_symbs = []
        for symbols in rare_symbols:
            for symb in symbols:
                if symb != '':
                    all_symbs.append(symb)
        list_symbols = list(set(all_symbs))

        return list_symbols

    @staticmethod
    # dict_obj = {'Ö': 'O', 'ô':'o', 'Þ':'p'}
    def replace_rare_symbols(df: pd.DataFrame, col_name: str, dict_obj: dict):
        for k, v in dict_obj.items():
            df[col_name] = df[col_name].map(lambda x: x.replace(k, v) if re.search(k, str(x)) else x)

        return df[col_name] 
    
    @staticmethod
    def remove_rare_symbols(sr: pd.Series, rare_symbols: list):
        for symb in rare_symbols:
            sr = sr.map(lambda x: x.replace(symb, '') if symb in str(x) else x)
        return sr 

    @staticmethod
    def create_df_comp_tables(tables_list: list):
        df = pd.DataFrame()

        for x in range(0, len(tables_list)):
            for y in range(0, len(tables_list[x])):
                comp_id = tables_list[x][y]['comp_id']
                season_id = tables_list[x][y]['season_id'] 
                table = tables_list[x][y]['table']

                all_data = dict()
                for team_name, v_tab in table.items():
                    data = pd.DataFrame({
                         'team_name' : [team_name[0]],
                         'team_id'   : [team_name[1]],
                         'pos'       : [v_tab['Pos']],
                         'pld'       : [v_tab['Pld']],
                         'w'         : [v_tab['W']],
                         'd'         : [v_tab['D']],
                         'l'         : [v_tab['L']],
                         'gf'        : [v_tab['GF']],
                         'ga'        : [v_tab['GA']],
                         '+/-'       : [v_tab['+/-']],
                         'pts'       : [v_tab['Pts']],
                         'comp_id'   : [comp_id],
                         'season_id' : [season_id]
                        })
                    df = pd.concat([df, data])
        df = df.reset_index(drop=True)   

        return df

    @staticmethod
    def competition_season_ids(df: pd.DataFrame, col_comp='comp_id', col_season='season_id'):
        comp_seasons = df.groupby(col_comp)[col_season].agg(lambda x: x.unique().tolist())
        comp_seasons = comp_seasons.to_dict()
        for key, value in comp_seasons.items():
            comp_seasons[key] = [x for x in value if re.search(r'[0-9]+', str(x))]

        return comp_seasons
    
    @staticmethod
    # '8/18/2008' - str date format
    def count_days_by_dates(start_date: str, end_date: str):
        date_format = "%m/%d/%Y"
        a = datetime.datetime.strptime(start_date, date_format)
        b = datetime.datetime.strptime(end_date, date_format)
        delta = b - a
        numdays = abs(delta.days)

        return numdays
 
    @staticmethod
    def get_minvalue_ind(inputlist: list):
        min_value = min(inputlist) 
        min_index=inputlist.index(min_value)

        return min_index

    @staticmethod
    # For 'bets' and 'pos' coefs use 'min' method, for 'pts' - 'max' method.
    def roles_determinate(inputlist, power_coef: float, method: str):
        if method != 'min' and method != 'max':
            print("Unsuported value in sinlge('min','max')")

        if None in inputlist:
            return None

        if method == 'min':
            roles_dict = {0:'Fav', 1:'Pre'}   
        if method == 'max':
            roles_dict = {0:'Pre', 1:'Fav'}

        if power_coef * inputlist[ParsingDataPrepare.get_minvalue_ind(inputlist)] < inputlist[~ParsingDataPrepare.get_minvalue_ind(inputlist)]:
                return roles_dict[ParsingDataPrepare.get_minvalue_ind(inputlist)]
        else: 
            return 'Neu'

class HtmlParser:
    
    @staticmethod
    def transform_date(list_obj: list):
        now = datetime.datetime.now()
        dates = []
        for obj in list_obj:
            if len(obj) == 16:
                date = obj
            elif len(obj) == 17:
                date = re.sub(',', '', obj)   
            elif re.search(r'[a-zA-Z]', obj):
                date = ''.join(re.findall(r'[a-zA-Z]+', obj))
            elif (len(obj) == 12) & (re.search(r'[a-zA-Z]', obj) is None):
                date = obj.replace(',', '.' + str(now.year))
            else: 
                date = obj[:6] + str(now.year)[:2] + obj[6:8] + obj[9:15]
            dates.append(date)
        
        return dates
    
    @staticmethod
    def double_slice_list(list_obj: list, septener: str):
        k = 2
        even = list_obj[k-1::k]
        odd = list_obj[k-2::k]
        all_res = []
        for x, y in zip(odd, even):
            res = x + septener + y
            all_res.append(res)
        
        return all_res
    
    @staticmethod
    def cut_part_of_string(str_obj: str, start_board: str, end_board: str):
        reg_str =  start_board +'(.*?)' + end_board 
        return re.findall(reg_str, str_obj)
    
    @staticmethod
    def scrape_html(str_url: str): 
        html = requests.get(str_url).content
        soup = BeautifulSoup(html, "html.parser")

        all_matches_db = {}
        for each_tb in soup.find_all('div', {'class': 'live_comptt_bd'}):
            ligue_header = each_tb.find('div', {'class': 'block_header'}).get_text()
            ligue_header = ''.join(re.findall(r'\n (.*?)\n', ligue_header))  
            ligue_header =   'Friendly' if ligue_header == '' else ligue_header

            season_id = ''.join(HtmlParser.cut_part_of_string(str(each_tb),'season_id=', '\''))
            if (season_id == '') & (ligue_header != 'Friendly'):
                season_id = 'Cup' 
            elif ligue_header == 'Friendly': 
                season_id = 'Friendly'

            comp_id  = each_tb.get('id')[3:] 
            game_ids = [x.get('dt-id') for x in each_tb.find_all('a', {'class': 'game_link'})]

            game_titles = [x.get('title') for x in each_tb.find_all('a', {'class': 'game_link'})]

            game_times_utc = [x.get_text() for x in each_tb.find_all('span', {'class': 'size10'})] 
            game_times_utc = HtmlParser.transform_date(game_times_utc)

            game_statuses  = [x if re.search('[a-zA-Z]', str(x)) else 'Finished' for x in game_times_utc]
            game_times_utc = [x[:16] for x in game_times_utc if re.search(r'[a-zA-Z]?', str(x))]

            all_goals = [x.get_text() for x in each_tb.find_all('div', {'class': 'gls'})]
            all_goals = HtmlParser.double_slice_list(all_goals, ':')

            stages = [x.get_text() for x in each_tb.find_all('div', {'class': 'stage'})]

            matches = dict()
            for game_id, game_utc, game_title, goals, game_status in zip(game_ids, game_times_utc, game_titles, all_goals, game_statuses): 
                matches.update({game_id: [ligue_header, comp_id, season_id, game_utc, game_title, goals, game_status]})

            all_matches_db.update(matches)

        return all_matches_db
    
    @staticmethod
    # 7-11-2013 last day with bet's data on soccer365, 2697 - days before now
    def create_date_list(numdays: int, start_year: int, start_month: int, start_day: int):
        base = datetime.date(start_year, start_month, start_day)
        date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
        
        return date_list
    
    @staticmethod
    # function take url without date
    def parsing_write_by_date(numdays: int, start_year: int, start_month: int, start_day: int, file_name: str, 
                                                                start_url='https://soccer365.me/online/&date='):
        date_list = HtmlParser.create_date_list(numdays, start_year, start_month, start_day)
        all_matches_db = {}
        for date in date_list:
            print(date)
            main_url = start_url + str(date)
            matches_db = HtmlParser.scrape_html(main_url)
            all_matches_db.update(matches_db)
            time.sleep(3)
        
        all_matches = open(file_name, 'wb')
        pickle.dump(all_matches_db, all_matches)  
        all_matches.close()
        
        return print('Data is saved')
    
#     @staticmethod
#     # event_hts and event_ats - left-right position on site's page
#     def find_game_events(game_ids: list, url='https://soccer365.me/games/', name_saved_file='events_games'):
#         events_dict = {}
#         for game_id, count in zip(game_ids, range(len(game_ids))):
#             try:
#                 html = requests.get(url + game_id).content
#                 soup = BeautifulSoup(html, "html.parser")

#                 event_mins = [x.get_text() for x in soup.find_all('div', {'class':'event_min'})]
#                 event_mins = [HtmlParser.cut_part_of_string(str(x), '^', '\'') for x in event_mins]
#                 event_mins = [''.join(x) if x != [] else '+' for x in event_mins]
            
#                 event_hts = [x.find_all('div') for x in soup.find_all('div', {'class':'event_ht'})]
#                 event_hts = [HtmlParser.cut_part_of_string(str(x), 'icon live_', '\">') for x in event_hts]
#                 event_ats = [x.find('div') for x in soup.find_all('div', {'class':'event_at'})]
#                 event_ats = [HtmlParser.cut_part_of_string(str(x), 'icon live_', '\">') for x in event_ats]

#                 event_hts_ats = [y if x == [] else x for x, y in zip(event_hts, event_ats)]
#                 event_hts_ats = [''.join(x) for x in event_hts_ats]
                
#                 team_id_hts = soup.find('div', {'class':'live_game_ht'})
#                 team_id_hts = ''.join(HtmlParser.cut_part_of_string(str(team_id_hts), '/clubs/', '/\">'))
#                 team_id_ats = soup.find('div', {'class':'live_game_at'})
#                 team_id_ats = ''.join(HtmlParser.cut_part_of_string(str(team_id_ats), '/clubs/', '/\">'))
                
#                 teams_ids  = team_id_hts + ' - ' + team_id_ats
                
#                 stats_items = soup.find_all("div", {"class": "stats_item"})
#                 stats_dict = []
                
#                 for stats_item in stats_items:
#                     stats_title = stats_item.find("div", {"class": "stats_title"}).text
#                     stats_inf_1 = stats_item.find_all("div", {"class": "stats_inf"})[0].text
#                     stats_inf_2 = stats_item.find_all("div", {"class": "stats_inf"})[1].text
#                     stats_list  = stats_title, stats_inf_1, stats_inf_2
#                     stats_dict.append(stats_list)

#                 try:
#                     preview_items = soup.find_all('div', {'class':'preview_item'})
#                     city_country  = preview_items[0].find_all('span', {'class':'min_gray'})[0].text
#                 except (AttributeError, IndexError):   
#                     preview_items = city_country = ''

#                 try:
#                     prview_weath_tmp = preview_items[0].find('span', {'class':'prview_weath_tmp'}).text
#                     weather          = HtmlParser.cut_part_of_string(prview_weath_tmp, '^', '°')
#                     temp             = HtmlParser.cut_part_of_string(prview_weath_tmp, '\xa0\xa0', '$')
#                     weath_temp       = ''.join(weather), ''.join(temp)
#                 except (AttributeError, IndexError):
#                     prview_weath_tmp = weath_temp = ''

#                 try:
#                     viewers = HtmlParser.cut_part_of_string(preview_items[1].text, ':', '$')
#                     viewers = ''.join(viewers)
#                 except (AttributeError, IndexError):
#                     viewers = ''

#                 time.sleep(1.5)
#                 url_for_bets = url.replace('.me/', '.ru/')
#                 bets_html    = requests.get(url_for_bets + game_id).content
#                 bets_soup    = BeautifulSoup(bets_html, "html.parser")

#                 bet_titeles  = [x.get_text() for x in bets_soup.find_all('div', {'class':'odds_coeff_title'})]

#                 try:
#                     coeffs = [x.get_text() for x in bets_soup.find_all('div', {'class':'odds_coeff'})[:len(bet_titeles)]]
#                 except (AttributeError, IndexError):
#                     coeffs = ''

#                 bet_coeffs = bet_titeles, coeffs

#                 events = {game_id:[teams_ids, event_mins, event_hts_ats, stats_dict, city_country, viewers, weath_temp, bet_coeffs]}
#                 events_dict.update(events)

#                 if ((count % 500 == 0) & (count != 0)) | (game_id == game_ids[-1]):
#                     print('Current_500_games_events_saved - {}'.format(game_id))

#                     events_games = open('pickle_files/' + name_saved_file + '_' + game_id, 'wb')
#                     pickle.dump(events_dict, events_games)  
#                     events_games.close()
#                     time.sleep(6) # time.sleep(600)

#                 time.sleep(1.5)    
#             except ConnectionError:
#                 time.sleep(600)  
#                 HtmlParser.find_game_events(game_ids[count +1:], name_saved_file=name_saved_file)

#         return print('Data saved with last id: {}'.format(game_id))
    
    @staticmethod
    def find_teams_ids(tm_names: list, url='https://soccer365.me/?a=search&q=', name_saved_file='teams_ids_na_cities'):
        ids_teams = []
        
        for tm_name, count in zip(tm_names, range(len(tm_names))):
            try:
                name_wt_space = re.sub(' ', '+', tm_name)
                html = requests.get(url + name_wt_space).content
                soup = BeautifulSoup(html, "html.parser")
                
                if soup.find_all('span', {'class':'flag16'}):
                    span_find = [x for x in soup.find_all('span', {'class':'flag16'}) if re.sub('\n', '', x.get_text()) == tm_name]
                    
                    if span_find != []:
                        ids = [''.join(HtmlParser.cut_part_of_string(str(x), '/clubs/', '/"')) for x in span_find][0]               
                    else:
                        ids = None
                    ids_teams.append([tm_name, ids])
                else:
                    ids_teams.append([tm_name, None])
                    
                if ((count % 1000 == 0) & (count != 0)) | (tm_name == tm_names[-1]):  
                    print('Current_1000_teams_ids_saved - {}'.format(tm_name))

                    file = open('pickle_files/teams_data/' + name_saved_file + '_' + tm_name, 'wb')
                    pickle.dump(ids_teams, file)  
                    file.close()
                    time.sleep(20) 

            except ConnectionError:
                time.sleep(100)          
        return print('Teams ids saved with last name: {}'.format(tm_name))
    
    @staticmethod
    # If data not exist - return save team data beefore
    def find_teams_data(teams_ids: list, url='https://soccer365.me/clubs/', name_saved_file='teams_wiki_data'):
        teams_data = []
        
        for teams_id, count in zip(teams_ids, range(len(teams_ids))):
            try:
                html = requests.get(url + teams_id).content
                soup = BeautifulSoup(html, "html.parser")

                div_find = soup.find('div', {'class':'profile_wiki'})   
                cut_str   = ''.join(HtmlParser.cut_part_of_string(str(div_find), '_wiki">', '\xa0<a class='))
                
                teams_data.append((teams_id, cut_str))
                
                
                if ((count % 500 == 0) & (count != 0)) | (teams_id == teams_ids[-1]):
                    print('Current_500_teams_data_saved - {}'.format(teams_id))

                    list_teams_data = open('pickle_files/' + name_saved_file + '_' + teams_id, 'wb')
                    pickle.dump(teams_data, list_teams_data)  
                    list_teams_data.close()
                    time.sleep(100) 

                time.sleep(1.5)
                
            except ConnectionError:
                time.sleep(600)      
                HtmlParser.find_teams_data(teams_ids[count +1:], name_saved_file=name_saved_file)    
        
        return print('Teams data saved with last id: {}'.format(teams_id))
    
    @staticmethod
    # https://soccer365.me/?c=live&a=showtable&competition_id=1157&season_id=306
    def parsing_competition_tables(comps_dict: dict, start_url='https://soccer365.me/?c=live&a=showtable'):
        all_comps_seasons = list()
        for comp, seasons in comps_dict.items():

            all_seasons = list()
            for season in seasons:
                url = start_url + '&competition_id=' + comp + '&season_id=' + season
                html = requests.get(url).content
                soup = BeautifulSoup(html, "html.parser") 
                regular_seasons = [x for x in soup.find_all('table', {'class':'stngs'})]
                
                if regular_seasons != []:
                    print(comp, season)
                    tb_header = [x.get_text() for x in soup.find_all('th', {'class': 'ctr'})]

                    key_pos = ['Pos']
                    places = [x.get_text() for x in soup.find_all('div', {'class': 'plc'})]
                    place_num = [re.findall('[0-9]+', x) for x in places]
                    place_num = list(filter(None, place_num))
                    places_dict = [dict(zip(key_pos, x)) for x in place_num]

                    scores = [x.get_text() for x in soup.find_all('td', {'class': 'ctr'})]  
                    each_score = re.split(r'\\n\',', str(scores))
                    clear_each_sc = [re.findall(r'[0-9+-]+', x) for x in each_score]
                    score_dict = [dict(zip(tb_header, x)) for x in clear_each_sc]
                    _ = [x.update(y) for x, y in zip(score_dict, places_dict)]

                    teams_names     = [x.get_text() for x in soup.find_all('div', {'class': 'img16'})]
                    div_ids         = [x for x in soup.find_all('div', {'class': 'img16'})]
                    teams_ids       = [''.join(HtmlParser.cut_part_of_string(str(x), '/clubs/', '/" ')) for x in div_ids]
                    times_names_ids = zip(teams_names, teams_ids)
                    teams_score     = dict(zip(times_names_ids, score_dict))   
                    
                    comps_seasons = {'comp_id': comp, 'season_id': season}
                    comps_seasons['table'] = teams_score

                    all_seasons.append(comps_seasons)
            all_comps_seasons.append(all_seasons)

        return all_comps_seasons   
    
    @staticmethod
    def find_countries_names(comp_ids: list, url='https://soccer365.me/competitions/', name_saved_file='countries_names'):
        countries_names_ids = []

        for comp_id, count in zip(comp_ids, range(len(comp_ids))):
            try:
                html = requests.get(url + comp_id).content
                soup = BeautifulSoup(html, "html.parser")

                tab_find = soup.find('table', {'class':'profile_params'})
                
                if tab_find:
                    country_name = ''.join(HtmlParser.cut_part_of_string(str(tab_find.get_text()), 'Country', ' Date'))   
                else:
                    country_name = None
                
                dict_country = {'comp_id': comp_id, 'country_name': country_name}

                countries_names_ids.append(dict_country)

                if comp_id == comp_ids[-1]:  
                    print('All_countries_names_saved - {}'.format(comp_id))

                    file = open('pickle_files/' + name_saved_file + '_' + comp_id, 'wb')
                    pickle.dump(countries_names_ids, file)  
                    file.close() 

            except ConnectionError:
                time.sleep(100)       

        return print('All countries names saved with last id: {}'.format(comp_id))

#    @staticmethod
    # cities_countries - list of tuples: ('Štip', 'FYR Macedonia')
    def cities_data_with_geocoordinates(cities_countries: list, name_saved_file='cities_data_26_05_2022'):
        cities_data = []

        for city_country, count in zip(cities_countries, range(len(cities_countries))):
            try:
                data = geolocator.geocode(city_country[0] +','+ city_country[1])
                cities_data.append([tuple(city_country), data])     
                    
                if ((count % 100 == 0) & (count != 0)) | (city_country == cities_countries[-1]):  
                    print('Cities_data_saved - {}'.format(city_country))

                    file = open('pickle_files/cities_countries/' + name_saved_file + '_' + str(city_country[0]) + '_' + str(city_country[1]), 'wb')
                    pickle.dump(cities_data, file)  
                    file.close() 
                
                time.sleep(2)

            except ConnectionError:
                time.sleep(3)       

        return print('All cities data saved with last names: {}'.format(city_country))






















