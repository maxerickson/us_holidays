#! python3
import json
import collections
#// https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States
federal={"New Year's Day" : [ 1, 1 ],
            "Martin Luther King, Jr. Day" : ['firstJanuaryMonday',14],
            "Washington's Birthday" : ['firstFebruaryMonday',14],
            "Memorial Day" : ['lastMayMonday',0],
            "Independence Day" : [7,4],
            "Labor Day" : ['firstSeptemberMonday',0],
            "Columbus Day" : ['firstOctoberMonday', 7],
            "Veterans Day" : [11,11],
            "Thanksgiving" : ['firstNovemberThursday', 21],
            "Christmas Day" : [ 12, 25 ],
        }

def rev_dict(d):
    return dict(((tuple(v),k) for k,v in d.items()))

def date_score(d):
    if isinstance(d[0], str):
        if d[0]=='easter':
            return 4.23+float(d[1])/30
        else:
            for i,t in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']):
                if t in d[0]:
                    return float(i+1)+float(d[1])/30
            return 13
    else:
        return float(d[0])+float(d[1])/30.

rev_fed=rev_dict(federal)
fed_dates=set(rev_fed.keys())
# special cases
# a couple of election days are every other year, illinois, indiana, hawaii
# Kentucky good friday
# Texas has optional and partial days.

f=json.load(open('openinghours_holidays.json', 'r', encoding='utf8'))

## k=f["us"].keys()
## print(len(k))
## print(k)

## datedefs=set()
## k=list(k)
## k.remove('PH')
## try:
##     for key in k:
##         hds=f['us'][key]['PH']
##         for v in hds.values():
##             datedefs.add(tuple(v))
## except:
##     print(key)
## for d in datedefs:
##     print(d)

states=f["us"]
states.pop("PH")
keys=sorted(states.keys())
date_lists=collections.defaultdict(list) # collect every entry under the date definition
date_states=collections.defaultdict(list)
specialwords=set()
# diff states/federal formatted for comparison to wikipedia
for state in keys:
    print(state)
    rev_state=rev_dict(states[state]["PH"])
    specialwords.update(w[0] for w in rev_state.keys() if isinstance(w[0], str))
    for k,v in rev_state.items():
        date_lists[k].append(v)
        date_states[k].append(state)
    dates=set(rev_state.keys())
    for dt in sorted(dates.intersection(fed_dates), key=date_score):
        if  rev_state[dt]!=rev_fed[dt]:
            print('   ', rev_state[dt],'replaces',rev_fed[dt])
    for dt in sorted(fed_dates-dates, key=date_score):
        print('   -',rev_fed[dt])
    for dt in sorted(dates-fed_dates, key=date_score):
        print('   +',rev_state[dt], dt)
print()

# holidays that occur in all states
for k,v in date_lists.items():
    if len(v)==len(states):
        if len(set(v))==1:
            print ('All:', set(v), k)
        else:
            print('All, with variation:', k)
            print('    ', set(v))
print()
# in more than 1 state.
for k,v in date_lists.items():
    if len(v) > 1 and len(v)!=len(states):
        print('Several:', k)
        print('    ', date_states[k])
        print('    ',set(v))
print()
print(sorted(specialwords))
