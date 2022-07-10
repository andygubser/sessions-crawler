import pandas as pd
import requests
import xml.etree.ElementTree as ET


def loadRSS(url):
    # url of rss feed

    # creating HTTP response object from given url
    resp = requests.get(url)

    # saving the xml file
    with open('geschaefte_feed.xml', 'wb') as f:
        f.write(resp.content)


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for deals items
    deals_items = []

    # iterate deals items
    for item in root.findall('./channel/item'):

        # empty deals dictionary
        deals = {}

        # iterate child elements of item
        for child in item:
            print(child.tag)
            print(type(child.tag))

            deals[child.tag] = child.text

        # append deals dictionary to deals items list
        deals_items.append(deals)

    # return deals items list
    return deals_items


def get_feed(url):
    # calling main function
    # load rss from web to update existing xml file
    loadRSS(url=url)

    # parse xml file
    df_geschaefte_feed = parseXML('geschaefte_feed.xml')

    df = pd.DataFrame(df_geschaefte_feed)
    df.to_excel("geschaefte_feed.xlsx")
    return df
