from _astro_constants import AspectsPrepare


class StatDataPrepare:
    @staticmethod
    def fav_win_count(x):
        return round((x == 'fav_win').sum(), 2)

    @staticmethod
    def fav_loss_count(x):
        return round((x == 'fav_loss').sum(), 2)

    @staticmethod
    def fav_drow_count(x):
        return round((x == 'fav_drow').sum(), 2)

    @staticmethod
    def fav_drow_loss_count(x):
        fav_loss = (x == 'fav_loss').sum()
        fav_drow = (x == 'fav_drow').sum()
        return round(fav_loss + fav_drow, 2)

    @staticmethod
    def get_results(f_pow: str, f_goals: int, s_goals: int):
        if f_goals == s_goals:
            result = 'fav_drow'
        elif f_pow == 'Pre' and f_goals > s_goals:
            result = 'fav_loss'
        elif f_pow == 'Fav' and f_goals < s_goals:
            result = 'fav_loss'
        else:
            result = 'fav_win'
        return result

    @staticmethod
    # point: (f_point or s_point), charact:(fmain_ch or smain_ch)
    def change_main_characteristic_by_rules_for_saturn(point: str, charact: tuple):
        if 'ruler_asc' in charact:
            chg_charact = 'ruler_asc'
        elif 'antes_ruler_asc' in charact:
            chg_charact = 'antes_ruler_asc'

        elif 'ruler_desc' in charact:
            chg_charact = 'ruler_desc'
        elif 'antes_ruler_desc' in charact:
            chg_charact = 'antes_ruler_desc'
        else:
            chg_charact = None

        return chg_charact

    @staticmethod
    # point: (f_point or s_point), charact:(fmain_ch or smain_ch).
    def change_main_characteristic_by_rules(point: str, charact: tuple):
        if point == 'Moon' or point == 'Antes Moon':
            chg_charact = None
        elif point == 'Saturn' or point == 'Antes Saturn':
            chg_charact = StatDataPrepare.change_main_characteristic_by_rules_for_saturn(point, charact)
        else:
            if 'ruler_asc' in charact:
                chg_charact = 'ruler_asc'
            elif 'antes_ruler_asc' in charact:
                chg_charact = 'antes_ruler_asc'

            elif 'ruler_desc' in charact:
                chg_charact = 'ruler_desc'
            elif 'antes_ruler_desc' in charact:
                chg_charact = 'antes_ruler_desc'

            elif 'ruler_pars_fortuna' in charact:
                chg_charact = 'ruler_pars_fortuna'
            elif 'antes_ruler_pars_fortuna' in charact:
                chg_charact = 'antes_ruler_pars_fortuna'
            else:
                if len(charact) > 0:
                    chg_charact = charact[0]
                else:
                    chg_charact = None
        return chg_charact
    
    @staticmethod
    # point: (f_point or s_point), charact:(fsec_ch or ssec_ch).
    def change_sec_characteristic_by_rules(point: str, charact: tuple):
        if point == 'Moon' or point == 'Antes Moon':
            chg_charact = None
        elif point == 'Saturn' or point == 'Antes Saturn':
            chg_charact = None
        else:
            if len(charact) > 0:
                chg_charact = charact[0]
            else:
                chg_charact = None
        return chg_charact

    @staticmethod
    # point - it's transform degree orb
    def fix_erorr_aspects_values(point: float):
        if point < 30:
            return point
        else:
            x = point // 1
            y = point % 1 * 1.6
            point_tr = round(x + y, 2)
 
            fix_point = 0
    
            if point_tr > 230:
                fix_point = 240 - point_tr
            elif point_tr > 170 and point_tr < 230:
                fix_point = 180 - point_tr
            elif point_tr > 110 and point_tr < 170:
                fix_point = 120 - point_tr

            return AspectsPrepare.degree_transform(fix_point)  

    @staticmethod
    # 'f_pow' = 'host_role'
    def fav_win_bets_statistic_coeff(f_pow: str, result: str, first_coeff: float, sec_coeff: float):
        if f_pow == 'Fav' and result == 'fav_win':
            return first_coeff
        elif f_pow == 'Pre' and result == 'fav_win':
            return sec_coeff
        else:
            return 0

    @staticmethod
    def fav_loss_bets_statistic_coeff(f_pow: str, result: str, first_coeff: float, sec_coeff: float):
        if f_pow == 'Pre' and result == 'fav_loss':
            return first_coeff
        elif f_pow == 'Fav' and result == 'fav_loss':
            return sec_coeff
        else:
            return 0

    @staticmethod
    def fav_drow_bets_statistic_coeff(result: str, drow_coeff: float):
        if result == 'fav_drow':
            return drow_coeff
        else:
            return 0
    
    @staticmethod
    def fav_goals_calculate(host_role: str, goals: str):
        if host_role in ['Fav', 'Pre']:
            fav_goals  = int(goals.split(':')[0]) if host_role == 'Fav' else int(goals.split(':')[1])
            pre_goals  = int(goals.split(':')[0]) if host_role == 'Pre' else int(goals.split(':')[1])
            diff_goals = fav_goals - pre_goals
        else:    
            diff_goals = '-'
        return diff_goals     
    
    
    @staticmethod
    def diff_mean_stat_result(fav_win: int,	fav_drow: int, fav_loss: int, win_mean: float, drow_mean: float, loss_mean: float):
        sum_results = sum([fav_win, fav_drow, fav_loss])

        if fav_win != 0:
            diff_win = win_mean - sum_results/fav_win
        else:
            diff_win = 0  

        if fav_drow != 0:
            diff_drow = drow_mean - sum_results/fav_drow
        else:
            diff_drow = 0   

        if fav_loss != 0:
            diff_loss  = loss_mean  - sum_results/fav_loss
        else:
            diff_loss = 0     

        max_ind = [diff_win, diff_drow, diff_loss].index(max(diff_win, diff_drow, diff_loss))

        if max_ind == 0:
            return 'fav_win'
        elif max_ind == 1:
            return 'fav_drow'
        else:
            return 'fav_loss'
        

    @staticmethod
    def stat_result_win_more_drow_plus_loss(fav_win: int,  fav_drow: int, fav_loss: int):
        if int(fav_win) > (int(fav_drow) + int(fav_loss)):    
            return 'fav_win'
        elif int(fav_drow) > int(fav_loss):
            return 'fav_drow'
        else:
            return 'fav_loss'
        
        
    @staticmethod
    def stat_result_win_more_drow_or_loss(fav_win: int,  fav_drow: int, fav_loss: int):
        if int(fav_win) > int(fav_drow) and int(fav_win) > int(fav_loss):
            return 'fav_win'
        elif int(fav_drow) > int(fav_loss):
            return 'fav_drow'
        else:
            return 'fav_loss'

    
    @staticmethod
    def stat_result_win_more_drow_or_loss_without_drow(fav_win: int, fav_drow: int, fav_loss: int):
        if int(fav_win) > int(fav_drow) and int(fav_win) > int(fav_loss):
            return 'fav_win'
        else:
            return 'fav_loss'
    
    
    @staticmethod
    def stat_result_win_more_drow_plus_loss_without_drow(fav_win: int, fav_drow: int, fav_loss: int):
        if int(fav_win) > int(fav_drow) + int(fav_loss):
            return 'fav_win'
        else:
            return 'fav_loss'
    
    @staticmethod
    def stat_result_only_drow_or_win_and_drow_more_win_or_loss(fav_win: int, fav_drow: int, fav_loss: int):
        if int(fav_drow) > int(fav_win) and int(fav_drow) > int(fav_loss):
            return 'fav_drow'
        else:
            return 'fav_win_loss'
    
    
    @staticmethod
    def stat_result_only_drow_or_win_and_drow_more_win_plus_loss(fav_win: int, fav_drow: int, fav_loss: int):
        if int(fav_drow) > int(fav_win) + int(fav_loss):
            return 'fav_drow'
        else:
            return 'fav_win_loss'

    

    @staticmethod
    def fora_calculate(fora_for: str, bet: float, fora: float):
        if fora_for == 'For_Fav':
            if fora == -1.5:
                if bet <= 1.15:
                    return round(bet / 0.75, 2)
                elif bet <= 1.7:
                    return round(bet / 0.6, 2)
                elif bet <= 2.1:
                    return round(bet / 0.55, 2)
                elif bet > 2.1:
                    return round(bet / 0.4, 2)

            if fora == -1.25:
                if bet <= 1.42:
                    return round(bet / 0.74, 2)
                elif bet <= 1.9:
                    return round(bet / 0.64, 2)
                elif bet > 1.9:
                    return round(bet / 0.57, 2)  

            if fora == -1:
                if bet <= 1.7:
                    return round(bet / 0.8, 2)
                elif bet <= 1.9:
                    return round(bet / 0.7, 2)
                elif bet > 1.9:
                    return round(bet / 0.55, 2)   

            if fora == -0.75:
                if bet <= 1.42:
                    return round(bet / 0.94, 2)
                elif bet <= 1.9:
                    return round(bet / 0.87, 2)
                elif bet > 2.1:
                    return round(bet / 0.84, 2)      

            if fora == -0.25:
                if bet <= 1.07:
                    return 1
                if bet <= 1.18:
                    return round(bet / 1.07, 2)
                elif bet <= 1.42:
                    return round(bet / 1.09, 2)
                elif bet > 1.42:
                    return round(bet / 1.12, 2)    

            if fora == 0:
                if bet <= 1.1:
                    return 1
                if bet <= 1.15:
                    return round(bet / 1.1, 2)
                elif bet <= 2.1:
                    return round(bet / 1.2, 2)
                elif bet > 2.1:
                    return round(bet / 1.4, 2)    

            if fora == 0.25:
                if bet <= 1.25:
                    return 1
                elif bet <= 1.4:
                    return round(bet / 1.25, 2)
                elif bet <= 2.1:
                    return round(bet / 1.35, 2)   
                elif bet > 2.1:
                    return round(bet / 1.55, 2)

            if fora == 0.5:
                if bet <= 1.25:
                    return 1
                elif bet <= 1.4:
                    return round(bet / 1.25, 2)
                elif bet <= 1.7:
                    return round(bet / 1.35, 2)   
                elif bet <= 2.1:
                    return round(bet / 1.45, 2)
                elif bet > 2.1:
                    return round(bet / 1.8, 2)

            if fora == 0.75:
                if bet <= 1.3:
                    return 1
                elif bet <= 1.45:
                    return round(bet / 1.3, 2)
                elif bet <= 1.7:
                    return round(bet / 1.45, 2)   
                elif bet <= 1.9:
                    return round(bet / 1.55, 2)
                elif bet <= 2.1:
                    return round(bet / 1.75, 2)
                elif bet > 2.1:
                    return round(bet / 1.85, 2)

            if fora == 1:
                if bet <= 1.4:
                    return 1
                elif bet <= 1.55:
                    return round(bet / 1.4, 2)
                elif bet <= 1.7:
                    return round(bet / 1.55, 2)   
                elif bet <= 1.95:
                    return round(bet / 1.65, 2)
                elif bet <= 2.15:
                    return round(bet / 1.95, 2)
                elif bet > 2.15:
                    return round(bet / 2.15, 2)   
                
        # If fora coef don't exist then return only bets    
            if fora == 1.25:     
                return bet
            
            if fora == 1.5:     
                return bet

        if fora_for == 'For_Pre':
            if fora == -1.5:     
                return bet
            
            if fora == -1.25:     
                return bet
            
            if fora == -1:
                if bet <= 3.8:
                    return round(bet / 0.55, 2)
                elif bet <= 7.7:
                    return round(bet / 0.43, 2)
                elif bet > 7.7:
                    return round(bet / 1, 2)

            if fora == -0.75:
                if bet <= 3:
                    return round(bet / 0.83, 2)
                elif bet <= 7.7:
                    return round(bet / 0.71, 2)
                elif bet > 7.7:
                    return round(bet / 1, 2)    

            if fora == -0.25:
                if bet <= 3:
                    return round(bet / 1.14, 2)
                elif bet <= 12:
                    return round(bet / 1.08, 2)
                elif bet > 12:
                    return round(bet / 1, 2)     

            if fora == 0:
                if bet <= 3:
                    return round(bet / 1.19, 2)
                elif bet <= 12:
                    return round(bet / 1.28, 2)
                elif bet > 12:
                    return round(bet / 1.65, 2)

            if fora == 0.25:   
                if bet <= 6:
                    return round(bet / 1.6, 2)
                elif bet <= 12:
                    return round(bet / 1.85 , 2)
                elif bet > 12:
                    return round(bet / 2.3, 2)    

            if fora == 0.5:
                if bet <= 4:
                    return round(bet / 2, 2)
                elif bet <= 8:
                    return round(bet / 2.3, 2)
                elif bet <= 10:
                    return round(bet / 2.7, 2)
                elif bet > 10:
                    return round(bet / 3, 2)

            if fora == 0.75:   
                if bet <= 4:
                    return round(bet / 1.95, 2)
                elif bet <= 12:
                    return round(bet / 2.6, 2)
                elif bet <= 16:
                    return round(bet / 3, 2)     
                elif bet > 16:
                    return round(bet / 3.5, 2) 

            if fora == 1:   
                if bet <= 3.05:
                    return round(bet / 2.15, 2)
                elif bet <= 4:
                    return round(bet / 2.55, 2)
                elif bet <= 8:
                    return round(bet / 2.8, 2)
                elif bet <= 16:
                    return round(bet / 3.2, 2)     
                elif bet > 16:
                    return round(bet / 4.1, 2)      

            if fora == 1.25:   
                if bet <= 3:
                    return round(bet / 2.2, 2)
                elif bet <= 3.9:
                    return round(bet / 2.75, 2)
                elif bet <= 7.8:
                    return round(bet / 3.55, 2)     
                elif bet <= 12:
                    return round(bet / 4.2, 2)     
                elif bet <= 16:
                    return round(bet / 5.23, 2)
                elif bet > 16:
                    return round(bet / 5.3, 2)

            if fora == 1.5:   
                if bet <= 3:
                    return round(bet / 2.3, 2)
                elif bet <= 6:
                    return round(bet / 3.15, 2)
                elif bet <= 8:
                    return round(bet / 4, 2)     
                elif bet <= 12:
                    return round(bet / 4.9, 2)     
                elif bet > 12:
                    return round(bet / 7.3, 2) 

    @staticmethod
    def bets_fora_result(host_role: str, result: str, stat_result: str, one: float, X: float, two: float, fav_goals: int, fora: float): # Bet == 1
        fav_win_bets  = one if host_role == 'Fav' else two
        fav_drow_bets = X
        fav_loss_bets = two if host_role == 'Fav' else one 

        if stat_result == 'fav_drow' and result == 'fav_drow':
            return fav_drow_bets 
        elif stat_result == 'fav_drow' and result != 'fav_drow':
            return 0 

        if fora == None:
            if stat_result == 'fav_win' and result == 'fav_win':
                return fav_win_bets
            elif stat_result == 'fav_win' and result != 'fav_win':
                return 0 
            elif stat_result == 'fav_loss' and result == 'fav_loss':
                return fav_loss_bets
            elif stat_result == 'fav_loss' and result != 'fav_loss':
                return 0  

        if fora == 0:
            if stat_result == 'fav_win' and result == 'fav_win':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and result == 'fav_drow':
                return 1
            elif stat_result == 'fav_win' and result == 'fav_loss':
                return 0
            elif stat_result == 'fav_loss' and result == 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and result == 'fav_drow':
                return 1
            elif stat_result == 'fav_loss' and result == 'fav_win':
                return 0

        if fora == 0.25 or fora == -0.25:
            if stat_result == 'fav_win' and result == 'fav_win':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and result == 'fav_drow':
                return 0.5
            elif stat_result == 'fav_win' and result == 'fav_loss':
                return 0
            elif stat_result == 'fav_loss' and result == 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and result == 'fav_drow':
                return 0.5
            elif stat_result == 'fav_loss' and result == 'fav_win':
                return 0

        if fora == 0.5:
            if stat_result == 'fav_win' and result != 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)   
            elif stat_result == 'fav_loss' and result != 'fav_win':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)  
            else:
                return 0

        if fora == 0.75:
            if stat_result == 'fav_win' and result != 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora) 
            elif stat_result == 'fav_win' and result != 'fav_win' and fav_goals == -1:
                return 0.5
            elif stat_result == 'fav_win' and result != 'fav_win' and fav_goals < -1:
                return 0
            elif stat_result == 'fav_loss' and result != 'fav_win':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora) 
            elif stat_result == 'fav_loss' and result != 'fav_loss' and fav_goals == 1:
                return 0.5
            elif stat_result == 'fav_loss' and result != 'fav_loss' and fav_goals > 1:
                return 0

        if fora == -0.75:
            if stat_result == 'fav_win' and result == 'fav_win' and fav_goals > 1:
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora) 
            elif stat_result == 'fav_win' and result == 'fav_win' and fav_goals == 1:
                return 0.5
            elif stat_result == 'fav_win' and result != 'fav_win':
                return 0
            elif stat_result == 'fav_loss' and result == 'fav_loss' and fav_goals < -1:
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora) 
            elif stat_result == 'fav_loss' and result == 'fav_loss' and fav_goals == -1:
                return 0.5
            elif stat_result == 'fav_loss' and result != 'fav_loss':
                return 0 

        if fora == 1:
            if stat_result == 'fav_win' and fav_goals > -1:
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora) 
            elif stat_result == 'fav_win' and fav_goals == -1:
                return 1
            elif stat_result == 'fav_win' and fav_goals < -1:
                return 0
            elif stat_result == 'fav_loss' and fav_goals < 1:
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora) 
            elif stat_result == 'fav_loss' and fav_goals == 1:
                return 1
            elif stat_result == 'fav_loss' and fav_goals > 1:
                return 0

        if fora == -1:
            if stat_result == 'fav_win' and result == 'fav_win' and fav_goals > 1:
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora) 
            elif stat_result == 'fav_win' and result == 'fav_win' and fav_goals == 1:
                return 1
            elif stat_result == 'fav_win' and result != 'fav_win':
                return 0
            elif stat_result == 'fav_loss' and result == 'fav_loss' and fav_goals < -1:
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora) 
            elif stat_result == 'fav_loss' and result == 'fav_loss' and fav_goals == -1:
                return 1
            elif stat_result == 'fav_loss' and result != 'fav_loss':
                return 0

        if fora == 1.25: # Only Pre coeff calculate for Fav only bet
            if stat_result == 'fav_win' and result == 'fav_win':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and result != 'fav_win':
                return 0
            elif stat_result == 'fav_loss' and fav_goals < 1:
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and fav_goals == 1:
                return 0.5
            elif stat_result == 'fav_loss' and fav_goals > 1:
                return 0

        if fora == -1.25: # Only Fav coeff calculate for Pre only bet
            if stat_result == 'fav_win' and fav_goals > 1:
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and fav_goals == 1:
                return 0.5
            elif stat_result == 'fav_win' and fav_goals < 1:
                return 0
            elif stat_result == 'fav_loss' and result == 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and result != 'fav_loss':
                return 0

        if fora == 1.5: # Only Pre coeff calculate for Fav only bet
            if stat_result == 'fav_win' and result == 'fav_win':
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and result != 'fav_win':
                return 0
            elif stat_result == 'fav_loss' and fav_goals < 2:
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and fav_goals > 1:
                return 0    

        if fora == -1.5: # Only Fav coeff calculate for Pre only bet
            if stat_result == 'fav_win' and fav_goals > 1:
                return StatDataPrepare.fora_calculate('For_Fav', fav_win_bets, fora)
            elif stat_result == 'fav_win' and fav_goals < 2:
                return 0 
            elif stat_result == 'fav_loss' and result == 'fav_loss':
                return StatDataPrepare.fora_calculate('For_Pre', fav_loss_bets, fora)
            elif stat_result == 'fav_loss' and result != 'fav_loss':
                return 0     
    @staticmethod
    def calculate_only_win_bet_coef(drow_bet: float):
        if drow_bet <= 2.65:
            return 1
        if drow_bet <= 3.5:
            return round(drow_bet / 2.65, 2)
        elif drow_bet <= 4.28:
            return round(drow_bet / 3.25, 2)
        elif drow_bet <= 5.06:
            return round(drow_bet / 4.28, 2)
        elif drow_bet <= 7:
            return round(drow_bet / 4.97, 2)
        elif drow_bet <= 8:
            return round(drow_bet / 6.98, 2)
        elif drow_bet > 8:
            return 1

    @staticmethod    
    def only_win_or_drow_bets_result(result: str, stat_result: str, X: float):
        if stat_result == 'fav_win_loss' and result in ['fav_win', 'fav_loss']:
            return StatDataPrepare.calculate_only_win_bet_coef(X)
        elif stat_result == 'fav_drow' and result == 'fav_drow':
            return X
        else:
            return 0
        
        
        
    @staticmethod     
    def prediction_bets_profit_calculate(who_pred: str, y_test: int, pred: int, result: str, bet: float, fora: float):
        if who_pred == 'For_Drow' and result == 'fav_drow' and y_test == pred == 1:
            return bet

        if fora == None:
            if who_pred == 'For_Fav' and result == 'fav_win' and y_test == pred == 1:
                return bet
            elif who_pred == 'For_Pre' and result == 'fav_loss' and y_test == pred == 1:
                return bet
        elif fora == 0:
            if result == 'fav_drow' and y_test == pred == 1:
                return 1
            elif who_pred == 'For_Fav' and result == 'fav_win' and y_test == pred == 1:
                return sdp.fora_calculate(who_pred, bet, fora)
            elif who_pred == 'For_Pre' and result == 'fav_loss' and y_test == pred == 1:
                return sdp.fora_calculate(who_pred, bet, fora)   
        elif fora == 0.5:
            if who_pred == 'For_Fav' and result != 'fav_loss' and y_test == pred == 1:
                return sdp.fora_calculate(who_pred, bet, fora)
            elif who_pred == 'For_Pre' and result != 'fav_win' and y_test == pred == 1:
                return sdp.fora_calculate(who_pred, bet, fora)        