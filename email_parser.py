import re
import json
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

# email_regex = r"""([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"""
email_regex = r'[\w.+-]+@[\w-]+\.[\w.-]+'
def get_emails_from_url(url):
    if url:
        print(f"Scraping emails for {url}")
        complete_address = f"https://{url}/"
        try:
            response = requests.get(complete_address)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all("a") # Find all elements with the tag <a>
            if len(links) > 100:
                emails = "Big Website"
            elif any(x in url for x in ["google", "hrblock", "liberty"]):
                emails = "General Website"
            else:
                emails = []
                for link in links:
                    sub_page_url = complete_address + link.get("href")
                    response = requests.get(sub_page_url)
                    if response.status_code == 200:
                        text = response.text
                        soup = str(BeautifulSoup(text,'html.parser').body)
                        emails = emails + re.findall(email_regex,soup)
                emails = json.dumps(list(set(emails)))
        except Exception as e:
            emails = "Error"
            print(f"{emails} - {e}")
    else:
        emails = None
    return emails


def main():
    business_data_list = pd.read_csv(f"google_maps_data.csv")
    business_data_list["emails"] = None
    for idx, business in business_data_list.iterrows():
        emails = get_emails_from_url(business["website"])
        business_data_list.loc[idx, "emails"] = emails
    print(business_data_list)
    business_data_list.to_csv(f"{search_for} {total}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    if args.search:
        search_for = args.search
    else:
        # in case no arguments passed
        # the scraper will search by defaukt for:
        search_for = "dentist new york"

    if args.total:
        total = args.total
    else:
        total = 10

    main()
