from requests import Session, exceptions
from time import sleep
from os import path
from argparse import ArgumentParser

class SessionController:

    OCR_URL = 'https://chroniclingamerica.loc.gov/ocr.json'

    def __init__(self, newspaper=None, start_date=None, end_date=None):
        self._session = Session()
        self._newspaper_url = newspaper
        self._issues = []
        self._batches = set()
        self._start_date = start_date
        self._end_date = end_date
    
    def _get_and_decode(self, url, timeout, tries, format, stream=False, skip_error=False): #TO DO: should skip error be implemented here or elsewhere?
        for i in range(tries):
            try:
                r = self._session.get(url, timeout=timeout, stream=stream)
            except exceptions.ReadTimeout:
                print("Timeout occurred, retrying GET")
                sleep(3) # be nice to the API
            else:
                if(r.status_code == 200 and format == 'json'):
                    return r.json()
                elif(r.status_code == 200 and format == 'tar'):
                    return r.iter_content(chunk_size=128)
                elif(r.status_code == 429):
                    wait_time = int(r.headers['Retry-After'])
                    print("Too many requests! Sleeping for " + str(wait_time) + " s")
                    sleep(wait_time)
                elif:
                    print("Other error, status code=" + str(r.status_code) + ". Skipping item")
            
    def get_issues(self):
        print("Getting issues")
        json_out = self._get_and_decode(self._newspaper_url, 5, 10, 'json')
        self._issues = json_out['issues']

    def get_bulk_file_names(self):
        print("Searching list of issues", end='', flush=True)
        for issue in self._issues:
            if(issue['date_issued'] >= self._start_date and
            issue['date_issued'] <= self._end_date):
                # TO DO: wrap in try-except to allow skipping 
                issue_json = self._get_and_decode(issue['url'], 5, 10, 'json')
                batch_name = issue_json['batch']['name']
                self._batches.add(batch_name)
            print('.', end='', flush=True)
        print()
        print("Batches to download: " + str(self._batches))

    def specify_bulk_file_names(self, filenames):
        self._batches = filenames

    def download_batches(self, destination):
        ocr_table = self._get_and_decode(
            self.OCR_URL, 5, 10, 'json')
        for ocr_dump in ocr_table['ocr']:
            if(ocr_dump['name'].split('.')[0] in self._batches):
                print("Downloading " + ocr_dump['name'])
                # streaming download 
                iter_content = self._get_and_decode(ocr_dump['url'], 5, 10, 'tar', stream=True)
                with open(path.join(destination, ocr_dump['name']), 'wb') as fd:
                    for chunk in iter_content:
                        fd.write(chunk)
                print("Done")
            

# RUNNING CODE
if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('url')
    parser.add_argument('start_date')
    parser.add_argument('end_date')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    s = SessionController(
        args.url, 
        args.start_date, 
        args.end_date)

    s.get_issues()
    s.get_bulk_file_names()

    if(args.output):
        s.download_batches(args.output)