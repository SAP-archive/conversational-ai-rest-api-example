# coding: utf-8
import requests
import pytest
from mock import patch, Mock
from dataset_translation.cai_client import CaiClient


def requests_mocked(status):
  mocked_requests = Mock()
  response = requests.Response()
  response.status_code = status
  response._content = b'{"results":[{"source":"expression0", "id":0}], "access_token":"access_token0"}'
  mocked_requests.get.return_value = response
  mocked_requests.put.return_value = response
  mocked_requests.post.return_value = response
  return mocked_requests

@pytest.fixture
@patch('dataset_translation.cai_client.requests', requests_mocked(200))
def cai_client_mocked():
  cai_client_object = CaiClient('user_slug', 'bot_slug', 'version_slug', 'developer_token', 'bot_client_id', 'bot_client_secret')
  return cai_client_object

class TestCaiClient:

  @patch('dataset_translation.cai_client.requests', new_callable=lambda: requests_mocked(200))
  def test_update_expression(self, mocked_request, cai_client_mocked):
    token = {
              'ind': 0,
              'space': True,
              'pos': 'VERB',
              'word': 'expression0',
              'entity': None
            }
    token_formatted = {
                        'ind': 0,
                        'space': True,
                        'part_of_speech': 'VERB',
                        'word': {'name': 'expression0'}
                      }
    cai_client_mocked.update_expression(0, token, 'intent-name', 'expression0', "id0")
    headers = {
                'Authorization': 'Bearer access_token0',
                'Content': 'application/json',
                'X-Token': 'Token developer_token'
              }

    mocked_request.put.assert_called_with('https://api.cai.tools.sap/train/v2/users/user_slug/bots/bot_slug/versions/version_slug/dataset/intents/intent-name/expressions/id0',
                                          json={'source': 'expression0', 'tokens': [token_formatted]}, headers=headers)

  @patch('dataset_translation.cai_client.requests', requests_mocked(400))
  def test_update_expression_error(self, cai_client_mocked):
    token = {
              'ind': 0,
              'space': True,
              'pos': 'VERB',
              'word': 'expression0',
              'entity': None
            }
    with pytest.raises(ValueError):
      assert cai_client_mocked.update_expression(0, token, 'intent-name', 'expression0', 'id0')

  @patch('dataset_translation.cai_client.requests', requests_mocked(200))
  def test_post_expression(self, cai_client_mocked):
    results = cai_client_mocked.post_expression('intent-name', 'expression0', 'en')
    assert results == [{'source': 'expression0', 'id': 0}]

  @patch('dataset_translation.cai_client.requests', requests_mocked(400))
  def test_post_expression_error(self, cai_client_mocked):
    with pytest.raises(ValueError):
      assert cai_client_mocked.post_expression('intent-name', 'expression0', 'en')

  @patch('dataset_translation.cai_client.requests', new_callable=lambda: requests_mocked(200))
  def test_post_synonyms(self, mocked_request, cai_client_mocked):
    cai_client_mocked.post_synonyms('entity_slug', ['synonym0', 'synonym1'], 'en')
    headers = {
                'Authorization': 'Bearer access_token0',
                'Content': 'application/json',
                'X-Token': 'Token developer_token'
              }
    list_synonyms = [{'value': 'synonym0', 'language': {'isocode': 'en'}},
                     {'value': 'synonym1', 'language': {'isocode': 'en'}}]
    mocked_request.post.assert_called_with('https://api.cai.tools.sap/train/v2/users/user_slug/bots/bot_slug/versions/version_slug/dataset/entities/entity_slug/synonyms/bulk_create',
                                           json={'synonyms': list_synonyms}, headers=headers)

  @patch('dataset_translation.cai_client.requests', requests_mocked(400))
  def test_post_synonyms_error(self, cai_client_mocked):
    with pytest.raises(ValueError):
      assert cai_client_mocked.post_synonyms('entity_slug', ['synonym0', 'synonym1'], 'en')

  @patch('dataset_translation.cai_client.requests', requests_mocked(200))
  def test_token_cai_convert(self, cai_client_mocked):
    token_none = {
                    'ind': 0,
                    'space': True,
                    'pos': 'VERB',
                    'word': 'expression0',
                    'entity': None
                 }
    token_entity = {
                      'ind': 0,
                      'space': True,
                      'pos': 'VERB',
                      'word': 'expression0',
                      'entity': {'name': 'PRONOUN', 'type': 'gold', 'is_custom': False}
                   }

    token_none_convert = cai_client_mocked.convert_token_cai(0, token_none)
    assert token_none_convert == {'ind': 0, 'space': True, 'part_of_speech': 'VERB', 'word': {'name': 'expression0'}}
