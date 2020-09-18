# Script parse urls from sitemap xml files and save it to csv
import requests
from bs4 import BeautifulSoup as bs
import xmltodict
import pandas as pd

SITEMAP_INDEX_URL = "https://www.example.com/sitemap.xml"

def is_index(body):
    return True if 'sitemapindex' in body else False

def get_xml(url):
    response = requests.get(url)
    body = xmltodict.parse(response.text, force_list=('url')) # about the bug:https://github.com/martinblech/xmltodict/issues/188
    return body

def parse_index_sitemap(body):
    data = [item["loc"] for item in body['sitemapindex']['sitemap']]
    print("{} sitemap urls already parsed".format(len(data)))
    return data

def parse_sitemap_urls(body):
    data = [item["loc"] for item in body['urlset']['url']]
    print("{} urls already parsed".format(len(data)))
    return data

def save_to_file(urls_dict):
    df = pd.DataFrame(urls_dict, columns=["urls"])
    df.to_csv('ready.csv', index=False)

def main():
    urls = []
    xml_body = get_xml(SITEMAP_INDEX_URL)
    if is_index(xml_body):
        sitemaps = parse_index_sitemap(xml_body)
        for sitemap in sitemaps:
            sitemap_body = get_xml(sitemap)
            print(sitemap)
            urls += parse_sitemap_urls(sitemap_body)
    else:
        print("else")
        urls += parse_sitemap_urls(xml_body)
    
    print("done {} urls".format(len(urls)))
    save_to_file(urls)
    

if __name__ == "__main__":
    main()
