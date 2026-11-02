import random

if __name__ == "__main__":
    print("=== Game Data Alchemist ===")
    players = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma',
               'Gregory', 'john', 'kevin', 'Liam']
    print(f"Initial list of players: {players}")
    cap_all = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {cap_all}")
    cap_only = [name for name in players if name[0].isupper()]
    print(f"New list of capitalized names only: {cap_only}")
    scores = {name: random.randint(0, 1000) for name in cap_all}
    print(f"Score dict: {scores}")
    av_scr = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {av_scr}")
    h_scrs = {name: score for name, score in scores.items() if score > av_scr}
    print(f"High scores: {h_scrs}")
