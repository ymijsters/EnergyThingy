import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy
import seaborn as sns

mypath= './Excelfiles'
#2605 files
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
dataframes = []


def get_daily_energy_per_hour(dataframe):
    array_per_hour = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    averages_per_hour = []
    for item in range(0, len(dataframe[dataframe.columns[0]])):
        array_per_hour[dataframe[dataframe.columns[0]][item].hour].append(dataframe[dataframe.columns[1]][item]
                                                                          + dataframe[dataframe.columns[2]][item])
    for array in array_per_hour:
        averages_per_hour.append(numpy.mean(array))
    return averages_per_hour


def get_total_energy_per_hour(dataframes):
    array_per_hour = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    all_days_array = []
    # Per dag van de week (maandag = 0) een array met een lengte van 24 waar alle energie waarden inzitten
    
    for dataframe in dataframes:
        all_days_array.append(get_daily_energy_per_hour(dataframe))
    for day_array in all_days_array:
        for hour in range(0, len(day_array)):
            array_per_hour[hour].append(day_array[hour])
    return array_per_hour


def divide_in_periods(dataframe, periods):
    periods_array = []
    period_size = int(len(dataframe)/periods)
    for i in range(0,periods):
        periods_array.append(dataframe[period_size*i:period_size*(i+1)])
    return periods_array


def get_mean_for_all_periods(data_per_hour, periods):
    period_averages = []
    for hour in range(0, len(data_per_hour)):
        period_array = divide_in_periods(data_per_hour[hour], periods)
        period_averages.append([])
        for period in period_array:
            period_averages[hour].append(numpy.nanmean(period))
    return period_averages

def average_out(array):
	total_value = 0
	for value in array:
		total_value = total_value + value
	return total_value

def get_map_by_day_of_the_week(dataframes):
	# map_day_of_the_week = {0:list(),1:list(),2:list(),3:list(),4:list(),5:list(),6:list()}
	map_day_of_the_week = {}
	for dataframe in dataframes:
		total_map = {}
		weekday = dataframe["Tijdstip"][13].weekday()
		year = str(dataframe["Tijdstip"][13].year)
		month =  str(dataframe["Tijdstip"][13].month)
		day = str(dataframe["Tijdstip"][13].day)
		if len(month) == 1:
			month = "0" + month
		if len(day) == 1:
			day = "0" + day
		date = year + month + day
		total_map = {"energy":average_out(get_daily_energy_per_hour(dataframe)),"date": date, "weekday": weekday}
		map_day_of_the_week[int(date)] = total_map
	return map_day_of_the_week



def getMap():
    for file in onlyfiles:
        df = pd.read_excel('./Excelfiles/' + file)
        dataframes.append(df)
        x = [item.time() for item in df[df.columns[0]]]
        y = [df[df.columns[1]][item] + df[df.columns[2]][item] for item in range(0, len(df[df.columns[0]]))]

    total_energy_per_hour = get_total_energy_per_hour(dataframes)
    total_map = get_map_by_day_of_the_week(dataframes)
    return total_map
	# print(total_map)


# period_array = get_mean_for_all_periods(total_energy_per_hour, 100)

# for hour_periods in period_array:
    # print(hour_periods)
    # print(numpy.argmax(hour_periods))

#print(total_energy_per_hour[4][0:int(len(total_energy_per_hour[4])/2+1)])
#plt.hist(total_energy_per_hour[4][0:int(len(total_energy_per_hour[4])/4)], bins=100)
#plt.hist(total_energy_per_hour[4][int((len(total_energy_per_hour[4])/4)+1):int(len(total_energy_per_hour[4])/2)], bins=100)
#plt.hist(total_energy_per_hour[4][int((len(total_energy_per_hour[4])/2)+1):int((len(total_energy_per_hour[4])/4)*3)], bins=100)
#plt.hist(total_energy_per_hour[4][int((len(total_energy_per_hour[4])/4)*3+1):len(total_energy_per_hour[4])], bins=100)
#plt.xlim(0, 1)
#plt.show(block=True)

adres = 'Mr van Rhemenslaan'
huisnummer = 3
postcode = '7316AJ'
stad = 'Apeldoorn'

