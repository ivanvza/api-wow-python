#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys
import datetime
import optparse
import urllib
from bs4 import BeautifulSoup
import textwrap

options = optparse.OptionParser(usage='%prog -r <Realm> -c <Character Name> --cs <options>', description='WoW API functions (https://github.com/blizzard/api-wow-docs) - OneSockThief')

#Functions
options_functions = optparse.OptionGroup(options, 'Supported functions')
options_functions.add_option('--cs', '--charactersearch', action="store_true", dest='charactersearch', help='Character search / Information')
options_functions.add_option('--ah', '--auctionsearch', action="store_true", dest='auctionsearch', help='Auction house search')
options.add_option_group(options_functions)

#Required parameters for other functions
options.add_option('-r', '--realm', type='string', dest='realm', help='Realm to search/filter by')
options.add_option("-c", "--character", type='string', dest="character", help="Search for a character by name")

#Smaller functions, for character details
character_group = optparse.OptionGroup(options, 'Detailed character information to use with Character Search (--cs)')
character_group.add_option("--guild", action="store_true", dest="guild", help="Guild information")
character_group.add_option("--items", action="store_true", dest="items", help="Current equipped items")
character_group.add_option("--mounts", action="store_true", dest="mounts", help="Current mounts collected")
character_group.add_option("--pvp", action="store_true", help="PvP stats")
character_group.add_option("--quests", action="store_true", dest="quests", help="Current active quests")
character_group.add_option("--reputation", action="store_true", dest="reputation", help="Current reputation level of appropriate factions")
character_group.add_option("--stats", action="store_true", dest="stats", help="Currect character stats #pewpew")
character_group.add_option("--talents", action="store_true", dest="talents", help="Current talent progres")
character_group.add_option("--audit", action="store_true", dest="audit", help="Audit the character")
options.add_option_group(character_group)

base_url = "http://eu.battle.net/api/wow"

def check_sub_character_options():
    requests = []
    if opts.guild:
        requests.append('guild')
    if opts.items:
        requests.append('items')
    if opts.mounts:
        requests.append('mounts')
    if opts.pvp:
        requests.append('pvp')
    if opts.quests:
        requests.append('quests')
    if opts.reputation:
        requests.append('reputation')
    if opts.stats:
        requests.append('stats')
    if opts.talents:
        requests.append('talents')
    if opts.audit:
        requests.append('audit')
    return requests

def query_api(url):
    try:
        s = requests.get(url).json()
        pass
    except Exception:
        #raise e
        pass
    try:
        if s["reason"]:
            print("ERROR: " + s["reason"])
            sys.stop()
    except:
        return s

def auction_house(realm):
    print("THIS SECTION IS BROKEN, EU AUCTION HOUSE IS MIA!")
    return
    url = base_url + "/api/wow/auction/data/" + realm
    s = query_api(url)
    print(s)

def character_male_female(n):
    if n == 0:
        return "Male"
    if n == 1:
        return "Female"

def character_class(n):
    url = base_url + "/data/character/classes"
    classes = query_api(url)
    for cclass in classes['classes']:
        if cclass['id'] == n:
            return cclass['name']

def character_race(n):
    url = base_url + "/data/character/races"
    races = query_api(url)
    for craces in races['races']:
        if craces['id'] == n:
            return craces['name']

def character_search(name, realm):
    fields = check_sub_character_options()
    url = base_url + "/character"
    print("\nCharacter search for " + name + " on " + realm + "\n")
    url = url + "/" + realm.title()
    url = url + "/" + name.title()
    #See if any sub fields are queried
    if fields:
        fields = ",".join(fields)
        url = url + "?fields=" + fields
    #Try and request the data from the API
    s = query_api(url)
    parse_char_info(s)
    #print(EXTRA INFO AT THE BOTTOM:
    if opts.guild:
        character_guild(s)
    if opts.items:
        character_items(s)
    if opts.mounts:
        character_mounts(s)
    if opts.pvp:
        character_pvp(s)
    if opts.quests:
        character_quests(s)
    if opts.reputation:
        character_reputation(s)
    if opts.stats:
        character_stats(s)
    if opts.talents:
        character_talents(s)
    if opts.audit:
        character_audit(s)

def parse_char_info(char_api_data):
    print("Realm: " + str(char_api_data["realm"]))
    print("Name: " + str(char_api_data["name"]))
    print("Level: " + str(char_api_data["level"]))
    print("Class: " + character_class(char_api_data["class"]))
    print("Race: " + character_race(char_api_data["race"]))
    print("Calc Class: " + str(char_api_data["calcClass"]))
    print("Gender: " + character_male_female(char_api_data["gender"]))
    print("Achievement Points: " + str(char_api_data["achievementPoints"]))
    print("Total Honorable Kills: " + str(char_api_data["totalHonorableKills"]))
    print("Battlegroup: " + str(char_api_data["battlegroup"]))
    print("Last Modified: " + str(datetime.datetime.fromtimestamp(char_api_data["lastModified"]/1000).strftime('%Y-%m-%d %H:%M:%S')))
    print("Thumbnail: http://eu.battle.net/static-render/eu/" + str(char_api_data["thumbnail"]))

def character_reputation(s):
    print("\n\tReputation:")
    names = []
    for long_names in s["reputation"]:
        if (long_names["value"] != 0) and (long_names["standing"] > 0):
            names.append(long_names["name"])
    longest = len(max(names, key=len))
    for reps in s["reputation"]:
        minimum = str(reps["value"])
        for x in range(3,5):
            if len(minimum) < x:
                minimum = minimum + " "
        if (reps["value"] != 0) and (reps["standing"] > 0):
            bar_length = 25
            bar = reps["name"]
            calc = round(float(reps["value"]) / float(reps["max"]) * bar_length)
            empty = bar_length - calc #This is the length of the BAR
            calculate_empty_spaces = longest - len(bar)
            line = u'█'
            bar = bar + " "*calculate_empty_spaces + " (lvl:" + str(reps["standing"]) + ") " + minimum + " |" + line*int(calc) + " "*int(empty) + "| " + str(reps["max"])
            print("\t" + bar)

def character_guild(s):
    print("\n\tGuild:")
    guild_info = s["guild"]
    print("\tName: " + guild_info["name"])
    print("\tTotal Achievement Points: " + str(guild_info["achievementPoints"]))
    print("\tTotal Members: " + str(guild_info["members"]))

def character_pvp(s):
    twovtwo = s["pvp"]["brackets"]["ARENA_BRACKET_2v2"]
    threevthree = s["pvp"]["brackets"]["ARENA_BRACKET_3v3"]
    fivevfive = s["pvp"]["brackets"]["ARENA_BRACKET_5v5"]
    RBG = s["pvp"]["brackets"]["ARENA_BRACKET_RBG"]
    print("\n\tPvP Ratings:")
    print("\t2v2:")
    print("\t\tRating: " + str(twovtwo["rating"]))
    print("\t\tSeason Won:  " + str(twovtwo["seasonWon"]))
    print("\t\tSeason Played: " + str(twovtwo["seasonPlayed"]))
    print("\t\tWeekly Won: " + str(twovtwo["weeklyWon"]))
    print("\t\tWeekly Played " + str(twovtwo["weeklyPlayed"]))
    print("\t3v3: ")
    print("\t\tRating: " + str(threevthree["rating"]))
    print("\t\tSeason Won:  " + str(threevthree["seasonWon"]))
    print("\t\tSeason Played: " + str(threevthree["seasonPlayed"]))
    print("\t\tWeekly Won: " + str(threevthree["weeklyWon"]))
    print("\t\tWeekly Played " + str(threevthree["weeklyPlayed"]))
    print("\t5v5: ")
    print("\t\tRating: " + str(fivevfive["rating"]))
    print("\t\tSeason Won:  " + str(fivevfive["seasonWon"]))
    print("\t\tSeason Played: " + str(fivevfive["seasonPlayed"]))
    print("\t\tWeekly Won: " + str(fivevfive["weeklyWon"]))
    print("\t\tWeekly Played " + str(fivevfive["weeklyPlayed"]))
    print("\tRated BG: ")
    print("\t\tRating: " + str(RBG["rating"]))
    print("\t\tSeason Won:  " + str(RBG["seasonWon"]))
    print("\t\tSeason Played: " + str(RBG["seasonPlayed"]))
    print("\t\tWeekly Won: " + str(RBG["weeklyWon"]))
    print("\t\tWeekly Played " + str(RBG["weeklyPlayed"]))

def character_items(s):
    all_items = s["items"]
    print("\n\tItems:")
    print("\tHead: " + str(all_items["head"]["name"]) + " ilvl: " + str(all_items["head"]["itemLevel"]))
    print("\tShoulders: " + str(all_items["shoulder"]["name"]) + " ilvl: " + str(all_items["shoulder"]["itemLevel"]))
    print("\tNeck: " + str(all_items["neck"]["name"]) + " ilvl: " + str(all_items["neck"]["itemLevel"]))
    print("\tBack: " + str(all_items["back"]["name"]) + " ilvl: " + str(all_items["back"]["itemLevel"]))
    print("\tFeet: " + str(all_items["feet"]["name"]) + " ilvl: " + str(all_items["feet"]["itemLevel"]))
    print("\tWrist: " + str(all_items["wrist"]["name"]) + " ilvl: " + str(all_items["wrist"]["itemLevel"]))
    print("\tMain Hand: " + str(all_items["mainHand"]["name"]) + " ilvl: " + str(all_items["mainHand"]["itemLevel"]))
    print("\tOff Hand:" + str(all_items["head"]["name"]) + " ilvl: " + str(all_items["head"]["itemLevel"]))
    print("\tHands: " + str(all_items["hands"]["name"]) + " ilvl: " + str(all_items["hands"]["itemLevel"]))
    print("\tLegs: " + str(all_items["legs"]["name"]) + " ilvl: " + str(all_items["legs"]["itemLevel"]))
    print("\tWaist: " + str(all_items["waist"]["name"]) + " ilvl: " + str(all_items["waist"]["itemLevel"]))
    print("\tFinger 1: " + str(all_items["finger1"]["name"]) + " ilvl: " + str(all_items["finger1"]["itemLevel"]))
    print("\tFinger 2: " + str(all_items["finger2"]["name"]) + " ilvl: " + str(all_items["finger2"]["itemLevel"]))
    print("\tTrinket 1: " + str(all_items["trinket1"]["name"]) + " ilvl: " + str(all_items["trinket1"]["itemLevel"]))
    print("\tTrinket 2: " + str(all_items["trinket2"]["name"]) + " ilvl: " + str(all_items["trinket2"]["itemLevel"]))
    print("\tAverage ilvl: " + str(all_items["averageItemLevel"]))
    print("\tAverage ilvl Equipped: " + str(all_items["averageItemLevelEquipped"]))

def character_mounts(s):
    mounts = s["mounts"]["collected"]
    print("\n\tMounts Collected:")
    for mount in mounts:
        print("\t" + mount["name"])

def character_quests(s):
    quests = s["quests"]
    print("\n\tQuests:")
    quest_continue = query_yes_no("\tThis can take some time, do you want to continue?", None)
    if quest_continue == "yes":
        for quest in quests:
            quest_url = "http://www.wowhead.com/quest=" + str(quest)
            #Lets do something for the user, and warn him this might take long, because were grabbing the title etc.
            soup = BeautifulSoup(urllib.urlopen(quest_url))
            quest_name = soup.title.string.split('-')
            print("\t" + quest_name[0] + "(http://www.wowhead.com/quest=" + str(quest) + ")")
    else:
        return

def character_stats(s):
    stats = s["stats"]
    longest_stat_name = []
    for long_name in stats:
            longest_stat_name.append(long_name)
    longest_stat_name = len(max(longest_stat_name, key=len))
    spacing = 30
    spacing = spacing - longest_stat_name
    print("\n\tStats:")
    print("\t------Attributes------\r")
    print("\tHealth: " + str(stats["health"]))
    print("\tStrength: " + str(stats["str"]))
    print("\tAgility: " + str(stats["agi"]))
    print("\tIntellect: " + str(stats["int"]))
    print("\tStamina: " + str(stats["sta"]))
    print("\tPowertype: " + str(stats["powerType"]))
    print("\tPower: " + str(stats["power"]))
    print("\tAttack Power: " + str(stats["attackPower"]))
    print("\t------Attack------\r")
    print("\tMain hand dps: " + str(stats["mainHandDps"]))
    print("\tMain Hand DMG Max: " + str(stats["mainHandDmgMax"]))
    print("\tMain hand DMG Min: " + str(stats["mainHandDmgMin"]))
    print("\tMainhand Speed: " + str(stats["mainHandSpeed"]))
    print("\tOff-Hand DPS: " + str(stats["offHandDps"]))
    print("\tOff-Hand DMG Max: " + str(stats["offHandDmgMax"]))
    print("\tOff-Hand DMG Min: " + str(stats["offHandDmgMin"]))
    print("\tOff-Hand Speed: " + str(stats["offHandSpeed"]))
    print("\t------Spell------\r")
    print("\tSpell Power: " + str(stats["spellPower"]))
    print("\tSpell Crit: " + str(stats["spellCrit"]))
    print("\tSpell Penetration: " + str(stats["spellPen"]))
    print("\tMana Regen in Combat: " + str(stats["mana5Combat"]))
    print("\tMana Regen outside Combat: " + str(stats["mana5"]))
    print("\t------Defence------\r")
    print("\tArmor: " + str(stats["armor"]))
    print("\tDodge: " + str(stats["dodge"]) + "%")
    print("\tParry: " + str(stats["parry"]) + "%")
    print("\tBlock: " + str(stats["block"]) + "%")
    print("\t------Enhancements------\r")
    print("\tCrit: " + str(stats["crit"]) + "%")
    print("\tHaste: " + str(stats["haste"]) + "%")
    print("\tMastery: " + str(stats["mastery"]) + "%")
    print("\tSpirit: " + str(stats["spr"]))
    print("\tBonus Armor: " + str(stats["bonusArmor"]))
    print("\tMultistrike: " + str(stats["multistrike"]) + "%")
    print("\tVersatility: " + str(stats["versatility"]) + "%")
    print("\tLeech: " + str(stats["leech"]) + "%")
    print("\tAvoidance Rating: " + str(stats["avoidanceRating"]) + "%")

def character_talents(s):
    print("\n\tTalents:")
    for talent in s["talents"]:
        try:
            if talent["selected"]:
                print("\tActive Talent:")
        except:
            print("\n\tSecondary Talent:")
        for tier in talent["talents"]:
            print("\tTier " + str(tier["tier"]+1))
            print("\t\tName: " + tier["spell"]["name"])
            print("\t\tCast Time: " + tier["spell"]["castTime"])
            try:
                if tier["spell"]["powerCost"]:
                    print("\t\tPower Cost: " + tier["spell"]["powerCost"])
            except:
                pass
            spell_description = "\t\tDescription: " + tier["spell"]["description"].replace("\n","")
            print("\n\t\t".join(textwrap.wrap(spell_description, 64)))

def character_audit(s):
    print("\n\tCharacter Audit:")
    if s["audit"]["missingLeatherworkerEnchants"] != {}:
        print("\tLeather Worker Enchants Missing:")
        for missing_leatherworker_enchant in s["audit"]["missingLeatherworkerEnchants"]:
            print("\t\t" + s["audit"]["missingLeatherworkerEnchants"])
    if s["audit"]["emptyGlyphSlots"] > 0:
        print("\tTotal Empty Glyph Slots: " + str(s["audit"]["emptyGlyphSlots"]))
    if s["audit"]["itemsWithEmptySockets"] != {}:
        print("\tItems With Empty Sockets:")
        for empty_sockets in s["audit"]["itemsWithEmptySockets"]:
            print("\t\tItem: " + empty_sockets)
    if s["audit"]["missingExtraSockets"] != {}:
        print("\tItems Missing Extra Sockets:")
        for missing_sockets in s["audit"]["missingExtraSockets"]:
            print("\t\tItem: " + missing_sockets)
    if s["audit"]["emptySockets"] > 0:
        print("\tTotal Empty Sockets: " + str(s["audit"]["emptySockets"]))
    if s["audit"]["recommendedBeltBuckle"] != {}:
        buckle_description = "Description: " + s["audit"]["recommendedBeltBuckle"]["itemSpells"][0]["spell"]["description"].replace("\n","")
        print("\tRecommended Belt Buckle: ")
        print("\t\t" + str(s["audit"]["recommendedBeltBuckle"]["itemSpells"][0]["spell"]["name"]) + " (" + buckle_description + ")")
    if s["audit"]["unenchantedItems"] != {}:
        print("\tUnenchanted Items:")
        for unenchanted_item in s["audit"]["unenchantedItems"]:
            print("\t\tItem: " + unenchanted_item)
    if s["audit"]["numberOfIssues"] > 0:
        print("\tNumber of Issues: " + str(s["audit"]["numberOfIssues"]))
    if s["audit"]["noSpec"]:
        print("No Spec Detected!")

def query_yes_no(question, default="yes"):
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
            "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("\tinvalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("\tPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

def main():
    print( " __      __      __      __                        .__ ")
    print( "/  \    /  \____/  \    /  \         _____  ______ |__|")
    print( "\   \/\/   /  _ \   \/\/   /  ______ \__  \ \____ \|  |")
    print( " \        (  <_> )        /  /_____/  / __ \|  |_> >  |")
    print( "  \__/\  / \____/ \__/\  /   python  (____  /   __/|__|")
    print( "       \/              \/                 \/|__|       ")
    print( "                                              - @viljoenivan")

    global opts
    opts, args = options.parse_args()
    if len(sys.argv) == 1:
        options.print_help()
        return

    #Character stuff
    if opts.charactersearch:
        if opts.character and opts.realm:
            character_search(opts.character, opts.realm)

    #Auction House
    if opts.auctionsearch:
        if opts.realm:
            auction_house(opts.realm)

if __name__ == '__main__':
    main()