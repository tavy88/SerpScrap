#!/usr/bin/python3
# -*- coding: utf-8 -*-
from GoogleScraper import scrape_with_config, GoogleSearchError
import serpscrap
from urlscrape import UrlScrape
import argparse
import chardet
import traceback
import pprint


class SerpScrap():

    args = []
    config = {
        # 'use_own_ip': True,
        'search_engines': ['google'],
        'num_pages_for_keyword': 2,
        'scrape_method': 'http',  # selenium
        # 'sel_browser': 'chrome', uncomment if scrape_method is selenium
        # 'executable_path': 'path\to\chromedriver' or 'path\to\phantomjs',
        'do_caching': True,
        'cachedir': '/tmp/.serpscrap/',
        'database_name': '/tmp/serpscrap',
        'clean_cache_after': 24,
        'output_filename': None,
        # 'print_results': 'all',
        'scrape_urls': True,
        'url_threads': 3
    }
    serp_query = None

    def cli(self, args=None):
        """method called if executed on command line"""
        parser = argparse.ArgumentParser(prog='serpscrap')
        parser.add_argument('-k', '--keyword', help='keyword for scraping', nargs='*')
        self.args = parser.parse_args()
        if len(self.args.keyword) > 0:
            keywords = ' '.join(self.args.keyword)

        print(keywords)
        self.init(config=None, keywords=keywords)
        return self.run()

    def init(self, config=None, keywords=None):
        """init config and serp_query"""
        if config is not None:
            self.config = config

        if isinstance(keywords, str):
            self.serp_query = [keywords]
        elif isinstance(keywords, list) and len(keywords) > 0:
            self.serp_query = keywords
        else:
            raise ValueError('no keywords given')

    def run(self):
        """main method to run scrap_serps and scrap_url
        return list of dicts with all results
        """
        results = None
        if self.serp_query is not None:
            results = self.scrap_serps()

        if self.config['scrape_urls']:
            for result in results:
                if 'serp_type' in result and 'ads_main' not in result['serp_type'] and 'serp_url' in result:
                    result_url = self.scrap_url(result['serp_url'])
                    results.append(result_url)
        return results

    def scrap_serps(self):
        """call scrap method and append serp results to list
        return list
        """
        search = self.scrap()
        result = []
        for serp in search.serps:
            for link in serp.links:
                # link, snippet, title, visible_link, domain, rank, serp, link_type, rating
                # if 'results' in link.link_type:
                result.append({
                    'query_num_results total': serp.num_results_for_query,
                    'query_num_results_page': serp.num_results,
                    'query_page_number': serp.page_number,
                    'query': serp.query,
                    'serp_rank': link.rank,
                    'serp_type': link.link_type,
                    'serp_url': link.link,
                    'serp_rating': link.rating,
                    'serp_title': link.title,
                    'serp_domain': link.domain,
                    'serp_visible_link': link.visible_link,
                    'serp_snippet': link.snippet,
                    'serp_sitelinks': link.sitelinks
                })
        return result

    def scrap(self):
        # See in the config.cfg file for possible values
        self.config['keywords'] = self.serp_query if isinstance(self.serp_query, list) else [self.serp_query]

        try:
            return scrape_with_config(self.config)
        except GoogleSearchError:
            print(traceback.print_exc())

    def scrap_url(self, url):
        urlscrape = UrlScrape(self.config)
        return urlscrape.scrap_url(url)

    def adjust_encoding(self, data):
        """detect and adjust encoding of data return data decoded to utf-8"""
        if data is None:
            return {'encoding': None, 'data': data}

        data = data.encode('utf-8')
        check_encoding = chardet.detect(data)

        if check_encoding['encoding'] is not None and 'utf-8' not in check_encoding['encoding']:
            try:
                data = data.decode(check_encoding['encoding']).encode('utf-8')
            except:
                pass
        try:
            data = data.decode('utf-8')
        except:
            data = data.decode('utf-8', 'ignore')

        return {'encoding': check_encoding['encoding'], 'data': data}

if __name__ == "__main__":
    res = SerpScrap().cli()
    pprint.pprint(res)