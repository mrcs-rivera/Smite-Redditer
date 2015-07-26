__author__ = 'marcus'

import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from socket import error as socket_error
import pymongo
from progressbar import ProgressBar, Percentage, Bar
from datetime import datetime, timedelta
import time
from xvfbwrapper import Xvfb


def web_scrapper():
    god_coll = pymongo.MongoClient().smite.gods
    Xvfb().start()
    chromedriver = os.path.dirname(os.path.realpath('chromedriver')) + '/chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver)
    driver.set_page_load_timeout(30)

    print "Please wait, this could take several minutes."

    # Grab up to date list of Smite gods
    driver = load_url(driver, chromedriver, "http://www.smitegame.com/gods/")
    gods = driver.find_elements_by_xpath("//a[@class='icon-container']")
    god_names = []
    for god in gods:
        god_names.append(god.get_attribute('data-name').encode('utf-8'))

    # Gather info on each god and store in mongo
    b = 0
    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), Percentage()], maxval=len(god_names)).start()
    for god in god_names:
        cached = god_coll.find_one({'god': god})
        if cached and ((datetime.now()) - cached['lastupdated']) < timedelta(days=1):
            # Update progress bar
            b += 1
            pbar.update(b)
        else:
            # Get god abilities from official website
            driver = load_url(driver, chromedriver, "http://www.smitegame.com/gods/" + god.replace(' ', '-'))
            
            # Scrap and parse god abilities
            tmp = driver.find_elements_by_xpath("//div[@class='single-ability']")
            info = []
            for t in tmp:
                if t.text != '':
                    info.append(t)
            passive = {}
            abil1 = {}
            abil2 = {}
            abil3 = {}
            abil4 = {}
            abilities = [abil1, abil2, abil3, abil4]
            i = 0
            for inf in info:
                texts = inf.find_elements_by_xpath(".//div")
                if "(Passive)" in texts[2].text:
                    passive['name'] = texts[2].text.encode('utf-8')[:-10]
                    passive['description'] = texts[3].text.encode('utf-8')
                else:
                    abilities[i]['name'] = texts[2].text.encode('utf-8')
                    abilities[i]['description'] = texts[3].text.encode('utf-8')
                    for j in range(4, len(texts)):
                        if 'Cost' in texts[j].text:
                            abilities[i]['cost'] = texts[j].text.encode('utf-8')[6:]
                        elif 'Cooldown' in texts[j].text:
                            abilities[i]['cooldown'] = texts[j].text.encode('utf-8')[10:]
                    i += 1

            # Get god Lore and stats from third party smite wiki
            driver = load_url(driver, chromedriver, "http://smite.gamepedia.com/" + god.replace(' ', '_'))
            
            # Scrap and parse god lore 
            info = scrap_info(driver, "//p", 99999)
            lore = ""
            for i in info[:-15]:
                if len(i) > 120:
                    lore = lore + i + '\n'
                if 'Ability Video' in i:
                    break
            
            # Scrap and parse god stats
            info = scrap_info(driver, "//tr", 1500)
            stats = {}
            for i in range(0, len(info)):
                if 'Title:' in info[i] and 'title' not in stats:
                    stats['title'] = info[i][7:]
                elif 'Pantheon:' in info[i] and 'pantheon' not in stats:
                    stats['pantheon'] = info[i]
                elif 'Type:' in info[i] and 'type' not in stats:
                    stats['type'] = info[i]
                elif 'Class:' in info[i] and 'class' not in stats:
                    stats['class'] = info[i]
                elif 'Pros:' in info[i] and 'pros' not in stats:
                    stats['pros'] = info[i]
                elif 'Health:' in info[i] and 'health' not in stats:
                    stats['health'] = info[i]
                elif 'Mana:' in info[i] and 'mana' not in stats:
                    stats['mana'] = info[i]
                elif 'Speed:' in info[i] and 'speed' not in stats:
                    stats['speed'] = info[i]
                elif 'Range:' in info[i] and 'range' not in stats:
                    stats['range'] = info[i]
                elif 'Attack/Sec:' in info[i] and 'att' not in stats:
                    stats['att/s'] = info[i]
                elif 'Damage:' in info[i] and 'damage' not in stats:
                    stats['damage'] = info[i]
                elif 'Progression:' in info[i] and 'progression' not in stats:
                    stats['progression'] = info[i]
                elif 'Physical:' in info[i] and 'physical' not in stats:
                    stats['physical'] = info[i]
                elif 'Magical:' in info[i] and 'magical' not in stats:
                    stats['magical'] = info[i]
                elif 'HP5:' in info[i] and 'hp5' not in stats:
                    stats['hp5'] = info[i]
                elif 'MP5:' in info[i] and 'mp5' not in stats:
                    stats['mp5'] = info[i]

            # Create mongo document
            doc = {'god': god, 'stats': stats, 'lore': lore, 'abilities':
                {'passive': passive,
                 'abil1': abil1,
                 'abil2': abil2,
                 'abil3': abil3,
                 'abil4': abil4},
                 'lastupdated': datetime.now()}
            
            # Store/Update mongo document
            god_coll.update({'god': doc['god']}, doc, True)
            
            # Update progress bar
            b += 1
            pbar.update(b)
    try:
        driver.quit()
    except:
        pass
    Xvfb().stop()
    print "\nDone!\n"


def load_url(driver, chromedriver, url):
    loaded = False
    while not loaded:
        try:
            driver.get(url)
        except TimeoutException:
            time.sleep(5)
        except socket_error:
            driver = webdriver.Chrome(executable_path=chromedriver)
            driver.set_page_load_timeout(30)
        except:
            try:
                driver.quit()
            except:
                pass
            driver = webdriver.Chrome(executable_path=chromedriver)
            driver.set_page_load_timeout(30)
        else:
            loaded = True
    return driver


def scrap_info(driver, xpath, len_delim):
    scrapped = False
    info = []
    while not scrapped:
        try:
            tmp = driver.find_elements_by_xpath(xpath)
            for t in tmp:
                if t.text != '' and len(t.text) < len_delim:
                    info.append(t.text.encode('utf-8'))
        except TimeoutException:
            scrapped = False
        else:
            scrapped = True
    return info

