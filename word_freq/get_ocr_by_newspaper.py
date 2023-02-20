from requests import Session, exceptions
from time import sleep
from os import path

class SessionController:

    def __init__(self, newspaper, start_date, end_date, directory_path):
        self._session = Session()
        self._newspaper_url = newspaper
        self._issues = []
        self._start_date = start_date
        self._end_date = end_date
        self._directory_path = directory_path
    
    def _get_and_decode(self, url, timeout, format):
        while True:
            try:
                r = self._session.get(url, timeout=timeout)
            except exceptions.ReadTimeout:
                print("Timeout occurred, retrying GET...")
                sleep(3) # we will be nice to the API
            else:
                if(r.status_code == 200 and format == 'json'):
                    return r.json()
                elif(r.status_code == 200 and format == 'txt'):
                    return r.text
                elif(r.status_code == 429):
                    print("Too many requests! Sleeping for 300 s...")
                    sleep(300)
                else:
                    print("Unknown error")
            
    def get_issues(self):
        json_out = self._get_and_decode(self._newspaper_url, 5, 'json')
        self._issues = json_out['issues']
        return 

    def get_and_write_ocr(self):
        for issue in self._issues:
            if(issue['date_issued'] >= self._start_date and
            issue['date_issued'] <= self._end_date):
                json_out = self._get_and_decode(issue['url'], 5, 'json')
                pages = json_out['pages']
                for page in pages:
                    json_out = self._get_and_decode(page['url'], 5, 'json')
                    text = self._get_and_decode(json_out['text'], 5, 'txt')
                    filename = issue['date_issued'] + '_' + str(json_out['sequence'])
                    with open(path.join(self._directory_path, filename),'w') as f:
                        f.write(text)

# RUNNING CODE
s = SessionController(
    'https://chroniclingamerica.loc.gov/lccn/sn83045462.json', 
    '1917-05-30', 
    '1917-12-31', 
    './evening-star')
s.get_issues()
s.get_and_write_ocr()