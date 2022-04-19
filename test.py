import ePubRSS
from datetime import datetime


def main():
    daily = ePubRSS.DailyRun()
    weekly = ePubRSS.WeeklyRun()
    half_hourly = ePubRSS.Run()


    daily.run()
    half_hourly.run()
    # weekly.run()

if __name__ == '__main__':
    start = datetime.now()
    print(start)
    # --------------
    main()
    # --------------
    end = datetime.now()
    timeDuration = str(end - start).zfill(4)
    print(end)
    print( 'Total time -- {}'.format(timeDuration) )
