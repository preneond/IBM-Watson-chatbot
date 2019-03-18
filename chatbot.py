from watson_developer_cloud import AssistantV2
from watson_developer_cloud import DiscoveryV1


def parse_short_tail_msg(response):
    return list(map(lambda r: r['text'], response))


def parse_long_tail_msg(response):
    result = response.result['results'][0]
    overview = result['overview']
    title = result['title']

    return [title + ': ' + overview]


class Chatbot:
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.discovery = DiscoveryV1(version='2018-08-01',
                                     url='insert-watson-url',
                                     iam_apikey='insert-api-key')
        self.discovery_env_id = 'insert-env-id'
        self.discovery_col_id = 'insert-col-id'
        self.assistant_id = 'insert-assistant-id'
        self.assistant = AssistantV2(
            iam_apikey='insert-api-key',
            version='2018-11-08',
            url='insert-url'
        )

        self.assistant_session_id = self.assistant.create_session(
            assistant_id=self.assistant_id
        ).get_result()['session_id']

    def get_response(self, msg):
        response = self.short_tail(msg)['output']
        short_tail = response['generic']
        if len(short_tail) != 0:
            if len(response['intents']) != 0 and response['intents'][0]['confidence'] > 0.75:
                return parse_short_tail_msg(short_tail)
            elif len(response['entities']) != 0 and response['entities'][0]['confidence'] > 0.75:
                return parse_short_tail_msg(short_tail)

        long_tail_response = self.long_tail(msg)
        if long_tail_response.result['matching_results'] == 0:
            return ["Hmmm, I am not sure what you mean."]
        else:
            return parse_long_tail_msg(long_tail_response)

    def long_tail(self, msg):
        return self.discovery.query(environment_id=self.discovery_env_id, collection_id=self.discovery_col_id,
                                    natural_language_query=msg)

    def short_tail(self, msg):
        response = self.assistant.message(
            assistant_id=self.assistant_id,
            session_id=self.assistant_session_id,
            input={
                'message_type': 'text',
                'text': msg
            }
        ).get_result()

        return response
