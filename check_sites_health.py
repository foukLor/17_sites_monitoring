import requests
import sys
from whois import whois
from urllib.parse import urlparse
import datetime


TIMEOUT = 10

def load_urls4check(path):
    urls = []
    with open(path,'r') as file:
        for line in file:
            urls.append(line.strip())
    return urls


def is_server_respond_with_200(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code == requests.codes.ok


def get_domain_expiration_date(domain_name):
    expiration_date = whois(domain_name)['expiration_date']
    if isinstance(expiration_date, list):
        return expiration_date[0]
    return expiration_date


def get_file_path_with_domains():
    if len(sys.argv) == 1:
        return None
    else:
        return sys.argv[1]


if __name__ == '__main__':
    file_path = get_file_path_with_domains()
    if file_path is None:
        exit()
    urls = load_urls4check(file_path)
    days_in_month = 30
    for url in urls:
        expiration_date = get_domain_expiration_date(urlparse(url).netloc)
        one_month = datetime.timedelta(days=days_in_month)
        next_month_date = datetime.datetime.today() + one_month
        if next_month_date < expiration_date and is_server_respond_with_200(url):
            print("This site:{0} is able to work".format(url)) 
        else:
            print("{0} has problems".format(url))