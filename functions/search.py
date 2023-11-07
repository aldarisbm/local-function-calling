import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
search_api_key = os.getenv("SEARCH_API_KEY")
cx_key = os.getenv("CX_KEY")
SEARCH_API_URL = os.getenv("SEARCH_API_URL", 'https://www.googleapis.com/customsearch/v1')


def search_google(query: str, **kwargs: dict) -> list[dict]:
    """
    Returns the result from the Google Search API
    Args:
        query (str): The query to search for.
        kwargs (dict): The keyword arguments to pass to the search API, this could be empty.
    Returns:
        list[dict]:  A list of python dictionaries containing the search results.

    Examples:
        >>> search_google(query='What is young sheldon?')
        [
            {'title': 'Young Sheldon - Wikipedia', 'link': 'https://en.wikipedia.org/wiki/Young_Sheldon', 'snippet': 'The series, set in the late 1980s and early 1990s, is a spin-off prequel to The Big Bang Theory and follows main character Sheldon Cooper growing up with his\xa0...'},
            {'title': 'Young Sheldon (TV Series 2017–2024) - IMDb', 'link': 'https://www.imdb.com/title/tt6226232/', 'snippet': 'Young Sheldon: Created by Steven Molaro, Chuck Lorre. With Iain Armitage, Zoe Perry, Lance Barber, Montana Jordan. Meet a child genius named Sheldon Cooper\xa0...'},
            {'title': 'About Young Sheldon', 'link': 'https://www.cbs.com/shows/young-sheldon/about/', 'snippet': 'For 12 years on The Big Bang Theory, audiences have come to know the iconic, eccentric, and extraordinary Sheldon Cooper. This single-camera, half-hour comedy\xa0...'},
            ...
        ]
        >>> search_google(query='How to use pandas in python?')
        [
            {'title': '10 minutes to pandas — pandas 2.1.2 documentation', 'link': 'https://pandas.pydata.org/docs/user_guide/10min.html', 'snippet': 'Selection#. Note. While standard Python / NumPy expressions for selecting and setting are intuitive and come in handy for interactive work, for production code,\xa0...'},
            {'title': 'Pandas Tutorial', 'link': 'https://www.w3schools.com/python/pandas/default.asp', 'snippet': 'Pandas Tutorial ... Pandas is a Python library. Pandas is used to analyze data. Learning by Reading. We have created 14 tutorial pages for you to learn more about\xa0...'},
            {'title': 'A Quick Introduction to the “Pandas” Python Library | by Adi ...', 'link': 'https://towardsdatascience.com/a-quick-introduction-to-the-pandas-python-library-f1b678f34673', 'snippet': "Apr 17, 2017 ... What's cool about Pandas is that it takes data (like a CSV or TSV file, or a SQL database) and creates a Python object with rows and columns\xa0..."},
            ...
        ]
        >>> search_google(query='Best iPad games?')
        [
            {'title': 'The Best iPad Games for 2023 | PCMag', 'link': 'https://www.pcmag.com/picks/the-50-best-ipad-games', 'snippet': "The Best iPad Games for 2023 · Alto's Odyssey · Among Us · Asphalt 9: Legends · Bastion · Blek · Carcassonne · Castlevania: Grimoire of Souls · Catan HD. $4.99\xa0..."},
            {'title': 'Best iPad games? : r/ipad', 'link': 'https://www.reddit.com/r/ipad/comments/1669hlf/best_ipad_games/', 'snippet': 'Aug 31, 2023 ... Best iPad games? · Agent A · Smash Hit · Kingdom Rush (original, origins, frontiers & vengeance) · Lego Bricktales · Bride Constructor: Portal.'},
            {'title': 'The 13 Best iPad Games to Play in 2023 - IGN', 'link': 'https://www.ign.com/articles/best-ipad-games', 'snippet': 'Oct 27, 2023 ... The 13 Best iPad Games to Play in 2023 · Get some gaming in on your Apple tablet. · Genshin Impact · Stardew Valley · Among Us · Minecraft.'},
            ...
        ]
    """
    if not search_api_key or not cx_key:
        raise Exception("search API key or CX key not set")
    params = dict(
        key=search_api_key,
        cx=cx_key,
        q=query,
        **kwargs
    )
    res = requests.get(SEARCH_API_URL, params)
    items = json.loads(res.text)['items']
    # we are deleting fields we don't need for our purposes.
    # maybe parameterizing this could be a good idea.
    for item in items:
        del item['kind']
        del item['pagemap']
        del item['displayLink']
        del item['htmlSnippet']
        del item['htmlTitle']
        del item['htmlFormattedUrl']
        del item['formattedUrl']
        if 'cacheId' in item:
            del item['cacheId']
    return items
