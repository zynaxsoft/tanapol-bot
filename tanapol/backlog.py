import requests


BASE_URL = 'https://qbit.backlog.com'
API_V2 = f'{BASE_URL}/api/v2'


class BacklogResponse:

    def __init__(self, json_dict):
        self.content = json_dict

    def __repr__(self):
        return str(self.content)

    def __bool__(self):
        return 'error' not in self.content


class BacklogClient:

    def __init__(self, secret):
        self.secret = secret

    def _request(self, entry, post=False, **kwargs):
        request_method = requests.get
        if post:
            request_method = requests.post
        url = f'{API_V2}/{entry}'
        request_params = dict(apiKey=self.secret,
                              **kwargs,
                              )
        response = request_method(url, params=request_params)
        return BacklogResponse(response)

    def check_auth(self):
        return self._request('users/myself')

    def comment(self, issue, content):
        return self._request(f'issues/{issue}/comments',
                             post=True,
                             content=content)
