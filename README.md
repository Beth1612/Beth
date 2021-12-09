# Covid information website

## Contents of this file
- Introduction
- Prerequisites
- Installation
- Getting Started Tutorial
- Developer Documentation
- Details

## Introduction

This is a simple personalised covid dashboard. Within the dashboard there is data that shows the current rate of cases within your local and national area. It also shows news articles relating to covid and 
you can schedule updates to the data or news within the website.

This dashboard was created to give people easy access to data and news in their area and the country that they live in about covid.  

## Prerequisites

To run this program, you will need to install:
- Flask
- Sched

Python version 3.9 was used to create this project so thing version or newer is recommended.

## Installation

To install the needed modules uses:
- pip install Flask
- pip install sched

When the project is run, it will open the server. The user needs to go to  http://127.0.0.1:5000/ for the interface to appear and be able to use the dashboard that has been created. 

## Getting Started Tutorial

When the website it first opened, it will have the data for your area and national area in the middle column, updates in the left and news articles on the right. 

For the news articles, there are 4 on the page, if not interested in an article that is there, you can click the X in the top right corner. This will get rid of the articles and then load a new article to 
replace it. To change the terms used for the news articles, you can change "covid terms" in the config file.

To schedule an update, you need to use the tools underneath the data in the middle column. You need to set a name for the update and time you want the update to happen. You then will need to pick what you 
want to be updates: data, news or both, and if you want the update to repeat. This will mean that the update will happen at the same time every day at the time you picked. Updates can also be discarded in 
the same way the news articles are, by clicking the X in the top right corner, this will cancel the update and if it is repeating all the updates that would happened.

## Developer Documentation 

The code using a main module which need to be run for the server to become active and then the website can be accesses. Within this main module, it uses flask to access a html file and create to website 
needed. The main module also calls on other modules, covid_data_handler.py which using the covid API to obtain data that is presented on the website, covid_news_handling.py that uses the news API to get 
articles relating to the terms given, in this case it is relating to covid and coronavirus and time_interval.py, this module converts the time that was given by the user into seconds and then calculates 
the interval from the time the program is running to the time the user has given. 

## Details 

Author - Bethany Whiting
