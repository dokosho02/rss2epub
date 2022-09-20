elsevier = [
    "journal-of-structural-geology",
    "tectonophysics",
    "earth-and-planetary-science-letters",
    "tribology-international",
    "earth-science-reviews",
    "journal-of-asian-earth-sciences",
    "theoretical-and-applied-fracture-mechanics",
    "computers-and-geosciences",
]
# ------------------------------------------------
springer = [
    10346,
]
# ------------------------------------------------
elsevierLinkHead = "https://rsshub.app/elsevier/"
elsevierLinkEnd  = "/latest"
elsevierRSS = list(map(lambda x: f"{elsevierLinkHead}{str(x)}{elsevierLinkEnd}", elsevier))
# ------------------------------------------------
springerLinkHead = "https://rsshub.app/springer/journal/"
springerRSS = list(map(lambda x: f"{springerLinkHead}{str(x)}" , springer))


journalRSS = elsevierRSS + springerRSS
# ------------------------------------------------
def main():
    print("These are Elsevier Journals")
    [print(rl) for rl in elsevierRSS]

    print("These are Springer Journals")
    [print(rl) for rl in springerRSS]
    
    [print(rl) for rl in journalRSS]

    
# ------------------------------------------------

if __name__ == '__main__':
    main()
