import requests
import pandas as pd
from requests_html import HTML, HTMLSession


def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_feed(url):
    """Return a Pandas dataframe containing the RSS feed contents.

    Args:
        url (string): URL of the RSS feed to read.

    Returns:
        ls_dfs_affairs (dataframe): Pandas dataframe containing the RSS feed contents.
    """

    response = get_source(url)

    df = pd.DataFrame(columns=['title', 'link', 'pubDate', 'guid', 'description'])

    with response as r:
        print(r.html)
        items = r.html.find("item", first=False)

        for item in items:
            print(item.text)

        for item in items:
            title = item.find('title', first=True).text
            link = item.find('link', first=True).text
            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text.replace("<![CDATA[", "").replace("]]>", "")
            description = item.find('description', first=True).text.replace("<![CDATA[", "").replace("]]>", "")

            row = {
                'title': [title],
                'link': [link],
                'pubDate': [pubDate],
                'guid': [guid],
                'description': [description]
            }

            df_new = pd.DataFrame.from_dict(row)

            df = pd.concat([df, df_new], ignore_index=True)

    return df
