api-wow-python
==============

Script to get results for the WoW API ( http://blizzard.github.io/api-wow-docs/ )

## Introduction
This script is written to interract with the publicly accessible WoW API.
It was written for a quick glance at character information.

At the time this was written, the WoW EU auction house was not available therefore it was not implemented. Hopefully sometime soon the auction house functionality can be built in.

### Python Dependencies
Note: I only had to install these following dependencies, the others were already installed on my local python instance.
* Requests
  ```
  http://docs.python-requests.org/en/latest/user/install/
  ```
* BeautifulSoup
  ```
  http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
  ```
  
## Usage
```
λ ~/git/api-wow-docs/wow_api/ master* ./wow_api.py
 __      __      __      __                        .__
/  \    /  \____/  \    /  \         _____  ______ |__|
\   \/\/   /  _ \   \/\/   /  ______ \__  \ \____ \|  |
 \        (  <_> )        /  /_____/  / __ \|  |_> >  |
  \__/\  / \____/ \__/\  /   python  (____  /   __/|__|
       \/              \/                 \/|__|
                                              - @viljoenivan
Usage: wow_api.py -r <Realm> -c <Character Name> --cs <options>

WoW API functions (https://github.com/blizzard/api-wow-docs) - OneSockThief

Options:
  -h, --help            show this help message and exit
  -r REALM, --realm=REALM
                        Realm to search/filter by
  -c CHARACTER, --character=CHARACTER
                        Search for a character by name

  Supported functions:
    --cs, --charactersearch
                        Character search / Information
    --ah, --auctionsearch
                        Auction house search

  Detailed character information to use with Character Search (--cs):
    --guild             Guild information
    --items             Current equipped items
    --mounts            Current mounts collected
    --pvp               PvP stats
    --quests            Current active quests
    --reputation        Current reputation level of appropriate factions
    --stats             Currect character stats #pewpew
    --talents           Current talent progres
    --audit             Audit the character
```

##Sample output:
```
λ ~/ ./wow_api.py -c Tink -r outland --cs --reputation
 __      __      __      __                        .__
/  \    /  \____/  \    /  \         _____  ______ |__|
\   \/\/   /  _ \   \/\/   /  ______ \__  \ \____ \|  |
 \        (  <_> )        /  /_____/  / __ \|  |_> >  |
  \__/\  / \____/ \__/\  /   python  (____  /   __/|__|
       \/              \/                 \/|__|
                                              - @viljoenivan

Character search for Tink on outland

Realm: Outland
Name: Tink
Level: 100
Class: Druid
Race: Night Elf
Calc Class: U
Gender: Female
Achievement Points: 3900
Total Honorable Kills: 5894
Battlegroup: Misery
Last Modified: 2014-12-13 22:15:42
Thumbnail: http://eu.battle.net/static-render/eu/outland/43/117026603-avatar.jpg

	Reputation:
	The Silver Covenant               (lvl:3) 849  |███████                  | 3000
	The Wyrmrest Accord               (lvl:3) 455  |████                     | 3000
	The Black Prince                  (lvl:5) 549  |█                        | 12000
	Booty Bay                         (lvl:3) 1187 |██████████               | 3000
	Gilneas                           (lvl:4) 901  |████                     | 6000
	The Earthen Ring                  (lvl:4) 311  |█                        | 6000
	The Frostborn                     (lvl:3) 1564 |█████████████            | 3000
	Ironforge                         (lvl:4) 2351 |██████████               | 6000
	Argent Dawn                       (lvl:3) 200  |██                       | 3000
	Gnomeregan                        (lvl:4) 3588 |███████████████          | 6000
	Kirin Tor Offensive               (lvl:6) 3650 |████                     | 21000
	Darnassus                         (lvl:5) 3025 |██████                   | 12000
	Cenarion Circle                   (lvl:3) 2000 |█████████████████        | 3000
	Alliance Vanguard                 (lvl:4) 127  |█                        | 6000
	Silverwing Sentinels              (lvl:3) 784  |███████                  | 3000
	Stormwind                         (lvl:4) 4341 |██████████████████       | 6000
	Valiance Expedition               (lvl:3) 1564 |█████████████            | 3000
	Magram Clan Centaur               (lvl:3) 2000 |█████████████████        | 3000
	Gelkis Clan Centaur               (lvl:3) 2000 |█████████████████        | 3000
	Timbermaw Hold                    (lvl:2) 100  |█                        | 3000
	The Klaxxi                        (lvl:3) 1650 |██████████████           | 3000
	Everlook                          (lvl:3) 1118 |█████████                | 3000
	Gadgetzan                         (lvl:3) 1118 |█████████                | 3000
	Explorers' League                 (lvl:3) 1564 |█████████████            | 3000
	Honor Hold                        (lvl:3) 1199 |██████████               | 3000
	Cenarion Expedition               (lvl:4) 1592 |███████                  | 6000
	The Consortium                    (lvl:3) 2783 |███████████████████████  | 3000
	Exodar                            (lvl:4) 2251 |█████████                | 6000
	Council of Exarchs                (lvl:6) 190  |                         | 21000
	Shado-Pan                         (lvl:3) 2075 |█████████████████        | 3000
	Golden Lotus                      (lvl:3) 2098 |█████████████████        | 3000
	Arakkoa Outcasts                  (lvl:5) 5224 |███████████              | 12000
	The Ashen Verdict                 (lvl:5) 9087 |███████████████████      | 12000
	Hydraxian Waterlords              (lvl:4) 905  |████                     | 6000
	Steamwheedle Preservation Society (lvl:3) 1500 |█████████████            | 3000
	Ratchet                           (lvl:3) 1118 |█████████                | 3000
	Lower City                        (lvl:3) 2860 |████████████████████████ | 3000
	Ashtongue Deathsworn              (lvl:5) 4787 |██████████               | 12000
	Guild                             (lvl:7) 999  |█████████████████████████| 999
	Baradin's Wardens                 (lvl:4) 850  |████                     | 6000
	The League of Arathor             (lvl:4) 565  |██                       | 6000
	Keepers of Time                   (lvl:4) 332  |█                        | 6000
	Kurenai                           (lvl:2) 1800 |███████████████          | 3000
	Sporeggar                         (lvl:2) 500  |████                     | 3000
	Stormpike Guard                   (lvl:5) 414  |█                        | 12000
	Wrynn's Vanguard                  (lvl:3) 1704 |██████████████           | 3000
	Avengers of Hyjal                 (lvl:3) 325  |███                      | 3000
```

MIT License = share and commit :)

Twitter: (at) viljoenivan
