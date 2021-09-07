import swisseph as swe
swe.set_ephe_path('/brahman/share/ephe')
now = swe.julday(2007,3,3) # get Julian day number
res = swe.lun_eclipse_when(now) # find next lunar eclipse (from now on)
ecltime = swe.revjul(res[1][0]) # get date UTC
day = swe.calc_ut(now, swe.AST_OFFSET+13681) # asteroid Monty Python

# help(swe)
