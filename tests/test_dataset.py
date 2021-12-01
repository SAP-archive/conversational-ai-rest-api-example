# coding: utf-8
from dataset_translation.dataset import Dataset


class TestDataset:

  @staticmethod
  def test_fill_intents():
    intents = [{
      'slug': 'greetings',
      'created_at': '2021-02-10T12:56:05.547Z',
      'updated_at': '2021-07-01T13:09:12.057Z',
      'description': 'Says hello',
      'name': 'greetings',
      'rating': 0,
      'dataset_id': 0,
      'is_activated': True,
      'position': 2,
      'is_forking': False,
      'strictness': None
    }]

    cai_intents = [{
      'name': 'greetings',
      'description': 'Says hello',
      'strictness': None,
      'expressions': []
    }]
    transformed_intents = Dataset().fill_intents(intents)
    assert transformed_intents == cai_intents
    assert len(transformed_intents) == len(cai_intents)

  @staticmethod
  def test_fill_gazettes():
    entities = [{
      'dataset_id': 0,
      'entity_id': None,
      'is_open': True,
      'is_activated': True,
      'slug': 'music-genre',
      'created_at': '2021-02-15T10:13:05.659Z',
      'updated_at': '2021-02-15T10:13:05.659Z',
      'strictness': None,
      'enrichment_strictness': 95,
      'is_custom': True,
      'color': '#b39ddb',
      'name': 'MUSIC-GENRE',
      'is_forking': False,
      'webhook_id': None,
      'gold_enrichment_from': None,
      'enrichment_type': 'map',
      'enrichment_webhook_id': None,
      'locked': True,
      'type': 2,
      'regex_pattern': None,
      'regex_flags': None
    }]
    synonyms = [{
      'entity_id': 0,
      'value': 'rock',
      'slug': None,
      'created_at': '2021-07-09T10:01:24.804Z',
      'updated_at': '2021-07-09T10:01:24.804Z',
      'language': 'en'
    }]

    cai_synonyms = [{
      'name': 'MUSIC-GENRE',
      'slug': 'music-genre',
      'locked': True,
      'type': 'restricted',
      'is_open': True,
      'strictness': None,
      'enrichment_strictness': 95,
      'synonyms': ["rock"],
      'regex_pattern': None,
      'regex_flags': None
    }]

    assert Dataset().fill_gazettes(entities, synonyms, 'en') == cai_synonyms
    cai_synonyms['name' == 'MUSIC-GENRE']['synonyms'] = []
    assert Dataset().fill_gazettes(entities, synonyms, 'fr') == cai_synonyms

  @staticmethod
  def test_fill_expressions():
    expressions = [{
      'intent_id': 0,
      'source': 'I want to listen to rock',
      'created_at': '2021-07-28T14:42:13.067Z',
      'updated_at': '2021-07-28T14:42:14.095Z',
      'tokens': "[{\"pos\":\"PRON\",\"word\":\"I\",\"space\":true,\"entity_id\":1},{\"pos\":\"VERB\",\"word\":\"want\",\"space\":true},{\"pos\":\"PART\",\"word\":\"to\",\"space\":true},{\"pos\":\"VERB\",\"word\":\"listen\",\"space\":true},{\"pos\":\"ADP\",\"word\":\"to\",\"space\":true},{\"pos\":\"NOUN\",\"word\":\"rock\",\"space\":false,\"entity_id\":0}]",
      'language': 'en'
    }]
    cai_synonyms = [
      {
        'name': 'MUSIC-GENRE',
        'slug': 'music-genre',
        'locked': True,
        'type': 'restricted',
        'is_open': True,
        'strictness': None,
        'enrichment_strictness': 95,
        'synonyms': ["rock"],
        'regex_pattern': None,
        'regex_flags': None
      },
      {
        'name': 'PRONOUN',
        'slug': 'pronoun',
        'locked': True,
        'type': 'gold',
        'is_open': True,
        'strictness': None,
        'enrichment_strictness': 95,
        'regex_pattern': None,
        'regex_flags': None
      }
    ]

    cai_expressions = [{
      'source': 'I want to listen to rock',
      'tokens': [
        {
          'pos': 'PRON',
          'word': 'I',
          'space': True,
          'entity': {
            'name': 'PRONOUN',
            'type': 'gold',
            'is_custom': False
          }
        },
        {
          'pos': 'VERB',
          'word': 'want',
          'space': True,
          'entity': None
        },
        {
          'pos': 'PART',
          'word': 'to',
          'space': True,
          'entity': None
        },
        {
          'pos': 'VERB',
          'word': 'listen',
          'space': True,
          'entity': None
        },
        {
          'pos': 'ADP',
          'word': 'to',
          'space': True,
          'entity': None
        },
        {
          'pos': 'NOUN',
          'word': 'rock',
          'space': False,
          'entity': {
            'name': 'MUSIC-GENRE',
            'type': 'restricted',
            'is_custom': True
          }
        }
      ]
    }]
    intents = [{
      'name': 'ask-music',
      'description': None,
      'strictness': 60,
      'expressions': []
    }]

    cai_intents_en = intents
    cai_intents_fr = intents
    cai_intents_en[0]['expressions'] = cai_expressions
    Dataset().fill_expressions(intents, cai_synonyms, expressions, 'en')
    assert intents == cai_intents_en
    Dataset().fill_expressions(intents, cai_synonyms, expressions, 'fr')
    assert intents == cai_intents_fr

  @staticmethod
  def test_to_cai_format():
    original_dataset = {
      'version': 5,
      'datasets': [
        {
          'slug': None,
          'created_at': '2021-02-15T10:13:05.609Z',
          'updated_at': '2021-07-28T14:43:12.028Z',
          'strictness': 50,
          'type': 0,
          'classifier': 4,
          'recognizer': 0,
          'manual_training': True,
          'big_bot': False,
          'bot_id': 'a6d7cb05-468b-4fce-ad31-5a10539ba0ce',
          'version_id': '9deee18f-8aa5-4a38-b797-f6a16ab56784',
          'is_forking': False,
          'resolve_pronouns': False,
          'resolve_descriptions': False,
          'last_data_update_at': "{\"en\": \"2021-07-28T14:43:12.027Z\", \"fr\": \"2021-07-28T14:41:37.198Z\"}",
          'language': 'fr',
          'restricted_entity_strictness': 90,
          'free_entity_strictness': 0,
          'is_generating': False,
          'sharenet': 0
        }
      ],
      'intents': [
        {
          'slug': 'ask-music',
          'created_at': '2021-02-15T10:13:07.284Z',
          'updated_at': '2021-02-15T10:13:07.284Z',
          'description': None,
          'name': 'ask-music',
          'rating': 0,
          'dataset_id': 0,
          'is_activated': True,
          'position': 2,
          'is_forking': False,
          'strictness': 60
        }
      ],
      'entities': [
        {
          'dataset_id': 0,
          'entity_id': None,
          'is_open': True,
          'is_activated': True,
          'slug': 'music-genre',
          'created_at': '2021-02-15T10:13:05.659Z',
          'updated_at': '2021-02-15T10:13:05.659Z',
          'strictness': None,
          'enrichment_strictness': 95,
          'is_custom': True,
          'color': '#b39ddb',
          'name': 'MUSIC-GENRE',
          'is_forking': False,
          'webhook_id': None,
          'gold_enrichment_from': None,
          'enrichment_type': 'map',
          'enrichment_webhook_id': None,
          'locked': True,
          'type': 2,
          'regex_pattern': None,
          'regex_flags': None
        },
        {
          'dataset_id': 0,
          'entity_id': None,
          'is_open': True,
          'is_activated': True,
          'slug': 'pronoun',
          'created_at': '2021-02-15T10:13:05.614Z',
          'updated_at': '2021-02-15T10:13:05.614Z',
          'strictness': None,
          'enrichment_strictness': 95,
          'is_custom': False,
          'color': '#cffff4',
          'name': 'PRONOUN',
          'is_forking': False,
          'webhook_id': None,
          'gold_enrichment_from': None,
          'enrichment_type': None,
          'enrichment_webhook_id': None,
          'locked': True,
          'type': 0,
          'regex_pattern': None,
          'regex_flags': None
        }
      ],
      'synonyms': [{
        'entity_id': 0,
        'value': 'rock',
        'slug': None,
        'created_at': '2021-07-09T10:01:24.804Z',
        'updated_at': '2021-07-09T10:01:24.804Z',
        'language': 'en'
      }],
      'expressions': [{
        'intent_id': 0,
        'source': 'I want to listen to rock',
        'created_at': '2021-07-28T14:42:13.067Z',
        'updated_at': '2021-07-28T14:42:14.095Z',
        'tokens': "[{\"pos\":\"PRON\",\"word\":\"I\",\"space\":true,\"entity_id\":1},{\"pos\":\"VERB\",\"word\":\"want\",\"space\":true},{\"pos\":\"PART\",\"word\":\"to\",\"space\":true},{\"pos\":\"VERB\",\"word\":\"listen\",\"space\":true},{\"pos\":\"ADP\",\"word\":\"to\",\"space\":true},{\"pos\":\"NOUN\",\"word\":\"rock\",\"space\":false,\"entity_id\":0}]",
        'language': 'en'
      }]
    }

    cai_dataset = {
      'language': 'en',
      'intents': [
        {
          'name': 'ask-music',
          'description': '',
          'strictness': 60,
          'expressions': [{
            'source': 'I want to listen to rock',
            'tokens': [
              {
                'pos': 'PRON',
                'word': 'I',
                'space': True,
                'entity': {
                  'name': 'PRONOUN',
                  'type': 'gold',
                  'is_custom': False
                }
              },
              {
                'pos': 'VERB',
                'word': 'want',
                'space': True,
                'entity': None
              },
              {
                'pos': 'PART',
                'word': 'to',
                'space': True,
                'entity': None
              },
              {
                'pos': 'VERB',
                'word': 'listen',
                'space': True,
                'entity': None
              },
              {
                'pos': 'ADP',
                'word': 'to',
                'space': True,
                'entity': None
              },
              {
                'pos': 'NOUN',
                'word': 'rock',
                'space': False,
                'entity': {
                  'name': 'MUSIC-GENRE',
                  'type': 'restricted',
                  'is_custom': True
                }
              }
            ]}]
        }
      ],
      'gazettes': [
        {
          'name': 'MUSIC-GENRE',
          'slug': 'music-genre',
          'locked': True,
          'type': 'restricted',
          'is_open': True,
          'strictness': None,
          'enrichment_strictness': 95,
          'synonyms': ['rock'],
          'regex_pattern': None,
          'regex_flags': None
        },
        {
          'name': 'PRONOUN',
          'slug': 'pronoun',
          'locked': True,
          'type': 'gold',
          'is_open': True,
          'strictness': None,
          'enrichment_strictness': 95,
          'synonyms': [],
          'regex_pattern': None,
          'regex_flags': None
        }
      ]
    }

    assert Dataset().to_cai_format(original_dataset, 'en') == cai_dataset
    cai_dataset['language'] = 'fr'
    cai_dataset['intents']['name' == 'ask-music']['expressions'] = []
    cai_dataset['gazettes']['name' == 'MUSIC-GENRE']['synonyms'] = []
    assert Dataset().to_cai_format(original_dataset, 'fr') == cai_dataset
