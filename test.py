import ePubRSS


daily = ePubRSS.DailyRun()
weekly = ePubRSS.WeeklyRun()
half_hourly = ePubRSS.Run()


daily.run()
half_hourly.run()
# weekly.run()
