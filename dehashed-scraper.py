import requests
import json
import csv
import datetime, time
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

class Dehashed_Scraper():
    # Authentication is email + API. BASIC Auth | Enter you Email and Dehashed API below
    de_EMAIL = ''
    API_KEY = ''

    # Leave the below alone
    domain = ''
    headers = {'Accept': 'application/json'}

    # Search Dehashed and return results
    def fetch_data(self, query):
        try:
            self.domain = query
            url = f'https://api.dehashed.com/search?query=domain%3A{query}'
            print(f'\nSearching for {query}')
            print("\nGrabbing Leaks...")
            response = requests.get(url, headers=self.headers, auth=HTTPBasicAuth(self.de_EMAIL, self.API_KEY))
            data = json.loads(response.content)
            return data
        except:
            print("\nIssue in fetching breached data from Dehashed...")

    # Store results
    def store_results_json(self, data):
        filename = f"results-domain-{self.domain.split('.')[0]}.json"
        print(f"\nSaving search results to {filename}")
        with open(filename, "w") as dump_file:
            json.dump(data, dump_file)

    # Read results
    def read_results(self):
        filename = f"results-domain-{self.domain.split('.')[0]}.json"
        with open(filename, 'r') as file:
            data_dump = json.load(file)
            return data_dump

    # Parse results
    def parse_results(self, data_dump):
        print(f"\nParsing search results from JSON file")
        try:
            breached_emails = [emails['email'] for emails in data_dump['entries']]
            breached_passwords = [passwords['password'] for passwords in data_dump['entries']]
            breach_origin = [origin['obtained_from'] for origin in data_dump['entries']]
            return breached_emails, breached_passwords, breach_origin
        except:
            print("\nIssue in parsing breached data from JSON...")

    # Save formatted results to csv and txt
    def save_results(self, be, bp, bo):
        # Save as CSV
        with open(f'results-domain-{self.domain.split(".")[0]}.csv', 'w') as breached_fileCSV:
            writer = csv.writer(breached_fileCSV, lineterminator='\n')
            for e, p, o in zip(be, bp, bo):
                writer.writerow([e, p, o])
        print(f"\nSaved breach results to results-domain-{self.domain.split('.')[0]}.csv")
        
        # Save as TXT
        with open(f'results-domain-{self.domain.split(".")[0]}.txt', 'w') as breached_fileTXT:
            for e, p, o in zip(be, bp, bo):
                breached_fileTXT.write(f'Email: {e} | Password: {p} | From: {o}\n')
        print(f"\nSaved breach results to results-domain-{self.domain.split('.')[0]}.txt")

    # Run program
    def run(self):
        if self.API_KEY and self.de_EMAIL:
            search_term = input("\nWhat's the Domain name? (example.com): ")
            t1 = time.perf_counter()
            data = self.fetch_data(search_term)
            self.store_results_json(data)
            results = self.read_results()
            breachedEmails, breachedPass, breachOrigin = self.parse_results(results)
            self.save_results(breachedEmails, breachedPass, breachOrigin)
            t2 = time.perf_counter()
            print(f"\nFinished in {round(t2-t1, 2)} seconds...\n")
        else:
            print("\nPlease enter your API and Email to the script\n")

if __name__ == '__main__':
    scraper = Dehashed_Scraper()
    scraper.run()