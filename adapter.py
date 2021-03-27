from bridge import Bridge
import os


class Adapter:
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.hashtag = self.request_data.get('hashtag', '')
            self.username = self.request_data.get('username', '')
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def create_request(self):
        try:
            if not self.hashtag:
                raise Exception('No hashtag provided')
            params = {
                'q': '#' + self.hashtag,
            }
            headers = {
                "Authorization": "Bearer " + os.environ.get('BEARER_TOKEN')}
            response = self.bridge.request(self.base_url, params, headers=headers)
            data = response.json()
            self.result = ''
            if self.username:
                for status in data['statuses']:
                    if status['user']['screen_name'] == self.username:
                        self.result = self.username
                        break
            elif data['statuses']:
                self.result = data['statuses'][0]['user']['screen_name']

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
