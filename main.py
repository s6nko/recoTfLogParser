import re
import sys
import json

'''
Dictionnary layout that stores players

"SteamId" = {
    "name" = "",
    "kills" = 0,
    "deaths" = 0,
    "damage" = 0,
    "classesPlayed" = "",
    "team" = ""
} 
'''
match_db = {}

#Regex patterns
kill_pattern = r'"(?P<attacker_name>.+?)<\d+><\[(?P<attacker_id>U:\d:\d+?)\]><.+?>"\s+killed\s+"(?P<victim_name>.+?)<\d+><\[(?P<victim_id>U:\d:\d+?)\]><.+?>"'
suicide_pattern = r'"(?P<attacker_name>.+?)<\d+><\[(?P<attacker_id>U:\d:\d+?)\]><.+?>"\s+committed\s+suicide'
damage_pattern = r'"(?P<attacker_name>.+?)<\d+><\[(?P<attacker_id>U:\d:\d+?)\]><.+?>"\s+triggered\s+"damage"\s+against\s+"(?P<victim_name>.+?)<\d+><\[(?P<victim_id>U:\d:\d+?)\]><.+?>"\s+\(damage\s+"(?P<damage_amount>\d+)"\)(?:\s+\(realdamage\s+"(?P<real_damage>\d+)"\))?'
class_team_pattern = r'"(?P<name>.+?)<\d+><\[(?P<steamid>[U:\d:]+)\]><(?P<team>\w+)>" spawned as "(?P<class>\w+)"'
round_win_pattern = r'World triggered "Round_Win"'
match_end_pattern = r'World triggered "Game_Over"'
round_start_pattern = r'World triggered "Round_Start"'

def getOrPutPlayerInDb(steam_id, name):
    if steam_id not in match_db:
        match_db[steam_id] = {
            "name": name,
            "kills": 0,
            "deaths": 0,
            "damage": 0,
            "ClassesPlayed": "",
            "team": ""
            }
    return match_db[steam_id]

def processLog(log_file):
    in_round = False
    classes_check = False
    for line in log_file:
        if re.search(round_start_pattern, line):
            in_round = True
            if len(match_db) < 18:
                classes_check = True
            continue
        
        class_team_match = re.search(class_team_pattern, line)
        if class_team_match and classes_check:
            # Process class and team information
            player = getOrPutPlayerInDb(class_team_match.group("steamid"), class_team_match.group("name"))
            if class_team_match.group("class") not in player["ClassesPlayed"]:
                player["ClassesPlayed"] = class_team_match.group("class")
            player["team"] = class_team_match.group("team")
            continue
        
        if re.search(match_end_pattern, line):
            print(json.dumps(match_db, indent=4))
            print("Match ended")
            match_db.clear()
            in_round = False
            continue
        
        if re.search(round_win_pattern, line):
            in_round = False
            continue

        if not in_round:
            continue

        kill_match = re.search(kill_pattern, line)
        if kill_match:
            attacker = getOrPutPlayerInDb(kill_match.group("attacker_id"), kill_match.group("attacker_name"))
            victim = getOrPutPlayerInDb(kill_match.group("victim_id"), kill_match.group("victim_name"))
            
            if "feign_death" in line:
                #Dead ringer utilisée, pas besoin de compter la mort ni le kill
                continue
            else:
                victim["deaths"] += 1
                attacker["kills"] += 1
            continue

        damage_match = re.search(damage_pattern, line)
        if damage_match:
            attacker = getOrPutPlayerInDb(damage_match.group("attacker_id"), damage_match.group("attacker_name"))
            if 'customkill "backstab"' in line:
                #doesn't fucking work because I have to figure out how to read the next line first
                attacker["damage"] += int(damage_match.match.group("real_damage"))
            else:
                attacker["damage"] += int(damage_match.group("damage_amount"))
            continue

        suicide_match = re.search(suicide_pattern, line)
        if suicide_match:
            attacker = getOrPutPlayerInDb(suicide_match.group("attacker_id"), suicide_match.group("attacker_name"))
            attacker["deaths"] += 1
            continue

if __name__ == "__main__":
    if sys.argv[1:]:
        log_file_path = sys.argv[1]
        with open(log_file_path, "r", encoding="utf-8") as log_file:
            processLog(log_file)
        print("Finished processing log file.")
        print("Total items in DB: ", len(match_db))
        print(match_db)
    else:
        print("Please provide a log file path as an argument.")

