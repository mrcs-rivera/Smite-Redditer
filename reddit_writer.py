__author__ = 'marcus'

import pymongo


def create_reddit_post(god_name):
    god_coll = pymongo.MongoClient().smite.gods
    god = god_coll.find_one({"god": god_name})
    reddit_post = \
        "**[" + god["god"] + "](http://smite.gamepedia.com/" + god["god"].replace(' ', '-') + "), " \
        + god["stats"]["title"] + "**\n\n"  \
        "*Note: these posts are not updated over time. The posts and their discussions are meant to be a reflection of " \
        "the metagame at the time of post.*\n\n" \
        + god["stats"]["pantheon"] + "\n\n" \
        + god["stats"]["type"] + "\n\n" \
        + god["stats"]["class"] + "\n\n" \
        + god["stats"]["pros"] + "\n\n" \
        "**Lore**\n\n" \
        + god["lore"] + "\n" \
        "~~==~~\n\n" \
        "**Stats** (Numbers in parentheses are the amount gained per level. Rankings are *italicized*, are based on " \
        "[this spreadsheet](https://docs.google.com/spreadsheets/d/15HqX3_rmU5ZeJpOi2ls3pp-_vYsAqJBDfqc8Z-XmmGA" \
        "/edit#gid=0), and assume level 20. If not noted, than not in the top or bottom 10.)\n\n" \
        + god["stats"]["health"] + "\n\n" \
        + god["stats"]["mana"] + "\n\n" \
        "Movement " + god["stats"]["speed"] + "\n\n" \
        + god["stats"]["range"] + "\n\n" \
        + god["stats"]["att/s"] + "\n\n" \
        "Basic Attack " + god["stats"]["damage"] + "\n\n" \
        + god["stats"]["progression"] + "\n\n" \
        + god["stats"]["physical"][:8] + " Protection" + god["stats"]["physical"][8:] + "\n\n" \
        + god["stats"]["magical"][:7] + " Protection" + god["stats"]["physical"][8:] + "\n\n" \
        + god["stats"]["hp5"] + "\n\n" \
        + god["stats"]["mp5"] + "\n\n" \
        "~~==~~\n\n" \
        "**Passive**\n\n" \
        + god["abilities"]["passive"].get("name", "") + "\n\n" \
        + god["abilities"]["passive"].get("description", "") + "\n\n" \
        "**Skills**\n\n" \
        "Slot|Name|Mana cost|Cooldown|Description\n" \
        ":---|:---|:---|:---|:\n" \
        "1| " + god["abilities"]["abil1"].get("name", "") + " | " + god["abilities"]["abil1"].get("cost", "0") + " | " \
        + god["abilities"]["abil1"].get("cooldown", "0") + " | " + god["abilities"]["abil1"].get("description", "") + "\n" \
        "2| " + god["abilities"]["abil2"].get("name", "") + " | " + god["abilities"]["abil2"].get("cost", "0") + " | " \
        + god["abilities"]["abil2"].get("cooldown", "0") + " | " + god["abilities"]["abil2"].get("description", "") + "\n" \
        "3| " + god["abilities"]["abil3"].get("name", "") + " | " + god["abilities"]["abil3"].get("cost", "0") + " | " \
        + god["abilities"]["abil3"].get("cooldown", "0") + " | " + god["abilities"]["abil3"].get("description", "") + "\n" \
        "4 (Ultimate)| " + god["abilities"]["abil4"].get("name", "") + " | " + god["abilities"]["abil4"].get("cost", "0") + " | " \
        + god["abilities"]["abil4"].get("cooldown", "0") + " | " + god["abilities"]["abil4"].get("description", "") + "\n\n" \
        "~~==~~\n\n" \
        "**Points of Discussion**\n\n" \
        "What items are particularly effective on this god?\n\n" \
        "What mistakes do you see commonly made with this god?\n\n" \
        "What play style is most effective with this god?\n\n" \
        "Do you disagree with any recommended items, or common builds?\n\n" \
        "What is the best way to counter or compliment this god?\n\n" \
        "Do you know of any high level players who are particularly good with this god? " \
        "(If so, you should invite him/her to this thread!)\n\n" \
        "**View all previous discussions [here](http://www.reddit.com/search?q=today%27s+discussion+subreddit%3Asmite+" \
        "author%3Anaterspotaters&amp;sort=new&amp;t=all).**\n\n" \
        "**Stats are based on [this spreadsheet](https://docs.google.com/spreadsheets/d/15HqX3_rmU5ZeJpOi2ls3pp-_vY" \
        "sAqJBDfqc8Z-XmmGA/edit#gid=0).**\n\n" \

    txt = open(god_name + ".txt", 'w')
    txt.write(reddit_post.encode('utf-8'))
    txt.close()