from datetime import datetime

# ------------------------------
def main():
    pass
# ------------------------------
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
