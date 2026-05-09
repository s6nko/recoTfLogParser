Log parser made for reconnexion.tf as per their wish for moving on from logs.tf or atleast avoid it as much as possible

python main.py [server_log]

TFTrue is needed for this parser to work
Python3 is required (duh)

__________________________
The program returns a JSON (in the terminal for now) that follows this template:

"SteamId" = {
    "name" = "",
    "kills" = 0,
    "deaths" = 0,
    "damage" = 0,
    "classesPlayed" = "",
    "team" = ""
} 

Every players are included, and in the offchance that the tournament mode gets glitchy or people have fun bugging it, it should not ruin their stats or give the parser any trouble.
Spies have boosted stats due to the fact they do six time their damage for each backstab they get, thats double for the backstab + triple because it's a crit. TFTrue has a real_damage event but I don't know why it's put before the backstab is registered, so it's difficult to make a condition for it