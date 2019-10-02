import requests

from tanapol.log import logger


API_URL = 'https://api.github.com'


class GithubResponse:

    def __init__(self, response):
        self.response = response
        self.content = response.json()

    def __repr__(self):
        return str(self.content)

    def __bool__(self):
        status_code = self.response.status_code
        if status_code == 200:
            return True
        else:
            logger.error(f'Status code: {status_code}'
                         f'Response: {self.response}')


class GithubClient:

    def __init__(self, secret):
        self.auth_headers = {
            'Authorization': f'token {secret}',
            }

    def _request(self, entry, post=False, **request_params):
        request_method = requests.get
        if post:
            request_method = requests.post
        url = f'{API_URL}{entry}'
        response = request_method(url,
                                  params=request_params,
                                  headers=self.auth_headers,
                                  )
        return GithubResponse(response)

    def get_feeds(self):
        return self._request('/feeds')

    def check_auth(self):
        return self.get_feeds()
