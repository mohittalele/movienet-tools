import requests
from bs4 import BeautifulSoup
import json
import os
import os.path as osp


class TMDBCrawler(object):
    def __init__(self, apikey_file):
        self.url_prefix = 'https://api.themoviedb.org/3/'
        try:
            self.api_key = open(apikey_file).read().strip()
        except Exception as e:
            print('No apikey found.')
            print(
                'To use TMDBCrawler, you should first sign up TMDB and get an api key'
                'at https://www.themoviedb.org/account/signup')

    def imdb2tmdb(self, mid):
        """Convert an IMDB ID to TMDB ID.

        Args:
            mid (str): IMDB ID
        
        Returns:
            str: TMDB ID
        """
        url = self.url_prefix + 'find/{}'.format(mid)
        params = {
        'api_key': self.api_key,
        'language': 'en-US',
        'external_source': 'imdb_id'
        }
        # get and check
        tmdb_id = None
        try:
            r = requests.get(url, params=params)
            data = json.loads(r.text)
            if data.get('status_code'):
                print('ERROR! status code: {}.'.format(data['status_code']))
            movie_results = data['movie_results']
            if len(movie_results) != 1:
                print('{} search results: {}'.format(mid, len(movie_results)))
            else:
                tmdb_id = '{}'.format(movie_results[0]['id'])
        except Exception as e:
            print('{} {}'.format(tmdb_id, e))
        return tmdb_id
