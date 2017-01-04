import requests
import argparse
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
    print(domain_name)
    expiration_date = whois(domain_name)['expiration_date']
    if isinstance(expiration_date, list):
        return expiration_date[0]
    return expiration_date


def get_arguments():
    parser = argparse.ArgumentParser(description='Check site...')
    parser.add_argument('filepath', help='Put path to file with urls')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_arguments()
    urls = load_urls4check(args.filepath)
    for url in urls:
        expiration_date = get_domain_expiration_date(urlparse(url).netloc)
        one_month = datetime.timedelta(days=30)
        next_month_date = datetime.datetime.today() + one_month
        if next_month_date < expiration_date and is_server_respond_with_200(url):
            print("This site:{0} is able to work".format(url)) 
        else:
            print("{0} has problems".format(url))