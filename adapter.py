from bridge import Bridge
import os


class Adapter:
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    code_params = ['code', 'verification_code', 'hashtag']

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        for param in self.code_params:
            self.code_param = self.request_data.get(param)
            if self.code_param is not None:
                break

    def create_request(self):
        try:
            params = {
                'q': '#' + self.code_param,
            }
            headers = {
                "Authorization": "Bearer " + os.environ.get('BEARER_TOKEN')}
            response = self.bridge.request(self.base_url, params, headers=headers)
            data = response.json()
            if data['statuses']:
                self.result = data['statuses'][0]['user']['id']
            else:
                self.result = 0
            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
