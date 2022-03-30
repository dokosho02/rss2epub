import schedule
import time
import ePubRSS

daily       = ePubRSS.DailyRun()
weekly      = ePubRSS.WeeklyRun()
half_hourly = ePubRSS.Run()


schedule.every(30).minutes.do( half_hourly.run )
schedule.every().day.at("20:40").do( daily.run )

schedule.every().day.at("22:20").do( daily.run )
schedule.every().day.at("23:40").do( daily.run )
schedule.every().friday.at("22:10").do( weekly.run )

"""
def job():
    print("I'm working...")
    
schedule.every(10).seconds.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)
"""

while True:
    schedule.run_pending()
    time.sleep(1)

# ePubRSS.main()
