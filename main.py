import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time

city = input('What city would you like the information displayed for: ')

while True:
    text = input('For how many days would you like to get the weather information: ')
    try:
        interval = eval(text)
        break
    except NameError:
        print('There was an error parsing the number, please try again')

now = datetime.now()

start = time.time()

days = []
max_temps = []
min_temps = []
average_temps = []
conditions = {}

error = False

for i in range(interval):
    days.append(i + 1)
    nowStr = now.strftime('%Y-%m-%d')
    response = requests.get(
        'http://api.weatherapi.com/v1/history.json?key=a2f62e3d3aa24e33aa8221828241501&q=' + city + '&dt=' + nowStr)
    data = response.text
    parsed = json.loads(data)
    try:
        parsed['error']
        error = True
        break
    except KeyError:
        pass
    max_temp = parsed['forecast']['forecastday'][0]['day']['maxtemp_c']
    max_temps.append(max_temp)
    min_temp = parsed['forecast']['forecastday'][0]['day']['mintemp_c']
    min_temps.append(min_temp)
    average_temp = parsed['forecast']['forecastday'][0]['day']['avgtemp_c']
    average_temps.append(average_temp)
    condition = parsed['forecast']['forecastday'][0]['day']['condition']['text']
    if condition not in conditions:
        conditions[condition] = 1
    else:
        conditions[condition] += 1
    now = now - timedelta(days=1)

if error:
    print('The city could not be found')
else:
    location = parsed['location']['name']
    print('Weather for the last ' + text + ' days for ' + location + ':')

    labels = conditions.keys()
    sizes = conditions.values()

    plt.title('Weater conditions')
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()

    plt.title('Temperatures')
    plt.plot(days, average_temps, label='Average temperature [c]')
    plt.plot(days, min_temps, label='Min temperature [c]')
    plt.plot(days, max_temps, label='Max temperature [c]')
    plt.xlabel('Day')
    plt.ylabel('Temperature')
    plt.legend()
    plt.locator_params(axis='y', nbins=20)
    plt.show()

    end = time.time()
    print('The execution of the program took ' + str(round(end - start, 2)) + 's')
