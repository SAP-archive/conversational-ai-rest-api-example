# coding: utf-8
import json
import requests

from mock import patch, Mock
import pytest
from dataset_translation.dataset_translation import DatasetTranslation
from dataset_translation.translator import SAPTranslationHubTranslator, NoneTranslator


def requests_mocked():
  mocked_requests = Mock()
  response = requests.Response()
  response.status_code = 200
  response._content = b'{"results":[{"name":"ACCESSORIES", "id":0, "type": "free"}, {"name":"BOX_OPTION", "id":1, "type": "free"}], "access_token": "token"}'
  mocked_requests.get.return_value = response
  mocked_requests.post.return_value = response
  mocked_requests.put.return_value = response
  return mocked_requests

@pytest.fixture
@patch('dataset_translation.cai_client.requests', requests_mocked())
def dataset_translation_mocked():
  mocked_dataset_translation = DatasetTranslation('none', 'en', 'fr', 'user_slug', 'bot_slug', 'version_slug', 'developer_token', 'bot_client_id', 'bot_client_secret')
  return mocked_dataset_translation


class TestDatasetTranslation:

  @patch('dataset_translation.cai_client.requests', requests_mocked())
  @patch('dataset_translation.translator.sap_translation_hub_translator.requests', requests_mocked())
  def test_datasettranslation_translator(self):
    saptranslation = DatasetTranslation('saptranslationhub', 'en', 'fr', 'user_slug', 'bot_slug', 'version_slug', 'developer_token', 'bot_client_id', 'bot_client_secret', 'client_id', 'client_secret')
    nonetranslation = DatasetTranslation('none', 'en', 'fr', 'user_slug', 'bot_slug', 'version_slug', 'developer_token', 'bot_client_id', 'bot_client_secret')
    assert isinstance(saptranslation.translator, SAPTranslationHubTranslator)
    assert isinstance(nonetranslation.translator, NoneTranslator)

  def test_convert_token_cai(self, dataset_translation_mocked):
    token = [{'ind': 0, 'space': True, 'part_of_speech': 'VERB', 'word': {'name': 'expression0'}}]
    token_converted = dataset_translation_mocked.convert_token_cai(token)
    assert token_converted == [{'word': 'expression0', 'space': True, 'pos': 'VERB', 'entity': None}]
    assert len(token) == len(token_converted)

  @patch('dataset_translation.cai_client.requests', new_callable=lambda: requests_mocked())
  def test_translate_synonyms(self, mocked_request, dataset_translation_mocked):
    gazettes = [{'slug': 'gazette slug', 'synonyms': ['synonym0', 'synonym1']},
                {'slug': 'gazette slug2', 'synonyms': ['synonym0', 'synonym1']}]
    gazettes_no_synonym = [{'slug': 'gazette slug', 'synonyms': None}]
    translated_synonyms = dataset_translation_mocked.translate_synonyms(gazettes)
    translated_no_synonym = dataset_translation_mocked.translate_synonyms(gazettes_no_synonym)
    assert mocked_request.post.call_count == 2
    assert translated_synonyms == gazettes
    assert translated_no_synonym == gazettes_no_synonym

  def test_translate_non_gold_tokens(self, dataset_translation_mocked):
    tokens = [
      {
        'word': 'BOXOPTION',
        'space': True,
        'pos': 'NOUN',
        'entity': {
          'name': 'BOX_OPTION',
          'type': 'free',
          'is_custom': True
        }
      },
      {
        'word': 'et',
        'space': True,
        'pos': 'CCONJ',
        'entity': None
      },
      {
        'word': 'prise',
        'space': True,
        'pos': "NOUN",
        'entity': None
      },
      {
        'word': 'CPL',
        'space': False,
        'pos': 'NOUN',
        'entity': {
          'name': 'ACCESSORIES',
          'type': 'free',
          'is_custom': True
        }
      }
    ]
    no_synonym = [{'name': 'BOX_OPTION', 'synonyms': []}, {'name': 'ACCESSORIES', 'synonyms': []}]
    synonym1 = [{'name': 'ACCESSORIES', 'synonyms': ['cpl']}]
    synonym2 = [{'name': 'BOX_OPTION', 'synonyms': ['another synonym']}, {'name': 'ACCESSORIES', 'synonyms': ['cpl']}]
    no_synonym_tokens = dataset_translation_mocked.translate_non_gold_tokens(tokens, no_synonym)
    synonym1_tokens = dataset_translation_mocked.translate_non_gold_tokens(tokens, synonym1)
    synonym2_tokens = dataset_translation_mocked.translate_non_gold_tokens(tokens, synonym2)
    assert no_synonym_tokens == {0: ['boxoption'], 3: ['cpl']}
    assert synonym1_tokens == {3: ['cpl']}
    assert synonym2_tokens == {0: ['another synonym', 'boxoption'], 3: ['cpl']}

  @patch('dataset_translation.cai_client.requests', requests_mocked())
  def test_update_and_compile_expressions(self, dataset_translation_mocked):

    tokens = [
      {
        'word': 'BOXOPTION',
        'space': True,
        'pos': 'NOUN',
        'entity': None
      },
      {
        'word': 'et',
        'space': True,
        'pos': 'CCONJ',
        'entity': None
      },
      {
        'word': 'prise',
        'space': True,
        'pos': 'NOUN',
        'entity': None
      },
      {
        'word': 'CPL',
        'space': False,
        'pos': 'NOUN',
        'entity': None
      }
    ]

    updated_tokens = [
      {
        'word': 'BOXOPTION',
        'space': True,
        'pos': 'NOUN',
        'entity': {
          'name': 'BOX_OPTION',
          'type': 'free',
          'is_custom': True
        }
      },
      {
        'word': 'et',
        'space': True,
        'pos': 'CCONJ',
        'entity': None
      },
      {
        'word': 'prise',
        'space': True,
        'pos': 'NOUN',
        'entity': None
      },
      {
        'word': 'CPL',
        'space': False,
        'pos': 'NOUN',
        'entity': {
          'name': 'ACCESSORIES',
          'type': 'free',
          'is_custom': True
        }
      }
    ]
    expression = {'id': 'f3230b7b-3676-4452-a0e9-b8c38d68124a',
                  'source': 'BOXOPTION et prise CPL',
                  'compiled': 'BOXOPTION et prise ACCESSORIES',
                  'tokens': [
                    {
                      'word': 'BOXOPTION',
                      'space': True,
                      'pos': 'NOUN',
                      'entity': {
                        'name': 'BOX_OPTION',
                        'type': 'free',
                        'is_custom': True
                      }
                    },
                    {
                      'word': 'et',
                      'space': True,
                      'pos': 'CCONJ',
                      'entity': None
                    },
                    {
                      'word': 'prise',
                      'space': True,
                      'pos': 'NOUN',
                      'entity': None
                    },
                    {
                      'word': 'CPL',
                      'space': False,
                      'pos': 'NOUN',
                      'entity': {
                        'name': 'ACCESSORIES',
                        'type': 'free',
                        'is_custom': True
                      }
                    }
                  ]
                  }
    list_tokens, expression_compiled = dataset_translation_mocked.update_and_compile_expressions(tokens, {0: ['boxoption'], 3: ['cpl']}, expression, 'accessories-information', 'f3230b7b-3676-4452-a0e9-b8c38d68124a')
    assert list_tokens == updated_tokens

  @patch('dataset_translation.cai_client.requests', new_callable=lambda: requests_mocked())
  def test_dataset_translation(self, mocked_request, dataset_translation_mocked):
    original_data = {'gazettes': [{'slug': 'gazette slug', 'synonyms': ['synonym0', 'synonym1']},
                                  {'slug': 'gazette slug2', 'synonyms': ['synonym0', 'synonym1']}],
                     'intents':  [{'name': 'accessories-information', 'expressions': [{
                       'id': 'dff14fc3-96c8-4b6f-b339-02d8e9d0a363',
                       'source': 'I would like information on the 7 G Roller',
                       'compiled': 'PRONOUN would like information on the MASS Roller',
                       'tokens': [
                         {
                           'word': 'I',
                           'space': True,
                           'pos': 'PRON',
                           'entity': {
                             'name': 'PRONOUN',
                             'type': 'gold',
                             'is_custom': False
                           }
                         },
                         {
                           'word': 'would',
                           'space': True,
                           'pos': 'AUX',
                           'entity': None
                         },
                         {
                           'word': 'like',
                           'space': True,
                           'pos': 'VERB',
                           'entity': None
                         },
                         {
                           'word': 'information',
                           'space': True,
                           'pos': 'NOUN',
                           'entity': None
                         },
                         {
                           'word': 'on',
                           'space': True,
                           'pos': 'ADP',
                           'entity': None
                         },
                         {
                           'word': 'the',
                           'space': True,
                           'pos': 'DET',
                           'entity': None
                         },
                         {
                           'word': '7',
                           'space': True,
                           'pos': 'NOUN',
                           'entity': {
                             'name': 'MASS',
                             'type': 'gold',
                             'is_custom': False
                           }
                         },
                         {
                           'word': 'G',
                           'space': True,
                           'pos': 'PROPN',
                           'entity': {
                             'name': 'MASS',
                             'type': 'gold',
                             'is_custom': False
                           }
                         },
                         {
                           'word': 'Roller',
                           'space': False,
                           'pos': 'NOUN',
                           'entity': None
                         }],
                       'sentiment': 'neutral'
                       }]}]
                     }

    response_post = requests.Response()
    response_post.status_code = 200
    return_results = {'results': {'id': 'dff14fc3-96c8-4b6f-b339-02d8e9d0a363',
                                  'tokens': [
                                    {
                                      'word': {'name': 'I'},
                                      'space': True,
                                      'part_of_speech': 'PRON',
                                      'entity': {
                                        'name': 'PRONOUN',
                                        'type': 'gold',
                                        'custom': False
                                      }
                                    },
                                    {
                                      'word': {'name': 'would'},
                                      'space': True,
                                      'part_of_speech': 'AUX'
                                    },
                                    {
                                      'word': {'name': 'like'},
                                      'space': True,
                                      'part_of_speech': 'VERB'
                                    },
                                    {
                                      'word': {'name': 'information'},
                                      'space': True,
                                      'part_of_speech': 'NOUN'
                                    },
                                    {
                                      'word': {'name': 'on'},
                                      'space': True,
                                      'part_of_speech': 'ADP'
                                    },
                                    {
                                      'word': {'name': 'the'},
                                      'space': True,
                                      'part_of_speech': 'DET'
                                    },
                                    {
                                      'word': {'name': '7'},
                                      'space': True,
                                      'part_of_speech': 'NOUN',
                                      'entity': {
                                        'name': 'MASS',
                                        'type': 'gold',
                                        'custom': False
                                      }
                                    },
                                    {
                                      'word': {'name': 'G'},
                                      'space': True,
                                      'part_of_speech': 'PROPN',
                                      'entity': {
                                        'name': 'MASS',
                                        'type': 'gold',
                                        'custom': False
                                      }
                                    },
                                    {
                                      'word': {'name': 'Roller'},
                                      'space': False,
                                      'part_of_speech': 'NOUN'
                                    }
                                  ]}}
    response_post._content = json.dumps(return_results, indent=2).encode('utf-8')
    mocked_request.post.return_value = response_post

    translated_data = dataset_translation_mocked.dataset_translation(original_data)

    assert translated_data['language'] == original_data['language']
    assert translated_data == original_data
    assert type(translated_data) == type(original_data)
    assert len(translated_data) == len(original_data)

  def test_flatten(self, dataset_translation_mocked):
    list_to_flatten = [1, [2, 3], 4]
    assert dataset_translation_mocked.flatten(list_to_flatten) == [1, 2, 3, 4]

  def test_add_entity_name(self, dataset_translation_mocked):
    result = dataset_translation_mocked.add_entity_name('TEST_1-0/=.0', 'this is a ')
    assert result == 'this is a TEST100 '
    assert isinstance(result, str)
