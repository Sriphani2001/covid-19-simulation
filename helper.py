import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as md

from pathlib import Path
import os


OUTPUT_NAME = 'a3-covid-simulation.png'
def get_filepath(filename):
    '''
    Returns full file path 
    '''
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    filepath = os.path.join(source_dir,filename)
    return filepath

def save_plot(fig, filename):
    filepath = get_filepath(filename)    
    fig.savefig(filepath,dpi=300)

def read_dataset(filename):

    filepath = get_filepath(filename)

    df = pd.read_csv(filepath, sep=',', header= 0)

    return df

def create_plot(summary_csv, countries):
    '''
    Creates a plot from the time series of the infection states

    input:
    summary_csv
    countries 

    the format of the summary_csv file should be like this, the name of the columns (date,D,H,I,M,S) matters (but not index). 
    The order of columns does not matter. 'NaN' values can be 0. Float values can be integer.

    country,date,H,I,S,M,D
    Afghanistan,2021-04-01,37,0,0,0,0
    Japan,2021-04-01,121,0,0,0,0
    Sweden,2021-04-01,9,0,0,0,0
    Afghanistan,2021-04-02,32,5,0,0,0
    Japan,2021-04-02,86,35,0,0,0  

    The `countries` is a list of countries. At this moment only an aggregated plot is created (For future, it needs to add a `country` column `states_timeseries_df` 
    to be able to create subplots)

    '''
    states_timeseries_df = read_dataset(summary_csv)
    

    print(f'Plotting is being prepared for the following dataset ...')
    print(states_timeseries_df)
    states_timeseries_df = states_timeseries_df[['country','date', 'H', 'I', 'S', 'M', 'D']]#reorder columns
    states_timeseries_df['date'] = pd.to_datetime(states_timeseries_df['date'])
    states_timeseries_df.set_index('date')

    # Multiple countries in subfigures
    countries_num = len(countries)
    fig, ax = plt.subplots(countries_num, figsize =(16,9*countries_num))
    for i in range(countries_num):
 
        states_timeseries_df[states_timeseries_df['country']==countries[i]].plot(
            kind= 'bar', 
            x= 'date', 
            # figsize =(16,9), 
            stacked=True, 
            width = 1, 
            color=['green', 'darkorange', 'indianred', 'lightseagreen', 'slategray'],
            ax = ax[i])

        ax[i].legend(['Healthy', 'Infected (without symptoms)', 'Infected (with symptoms)', 'Immune', 'Deceased'])
        ax[i].set_xticklabels(ax[i].get_xticks(), rotation = 30)
        # plot_name = ', '.join(countries)
        plot_name = countries[i]
        ax[i].set_title(f"Covid Infection Status in {plot_name}")
        ax[i].set_xlabel("Date")
        ax[i].set_ylabel("Population in Millions")

        ax[i].xaxis.set_major_locator(md.MonthLocator())#bymonth = range(1, 13, 2) [1,4,7,10]
        selected_dates = states_timeseries_df['date'].dt.to_period('M').unique()
        ax[i].set_xticklabels(selected_dates.strftime('%b %Y'), rotation=30, horizontalalignment= "center")


    # Pandas bug 1970!
    # ax.xaxis.set_major_locator(md.YearLocator())
    # ax.xaxis.set_minor_locator(md.MonthLocator())
    # date_format = md.DateFormatter("%Y-%m")
    # ax.xaxis.set_major_formatter(date_format)


    save_plot(fig, f'{OUTPUT_NAME}')

    print(f'Plotting Done!')
