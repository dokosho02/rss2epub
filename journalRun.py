from Run import Run

from Journals import journalRSS
# ----------------------------------
class JournalRun(Run):
    def __init__(self):
        self.rssList = journalRSS
# ----------------------------------
def main():
    jr = JournalRun()
    jr.run()
# ----------------------------------
if __name__ == '__main__':
    main()
