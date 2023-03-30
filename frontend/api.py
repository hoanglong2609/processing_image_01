import requests


class Api:
    base_url = 'http://localhost:2100'

    def get(self, path, params=None):
        return requests.get(url=self.__get_url(path), params=params)

    def post(self, path, data=None, json=None, **kwargs):
        return requests.post(url=self.__get_url(path), data=data, json=json, **kwargs)

    def __get_url(self, path):
        return f'{self.base_url}/{path}'


api = Api()
