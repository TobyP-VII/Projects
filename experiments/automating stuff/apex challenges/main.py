all_characters: dict[str, int] = {"bangalore": 0,
                        "fuse": 0,
                        "ash": 0,
                        "mad maggie": 0,
                        "ballistic": 0,
                        "pathfinder": 0,
                        "wraith": 0,
                        "octane": 0,
                        "revenant": 0,
                        "horizon": 0,
                        "valkyrie": 0,
                        "alter": 0,
                        "bloodhound": 0,
                        "crypto": 0,
                        "seer": 0,
                        "vantage": 0,
                        "Gibraltar": 0,
                        "lifeline": 0,
                        "mirage": 0,
                        "loba": 0,
                        "newcastle": 0,
                        "conduit": 0,
                        "caustic": 0,
                        "wattson": 0,
                        "rampart": 0,
                        "catalyst": 0}

def get_amount() -> dict[str, int]:
    for x in all_characters:
        Char = x
        Amount = str(all_characters[x])
        # print(Char, Amount)
        
        while True:
            Amount: str = input("Enter amount of challenges for " + Char + ": ")
            try:
                int(Amount)
                break
            except Exception:
                print("Must be a number")
                
                
        all_characters[x] = int(Amount)
    
    return all_characters

def main() -> None:
    print(get_amount())
    
if __name__ == '__main__':
    main()