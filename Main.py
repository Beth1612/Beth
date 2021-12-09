'''This is the main module that using flask to create a website'''

import sched
import time
import logging
from flask import render_template, request, Flask, redirect
import covid_data_handler
import covid_news_handling
import time_interval

s= sched.scheduler(time.time, time.sleep)
logging.basicConfig(filename='sys.log', encoding='utf-8')

app = Flask(__name__)
cancel_news= []
scheduled_updates = []

@app.route('/')
@app.route('/index')
def index():
    '''The main logic of the website is contained here '''
    s.run(blocking = False)
    news = covid_news_handling.update_news(cancel_news)
    local_last7days_cases, national_last7days_cases, national_current_hospital, national_total_death = covid_data_handler.update_data()
    no_news = request.args.get("notif")
    if no_news:
        cancel_news.append(no_news)
        return redirect ("/index")
    update_name = request.args.get("two")
    if update_name:
        time_for_update = request.args.get("update")
        update_covid = request.args.get("covid-data")
        update_news = request.args.get("news")
        repeating = request.args.get("repeat")
        if update_covid and update_news and time_for_update:
            update_interval = time_interval.interval(time_for_update)
            covid_event_name = covid_data_handler.schedule_covid_updates(update_interval,update_name,s)
            news_event_name = covid_news_handling.schedule_news_updates(update_interval,update_name,s)
            if repeating:
                scheduled_updates.append({"title":update_name,"content":("Repeating update of the covid data and the news at"+" "+time_for_update),"covid_event":covid_event_name,"news_event": news_event_name,"repeated":True})
            else:
                scheduled_updates.append({"title":update_name,"content":("Updating the covid data and the news at"+" "+time_for_update),"covid_event":covid_event_name,"news_event": news_event_name,"repeated":False})
        elif update_covid and time_for_update:
            update_interval = time_interval.interval(time_for_update)
            covid_event_name = covid_data_handler.schedule_covid_updates(update_interval,update_name,s)
            if repeating:
                scheduled_updates.append({"title":update_name,"content":("Fepeating update of the covid data at"+" "+time_for_update),"covid_event":covid_event_name,"news_event":None,"repeated":True})
            else:
                scheduled_updates.append({"title":update_name,"content":("Updating the covid data at"+" "+time_for_update),"covid_event":covid_event_name,"news_event":None,"repeated":False})
        elif update_news and time_for_update:
            update_interval = time_interval.interval(time_for_update)
            news_event_name = covid_news_handling.schedule_news_updates(update_interval,update_name,s)
            if repeating:
                scheduled_updates.append({"title":update_name,"content":("Repeating update of the news at"+" "+time_for_update),"covid_event":None,"news_event":news_event_name,"repeated":True})
            else:
                scheduled_updates.append({"title":update_name,"content":("Updating the news at"+" "+time_for_update),"covid_event":None,"news_event":news_event_name,"repeated":False})
        return redirect ("/index")
    for k in range (len(scheduled_updates)):
        if scheduled_updates[k]["news_event"]:
            if scheduled_updates[k]["news_event"] not in s.queue:
                if scheduled_updates[k]["repeated"]:
                    scheduled_updates[k]["news_event"] = covid_news_handling.schedule_news_updates(86400,str(scheduled_updates[k]["news_event"]),s)
                else:
                    scheduled_updates.pop(k)
            break
        else:
            if scheduled_updates[k]["covid_event"] not in s.queue:
                if scheduled_updates[k]["repeated"]:
                    if scheduled_updates[k]["news_event"]:
                        scheduled_updates[k]["news_event"] = covid_news_handling.schedule_news_updates(86400,str(scheduled_updates[k]["news_event"]),s)
                    scheduled_updates[k]["covid_event"] = covid_news_handling.schedule_news_updates(86400,str(scheduled_updates[k]["news_event"]),s)
                else:
                    scheduled_updates.pop(k)
            break
    deleted_update = request.args.get("update_item")
    if deleted_update:
        for h in range (len(scheduled_updates)):
            if scheduled_updates[h]["title"] == deleted_update:
                try:
                    s.cancel(scheduled_updates[h]["covid_event"])
                except:
                    None
                scheduled_updates.pop(h)
                break
        return redirect("/index")
    return render_template('index.html',
                            title="Daily Update",
                            location = "Exeter",
                            nation_location = "England",
                            local_7day_infections = local_last7days_cases,
                            national_7day_infections = national_last7days_cases,
                            hospital_cases = national_current_hospital,
                            deaths_total = national_total_death,
                            news_articles = news,
                            image = 'covid.jpg',
                            updates = scheduled_updates
                            )

if __name__ == "__main__":
    app.run()
