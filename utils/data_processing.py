from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
 

teams = ['TOR', 'BAL', 'TB', 'BOS', 'NYY', 
         'CLE', 'KC', 'DET', 'MIN', 'CWS', 
         'LAA', 'HOU', 'OAK', 'SEA', 'TEX',
         'ATL', 'MIA', 'NYM', 'WSH', 'PHI',
         'MIL', 'STL', 'CHC', 'PIT', 'CIN',
         'AZ', 'LAD', 'SF', 'SD', 'COL']

glossary = ['pitch_type', 'release_pos_x', 'release_pos_z', 'pitcher',
            'description', 'stand', 'pfx_x', 'pfx_z', 'plate_x', 'plate_z',
            'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'release_pos_y']


def data_crawler():
    options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(os.path.join(os.getcwd(), ".."))+"\data",
        "savefile.default_directory": os.path.abspath(os.path.join(os.getcwd(), ".."))+"\data"
    }
    options.add_experimental_option("prefs", prefs)
    
    chrome = webdriver.Chrome(options=options)
    chrome.get("https://baseballsavant.mlb.com/statcast_search")

    for team in teams:
        time.sleep(1)
        team_list = chrome.find_element(By.XPATH, "//div[@class='mock-pulldown-inner'][@id='ddlTeam']/div")
        team_list.click()
        select_team = chrome.find_element(By.ID, "chk_Team_"+team)
        select_team.click()
        search_button = chrome.find_element(By.XPATH, "//input[@class='btn btn-default btn-search-green'][@type='submit']")
        search_button.click()
        time.sleep(3)
        chrome.find_element(By.ID, "csv_all_pid_").click()
        time.sleep(1)
        
        os.chdir("../data")
        latest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[-1]
        while True:
            if not latest_file.endswith(".crdownload"):
                os.rename(latest_file, team+".csv")
            break
        print(team, "downloaded")

        clear_button = chrome.find_element(By.ID, "btnClear")
        clear_button.click()


def data_classifier():
    os.chdir("../data")
    for team_csv in os.listdir(os.getcwd()):
        raw_data = pd.read_csv(team_csv)
        necessary_data = raw_data[glossary]
        


if __name__ == "__main__":
    # data_crawler()
    data_classifier()
