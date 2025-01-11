""" 
---------
Libraries
---------

BeasutifulSoup: Used to scrape homebrew data from dandwiki.com coverd 
under the GNU v1.3 License located in the DATA LICENSE folder.

requests: Used to connect to dandwiki.com.

re: Used to search for specific text in the soup objects such as "Armor Class,"
"Hit Points," and "Strength."

pandas: Used to create a dataframe to store the monster data.

math: Used for various math functions such as floor().
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import math

"""
---------
Functions
---------
"""

def monster_name(monster_soup):                                           # The input is the Soup object made from the individual monsters webpage
    
    """Get Monster's Name"""
    
    return monster_soup.find("span", class_="mw-headline").get_text()     # The name is in the first span of the page with class "mw-headline". This grabs the text.



def monster_size_type_alignment(monster_soup):
    
    """Get Monster's Size, Body Type, and Alignment"""
    
    size, body_type, alignment = monster_soup.find("table").find("i").get_text().split(" ")   # The size, body type, and alignment are all together in the first italic tag of the first table. This grabs and assgins the values
    body_type = body_type.rstrip(",")                                                         # Removes a comma between body type and alignment
    
    return size, body_type, alignment



def monster_ac_naturalarmor(monster_soup):
    
    """Get Monster's Armor Class value and returns a boolean value if the monster has natural armor or not"""
    
    armorclass_naturalarmor = monster_soup.find("a", href=re.compile("Armor_Class")).parent.next_sibling.get_text().strip(" ")      # Searches for the only reference of Armor Class then goes up in the tree to grab the value with possible natural armor. There is a space at the beginning of the text.
    
    if "natural armour" in armorclass_naturalarmor:                              # Note the u in "natural armour" 
        ac = armorclass_naturalarmor.split(" ", 1)[0]                            # Splits the armorclass_naturalarmor variable only splitting once because of the space in "natural armour". Only grabs the first item which is the AC.
        natural_armor = True        
    else:
        ac = armorclass_naturalarmor                                             # Assigns the armor class to ac if there is no natural armor.
        natural_armor = False
        
    return int(ac), natural_armor                                                # Variable is converted from string to int



def monster_hp_hitdice_hitdicecount(monster_soup):

    """Get Monster's Hit Points, Hit Dice, and how many Hit Dice the monster has"""
    
    hitpoints_hitpointscalc = monster_soup.find("a", href=re.compile("Hit_Points")).parent.next_sibling.get_text().strip(" ")               # Searches for the only reference of Hit Points then goes up in the tree to grab the value with the calculation for HP. There is a space at the beginning of the text.
    hit_points, hit_points_calc = hitpoints_hitpointscalc.split(" ", 1)                                  # Splits the HP and the calculation
    hit_dice_count, hit_dice = hit_points_calc.strip("()").split(" + ")[0].split("d")                    # Opted for trimming the text from outside-inside instead of extracting because the possible variations of hit die and the number of hit die 
    
    return int(hit_points), int(hit_dice_count), int(hit_dice)                                           # Variables are converted from string to int



def monster_speed(monster_soup):

    """Get Monster's air, land, and water speed"""

    speed = monster_soup.find("a", href=re.compile("Movement")).parent.next_sibling.get_text().strip(" ").split(",")       # Grabs all the modes of movement (ground, fly, and swim) and stores it in a list. Trims the items with strip().
    ground_speed = speed[0].rstrip(" ft.\n")                                         # Assigns ground speed with the first element of speed. Trims the units and 

    for mode in speed[1:3]:                                                          # Loops through the second and thirf mode of movement (if there are any) to see what kind of movement it is
        if ("swim" in mode) and ("fly" not in mode):
            swim_speed = mode.lstrip("swim ").rstrip(" ft.\n")                       # Each if statement determines if there is swim, fly, swim and fly, or neither then assigns it to the appropiate variable
            fly_speed = 0                                                            # Units and newlines are trimmed as well
        elif ("fly" in mode) and ("swim" not in mode):
            fly_speed = mode.lstrip("fly ").rstrip(" ft.\n")
            swim_speed = 0
        elif ("swim" and "fly") in mode:
            swim_speed = mode.lstrip("swim ").rstrip(" ft.\n")
            fly_speed = mode.lstrip("fly ").rstrip(" ft.\n")
        elif ("swim" and "fly") not in mode:
            swim_speed = 0
            fly_speed = 0
            
    return int(ground_speed), int(fly_speed), int(swim_speed)                        # Variables are converted from string to int



def monster_abilities(monster_soup):

    """Get Monster's ability scores and modifiers"""

    ability_score_and_mod = monster_soup.find("a", href=re.compile("Strength")).parent.parent.next_sibling.next_sibling.get_text().replace("\n", "")                                 # Grabs numerical data in the abilities table. Searches for the "Strength" href, then goes to next row to grab the data. Removes \n.
    scores = [int(score) for score in re.sub(r"\n|\(([^)]*)\)", "", ability_score_and_mod).strip().split(" ")]                                                                       # Puts score data in a list after removing modifier number that are in parenthesis.

    strength_score, dexterity_score, constitution_score, intelligence_score, wisdom_score, charisma_score = scores                                                               # Assign each score value in the scores list
    strength_modifier, dexterity_modifier, constitution_modifier, intelligence_modifier, wisdom_modifier, charisma_modifier = [math.floor(score / 2) - 5 for score in scores]    # Calculates the modifier for each score. I.e. 12 / 2 = 6, 6 - 5 = 1

    return strength_score, dexterity_score, constitution_score, intelligence_score, wisdom_score, charisma_score, strength_modifier, dexterity_modifier, constitution_modifier, intelligence_modifier, wisdom_modifier, charisma_modifier

"""
-------------------------------
Initailizaing Monster Dataframe
-------------------------------
"""

monster_df = pd.DataFrame(
    columns = [
        "monster_id",	
        "monster_name",	
        "size",	
        "body_type",	
        "alignment",	
        "ac",
        "natural_armor",
        "hit_points",	
        "hit_dice_count",
        "hit_dice",
        "ground_speed_ft",	
        "fly_speed_ft",	
        "swim_speed_ft",
        "strength_score",	
        "dexterity_score",	
        "constitution_score",	
        "intelligence_score",	
        "wisdom_score",	
        "charisma_score",
        "strength_modifier",
        "dexterity_modifier",
        "constitution_modifier",
        "intelligence_modifier",
        "wisdom_modifier",
        "charisma_modifier",
        "challenge_rating",	
        "passive_perception",	
        "blindsight",	
        "darkvision",	
        "tremosense",	
        "truesight",	
        "acid_damage",	
        "bludgeoning_damage",	
        "cold_damage",	
        "fire_damage",	
        "force_damage",	
        "lightning_damage",	
        "necrotic_damage",	
        "piercing_damage",	
        "poison_damage",	
        "psychic_damage",	
        "radiant_damage",	
        "slashing_damage",	
        "blinded",	
        "charmed",	
        "deafened",	
        "exhaustion",	
        "frightened",	
        "grappled",	
        "incapacitated",	
        "invisible",	
        "paralyzed",	
        "petrified",	
        "poisoned",	
        "prone",	
        "restrained",	
        "stunned",	
        "unconscious"
    ]
)

"""
------------------------------------
Get Webpage for the List of Monsters
------------------------------------
"""

response = requests.get("https://www.dandwiki.com/wiki/5e_Monsters")

if response.status_code == 200:                   # Checks that the connection to the webpage was established
    """Makes the HTML soup from the content of the response and assigns it to a variable"""
    monster_list_soup = BeautifulSoup(
        response.content,
        "html.parser"
    )          
else:
    print(response)                               # If not a good connection, prints response code

"""
-------------------------------
Get Hyperlinks for all Monsters
-------------------------------
"""

monster_href = []                                                                       # List to store each monster's hyperlink

for a in monster_list_soup.find_all("a", href=re.compile("\\(5e_Creature\\)")):         # Finds all <a> tags that have a hyperlink to a monster. The '\' allows the parenthesis to be recognized
    monster_href.append("https://dandwiki.com" + a["href"])                             # Adds the web address prefix to the href attribute and appends it to the monster_href list

"""
----------------------
Get Monster Attributes
----------------------
"""

response = requests.get(monster_href[0])

if response.status_code == 200:                                                   # Checks that the connection to the webpage was established
    soup = BeautifulSoup(response.content, "html.parser")                         # Makes the HTML soup from the content of the response and assigns it to variable MonsterName_soup
else:
    print(response)                                                               # If not a good connection, prints response code

monster_df.loc[1, "monster_id"] = 1

monster_df.loc[1, "monster_name"] = monster_name(soup)

monster_df.loc[1, ["size", "body_type", "alignment"]] = monster_size_type_alignment(soup)

monster_df.loc[1, ["ac", "natural_armor"]] = monster_ac_naturalarmor(soup)

monster_df.loc[1, ["hit_points", "hit_dice_count", "hit_dice"]] = monster_hp_hitdice_hitdicecount(soup)

monster_df.loc[1, ["ground_speed", "fly_speed", "swim_speed"]] = monster_speed(soup)

monster_df.loc[1, ["strength_score", "dexterity_score", "constitution_score", "intelligence_score", "wisdom_score", "charisma_score", "strength_modifier", "dexterity_modifier", "constitution_modifier", "intelligence_modifier", "wisdom_modifier", "charisma_modifier"]] = monster_abilities(soup)

monster_df

# print(soup.prettify())

