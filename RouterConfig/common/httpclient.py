from requests import get, post, delete


class HttpClient(object):

    def __init__(self, method, url, data=None, headers={}, params=None, timeout=None):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.headers['Content-Type'] = 'application/json'
        self.params = params
        self.timeout = timeout

    @property
    def process(self):
        if self.method == 'GET':
            return self.GET
        elif self.method == 'POST':
            return self.POST
        elif self.method == 'DELETE':
            return self.DELETE

    # three curl methods
    @property
    def GET(self):
        res = get(url=self.url, headers=self.headers, params=self.params, timeout=self.timeout)
        return res

    @property
    def POST(self):
        res = post(url=self.url, data=self.data, headers=self.headers, params=self.params, timeout=self.timeout)
        return res

    @property
    def DELETE(self):
        res = delete(url=self.url, headers=self.headers, params=self.params, timeout=self.timeout)
        return res
