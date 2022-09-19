
journals = [
    "journal-of-structural-geology",
    "tectonophysics",
    "earth-and-planetary-science-letters",
    "tribology-international",
    "earth-science-reviews",
    "journal-of-asian-earth-sciences",
]


# ------------------------------------------------

elsevierLinkHead = "https://rsshub.app/elsevier/"
elsevierLinkEnd  = "/latest"

journalRSS = list(map(lambda x: f"{elsevierLinkHead}{str(x)}{elsevierLinkEnd}" , journals))

def main():
    print("This is class Journals")
    
    [print(rl) for rl in journalRSS]


if __name__ == '__main__':
    main()