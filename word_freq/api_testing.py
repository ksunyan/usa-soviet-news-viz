from requests import Session, exceptions

class SearchSession:

    def __init__(self):
        self._session = Session()
        self._base_url = 'https://chroniclingamerica.loc.gov/search/pages/results/'
        self._payload = {'andtext':'', 'format':'json', 'page':''}
        self._page = 1
        self.total_items = 0
        self.last_end_index = 0

    def set_query(self, q):
        self._payload['andtext'] = q

    def get_and_write(self, filename):
        """Make a GET request to the ChronAm API and
        write the results to a file"""
        while True:
            try:
                self._payload['page'] = self._page
                r = self._session.get(self._base_url, params=self._payload, timeout=5)
                json_out = r.json()
            except exceptions.ReadTimeout:
                print("Timeout occurred, retrying GET...")
            except exceptions.JSONDecodeError:
                print(r.status_code)
                print(r.headers)
                print("JSON decode failed, retrying GET...")
            else:
                self.total_items = json_out['totalItems']
                self.last_end_index = json_out['endIndex']
                self._page += 1
                items = json_out['items']
                with open(filename, 'a') as f:
                    for item in items:
                        f.write(item['id'] + '\n')
                return

# RUNNING CODE
s = SearchSession()
s.set_query('Lenin')
# first GET request
s.get_and_write('ids.txt')
print(str(s.last_end_index)+' of '+str(s.total_items))

# GET subsequent pages
while s.last_end_index < s.total_items:
    s.get_and_write('ids.txt')
    print(str(s.last_end_index)+' of '+str(s.total_items))