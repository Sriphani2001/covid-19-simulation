from operator import index
import pandas as pd
from datetime import datetime, timedelta
from markov_chain import markov_chain
from math import fabs, floor
from helper import create_plot



# returns the indices of countries. will be useful for iloc function.
def return_indice(countries_list):

    indices = [x for x in range(0,152)]
    all_countries = [
    'Afghanistan',
    'Albania',
    'Algeria',
    'Angola',
    'Argentina',
    'Armenia',
    'Australia',
    'Austria',
    'Azerbaijan',
    'Bahrain',
    'Bangladesh',
    'Belarus',
    'Belgium',
    'Benin',
    'Bolivia',
    'Bosnia and Herzegovina',
    'Botswana',
    'Brazil',
    'Bulgaria',
    'Burkina Faso',
    'Burundi',
    'Cambodia',
    'Cameroon',
    'Canada',
    'Central African Republic',
    'Chad',
    'Chile',
    'China',
    'Colombia',
    'Congo',
    'Costa Rica',
    'Cote d\'Ivoire',
    'Croatia',
    'Cuba',
    'Czechia',
    'Democratic Republic of Congo',
    'Denmark',
    'Djibouti',
    'Dominican Republic',
    'Ecuador',
    'Egypt',
    'El Salvador',
    'Equatorial Guinea',
    'Eritrea',
    'Estonia',
    'Eswatini',
    'Ethiopia',
    'Finland',
    'France',
    'Gabon',
    'Gambia',
    'Georgia',
    'Germany',
    'Ghana',
    'Greece',
    'Guatemala',
    'Guinea',
    'Guinea-Bissau',
    'Haiti',
    'Honduras',
    'Hong Kong',
    'Hungary',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland',
    'Israel',
    'Italy',
    'Jamaica',
    'Japan',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Liberia',
    'Libya',
    'Lithuania',
    'Madagascar',
    'Malawi',
    'Malaysia',
    'Mali',
    'Mauritania',
    'Mauritius',
    'Mexico',
    'Moldova',
    'Mongolia',
    'Morocco',
    'Mozambique',
    'Myanmar',
    'Namibia',
    'Nepal',
    'Netherlands',
    'New Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'North Macedonia',
    'Norway',
    'Oman',
    'Pakistan',
    'Palestine',
    'Panama',
    'Papua New Guinea',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Puerto Rico',
    'Qatar',
    'Romania',
    'Russia',
    'Rwanda',
    'Saudi Arabia',
    'Senegal',
    'Serbia',
    'Sierra Leone',
    'Singapore',
    'Slovakia',
    'Slovenia',
    'Somalia',
    'South Korea',
    'Spain',
    'Sri Lanka',
    'Sudan',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tanzania',
    'Thailand',
    'Timor',
    'Togo',
    'Trinidad and Tobago',
    'Tunisia',
    'Turkey',
    'Uganda',
    'Ukraine',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
    'Uruguay',
    'Uzbekistan',
    'Venezuela',
    'Vietnam',
    'Zambia',
    'Zimbabwe']
    index_giver = dict(zip(all_countries,indices))
    returner = []
    for i in countries_list:
        returner.append(index_giver.get(i))
    returner.sort()
    return returner

def chain(steps):
    pass


def run(countries_csv_name,countries, sample_ratio,start_date,end_date):
    # parsing the data and creating a copy df
    df1 = pd.read_csv(countries_csv_name)
    indices = return_indice(countries)
    df2 = {
        'country':[],
        'population':[],
        'median_age':[],
        'less_5':[],
        '5_to_14':[],
        '15_to_24':[],
        '25_to_64':[],
        'over_65':[]
    }
    df2 = pd.DataFrame(df2)
    for i in indices:
        df2.loc[len(df2)] = df1.iloc[i]

    # creating sample population dataframes
    df3 = pd.DataFrame()
    df3['country'] = df2['country']
    # creating sample population dataframes
    df3['sample_population'] = (df2['population']//sample_ratio)
    df3['less_5'] = ((df3['sample_population']*df2['less_5'])/100).astype(float).round()
    df3['5_to_14'] = ((df3['sample_population']*df2['5_to_14'])/100).astype(float).round()
    df3['15_to_24'] = ((df3['sample_population']*df2['15_to_24'])/100).astype(float).round()
    df3['25_to_64'] = ((df3['sample_population']*df2['25_to_64'])/100).astype(float).round()
    df3['over_65'] = ((df3['sample_population']*df2['over_65'])/100).astype(float).round()

    # parsing dates
    actual_starting_date = start_date.split('-')
    actual_ending_date = end_date.split('-')
    date1 = datetime(int(actual_starting_date[0]),int(actual_starting_date[1]),int(actual_starting_date[2]))
    date2 = datetime(int(actual_ending_date[0]),int(actual_ending_date[1]),int(actual_ending_date[2]))
 

    days = (date2-date1).days + 1

    df4 = pd.DataFrame({
        'person_id':[],
        'age_group_name':[],
        'country':[],
        'date':[],
        'state':[],
        'staying_days':[],
        'prev_state':[]
    })

    #iterationg through given countries
    for index, country in df3.iterrows():
        country_index = 0
        id = 0
        #iterating through age groups
        for age in df3.columns[2:]:

            #iterating through people in age group
            for guy in range(int(country[age])):
                print(id)

                #getting markov timeline
                states = markov_chain(days,age)
                prev_state = 'H'
                date_index = 0
                for state in states:
                    current_state = state[0]
                    if(state[0]=='H' or state[0]=='D'):
                        df4.loc[len(df4)] = [id, age, country['country'], (date1+timedelta(days=date_index)).strftime("%Y-%m-%d"),state[0], 0, prev_state]
                        date_index += 1
                    else:
                        for a in range(1, state[1]+1):
                            df4.loc[len(df4)] = [id, age, country['country'], (date1+timedelta(days=date_index)).strftime("%Y-%m-%d"),state[0], a, prev_state]
                            date_index += 1
                    prev_state = current_state
                id+=1
    
    df4.to_csv('a3-covid-simulated-timeseries.csv',index=False)

    df5 = pd.DataFrame({'date':[],'country':[],'D':[],'H':[],'I':[],'M':[],'S':[]})

    for country in countries:
        date_index = 0
        for a in range(days):

            frequency = {'date':'','country':'','D':0,'H':0,'I':0,'M':0,'S':0}
            date = (date1+timedelta(days=date_index)).strftime("%Y-%m-%d")
            data = list(df4[(df4['country']==country) & (df4['date']==date)]['state'])
            
            for state in set(data):
                frequency[state] = data.count(state)
            
            frequency['country'] = country
            frequency['date'] = date
            df5.loc[len(df5)] = frequency
            date_index += 1
    
    df5.to_csv('a3-covid-summary-timeseries.csv',index=False)

    create_plot('a3-covid-summary-timeseries.csv',countries)

start = '2021-04-01'
ending = '2022-04-30'
RATIO = 1e6
countries = ['Afghanistan','Sweden','Japan']
run(countries_csv_name='a3-countries.csv',countries=countries,sample_ratio=RATIO,start_date=start,end_date=ending)

#timeline = pd.read_csv('a3-covid-summary-timeseries.csv')

