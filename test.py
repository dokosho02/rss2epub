from Run import JournalRun, DailyRun
from datetime import datetime


def main():
    jr = JournalRun()
    jr.run()


    # daily = DailyRun()
    # daily.run()

    # weekly = ePubRSS.WeeklyRun()
    # half_hourly = ePubRSS.Run()


    # half_hourly.run()
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
