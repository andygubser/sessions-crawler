import os
import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from scripts.scrape_details_into_dataframe import scrape_details_into_dataframe
from scripts.xml_parser import get_feed

# use vpn located in switzerland

path_project = r"G:\My Drive\glpbe\kantonale_geschaefte_bern"
os.chdir(path_project)

if __name__ == "__main__":
    # get urls from feed
    url_feed = "https://www.rrgr-service.apps.be.ch/api/gr/instances/1796b1af-bd1e-4ffa-a80d-ba08d1b8a2ed/render?guid=&lang=de"
    df_feed = get_feed(url=url_feed)
    ls_urls_affairs = df_feed["guid"].unique().tolist()

    # selenium - scrape table
    options = FirefoxOptions()
    options.headless = False

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                               options=options)

    ls_dfs_affairs = []

    # TODO: loop is currently limited to 10 affairs
    for url in ls_urls_affairs[:10]:
        df_affair = scrape_details_into_dataframe(driver=driver, url=url)
        ls_dfs_affairs.append(df_affair)

    driver.quit()

    # append dataframes
    df_affairs = pd.concat(ls_dfs_affairs)
    df_affairs.to_excel("data/kantonale_geschäfte.xlsx")
