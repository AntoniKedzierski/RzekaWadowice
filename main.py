import pandas as pd
import datetime
import lmoments

from scipy.stats import norm

def read_data():
    dane = {
        'rzeka': [],
        'stacja': [],
        'data': [],
        'rok_hydro': [],
        'mies_hydro': [],
        'sezon': [],
        'przeplyw': []
    }

    with open('data/dane.txt', 'r') as file:
        for line in file.readlines():
            rok = line[72:76].replace(' ', '')
            rok_hydrologiczny = rok
            miesiac_hydrologiczny = line[76:78]
            miesiac = line[97:99].replace(' ', '')
            dzien = line[78:80].replace(' ', '')
            dane['rzeka'].append(line[32:72].replace(' ', ''))
            przeplyw = line[86:97].replace(' ', '').replace(',', '.')
            if przeplyw == '99999.999':
                dane['przeplyw'].append(None)
            else:
                dane['przeplyw'].append(float(przeplyw))
            dane['stacja'].append(line[8:32].replace(' ', ''))

            rok = int(rok)
            miesiac = int(miesiac)
            dzien = int(dzien)

            if miesiac >= 11:
                rok = rok - 1

            sezon = 'zima'
            if miesiac >= 5 and miesiac <= 10:
                sezon = 'lato'

            dane['data'].append(datetime.datetime(rok, miesiac, dzien))
            dane['rok_hydro'].append(int(rok_hydrologiczny))
            dane['mies_hydro'].append(int(miesiac_hydrologiczny))
            dane['sezon'].append(sezon)

    pd.DataFrame(dane).to_csv('data/dane.csv', index=False)


def eval_wadowice():
    wadowice = pd.read_csv('data/wadowice.csv', parse_dates=[0])
    wadowice['rok'] = wadowice['data'].dt.year
    print(wadowice)
    # shape, loc, scale = norm.fit(wadowice['przeplyw'])

if __name__ == '__main__':
    rzeki = pd.read_csv('data/dane.csv', parse_dates=[2])
    wadowice = rzeki.loc[(rzeki['stacja'] == 'WADOWICE'), :].dropna()
    # print(wadowice.loc[rzeki['data'] == min(wadowice['data']), :])
    # print(wadowice.loc[rzeki['data'] == max(wadowice['data']), :])
    #
    wadowice[['data', 'rok_hydro', 'mies_hydro', 'sezon', 'przeplyw']].to_csv('data/wadowice.csv', index=False)
    #
    # # wadowice = wadowice.sort_values('data')
    # # with pd.option_context('display.max_rows', None):
    # #     print(wadowice)
    #
    # dni = (wadowice['data'] - wadowice['data'].shift(1)).dt.days
    # print(dni)
    # print(dni.unique())


    eval_wadowice()





