'''This module calulate data that is needed for the website from a csv file and using the covid api'''

import sched
import time
import json
from uk_covid19 import Cov19API

s= sched.scheduler(time.time, time.sleep)
config_data = json.load(open("config.json"))

def parse_csv_data(csv_filename) -> list:
    '''Reads the csv file and returns a list of covid data'''
    data = open(csv_filename, "r").readlines()
    rows = []
    for line in data:
        line = line.rstrip("\n")
        line = line.lower()
        rows.append(line)
    return rows

def process_covid_csv_data(covid_csv_data:list) -> str:
    '''Takes the covid data in a list and calulates and returns the rate of the last 7 days, the current number of hospital cases and the cumulative number of deaths'''
    data = covid_csv_data[3:10]
    last7days_cases = 0
    for i in range (0,7):
        each_day = data[i].split(",")
        last7days_cases += int(each_day[6])
    today = covid_csv_data[1].split(",")
    current_hospital_cases = int(today[5])
    found = False
    index = 1
    while not found:
        day = covid_csv_data[index].split(",")
        if day[4] != "":
            found = True
            total_death = int(day[4])
        else:
            index += 1
    return last7days_cases, current_hospital_cases, total_death

def process_covid_api_data(covid_api_data:dict) -> str:
    '''Takes covid data in the form of a json file and calulates and returns the rate of the last 7 days, the current number of hospital cases and the cumulative number of deaths'''
    last7days_cases = 0
    for j in range (1,8):
        last7days_cases += covid_api_data["data"][j]["newCasesByPublishDate"]
    current_hospital_cases = covid_api_data["data"][1]["hospitalCases"]
    total_death = covid_api_data["data"][1]["cumDeaths28DaysByDeathDate"]
    return last7days_cases,current_hospital_cases,total_death

def covid_API_request(location = "Exeter", location_type = "ltla") -> dict:
    '''Create and returns a json file of the covid data for the location specified by the location and location_type parameters'''
    local_only = [f'areaType={location_type}',f'areaName={location}']
    cases_and_deaths = {"date": "date","areaName": "areaName","areaCode": "areaCode","hospitalCases": "hospitalCases","newCasesByPublishDate": "newCasesByPublishDate","cumCasesByPublishDate": "cumCasesByPublishDate","newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate","cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"}
    api = Cov19API(filters=local_only, structure=cases_and_deaths)
    data = api.get_json()
    return data

def update_data () -> str:
    '''Calls the covid_API_request function to recieve the data and then gives the data to the process_covid_api_data to be processed and then the data that is needed for the website'''
    local_last7days_cases, local_current_hospital, local_total_death = process_covid_api_data(covid_API_request(config_data["data"]["local_location"],config_data["data"]["local_location_type"]))
    national_last7days_cases, national_current_hospital, national_total_death = process_covid_api_data(covid_API_request(config_data["data"]["national_location"],config_data["data"]["national_location_type"]))
    return local_last7days_cases, national_last7days_cases, national_current_hospital, national_total_death

def schedule_covid_updates(update_interval:int, update_name:str, s) -> str:
    '''Creates schedule updates of the covid data and returns the name of the update created'''
    globals()[update_name] = s.enterabs(time.time()+update_interval,1,update_data,)
    return globals()[update_name]
