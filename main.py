__author__ = 'marcus'

from Scrapper import web_scrapper
from reddit_writer import create_reddit_post
import pymongo


def main():
    god_coll = pymongo.MongoClient().smite.gods

    print "============================================================\n\n"
    print "       Welcome to the Smite Reddit Post Creator!\n\n"
    print "  --------------------------------------------------------  \n\n"

    while True:
        print "    Please choose from the following options:"
        if god_coll.count() == 0:
            empty = True
            print "    MongoDB is empty:"
            print "    |populate| Populate MongoDB with god stats."
            print "        |exit| Exit Program."
        else:
            empty = False
            print "    |update| Update MongoDB (Individual gods can only be updated once every 24 hours)"
            print "       |one| Create Reddit Post for one."
            print "       |all| Create Reddit Posts for all."
            print "      |exit| Exit Program."

        choice = raw_input("\n    What do you want to do? ")

        if choice == "populate" or choice == "update":
            web_scrapper()
        elif choice == "one" and not empty:
            god_choice = raw_input("        Which god do you want? ")
            print god_choice
            god = god_coll.find_one({"god": god_choice.title()})
            if not god:
                print "    Invalid god!"
            else:
                create_reddit_post(god_choice.title())
                print "\n\n    Text File Created!\n"
        elif choice == "all" and not empty:
            gods = god_coll.find()
            for god in gods:
                create_reddit_post(god["god"])
            print "\n    All Text Files Createdn\n"
        elif choice == "exit":
            print "\n\n  GOODBYE!\n"
            break
        else:
            print "    Invalid Choice!\n"

main()