#!/usr/bin/env python3
import json
import logging

class Dataset:
  """
  Corresponds to the CAI-format json dataset, can transform the exported dataset from the CAI platform to this format.
  """

  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def to_cai_format(self, dataset, language):
    """
    Transforms an exported dataset to a CAI-format dataset

    Args :
      - language (str) : the source language of the dataset
      - dataset (dict) : the original exported dataset

    Returns :
      - dict : the transformed CAI-format dataset
    """

    cai_dataset = {'language': language, 'intents': [], 'gazettes': []}

    self.logger.info('Transforming dataset')
    cai_dataset['intents'] = self.fill_intents(dataset['intents'])
    cai_dataset['gazettes'] = self.fill_gazettes(dataset['entities'], dataset['synonyms'], language)
    self.fill_expressions(cai_dataset['intents'], cai_dataset['gazettes'], dataset['expressions'], language)
    self.logger.debug('Transformed dataset')
    return cai_dataset

  @staticmethod
  def fill_intents(intents):
    """
    Fill the intents in a CAI-format

    Args :
      - intents (list) : list of all the intents of the original dataset

    Returns :
      - list : list of all the intents in a CAI-format
    """
    list_intents = []
    for intent in intents:
      dict_intent = {
        'name': intent['name'],
        'description': intent['description'] if intent['description'] is not None else "",
        'strictness': intent['strictness'],
        'expressions': []
        }
      list_intents.append(dict_intent)
    return list_intents

  @staticmethod
  def fill_gazettes(dataset_entities, dataset_synonyms, language):
    """
    Fill the gazettes in a CAI-format

    Args :
      - dataset_entities (list) : list of all the entities of the original dataset
      - dataset_synonyms (list) : list of all the synonyms of the original dataset
      - language (str) : the source language of the original dataset

    Returns :
      - list : list of all the synonyms in a CAI-format
    """
    gazettes = []
    entity_type = {
      0: 'gold',
      1: 'free',
      2: 'restricted'
    }
    for entity in dataset_entities:
      dict_gazette = {
        'name': entity['name'],
        'slug': entity['slug'],
        'locked': entity['locked'],
        'type': entity_type[entity['type']],
        'is_open': entity['is_open'],
        'strictness': entity['strictness'],
        'enrichment_strictness': entity['enrichment_strictness'],
        'synonyms': [],
        'regex_pattern': entity['regex_pattern'],
        'regex_flags': entity['regex_flags']
      }
      gazettes.append(dict_gazette)

    for synonym in dataset_synonyms:
      if synonym['language'] == language:
        gazettes[synonym['entity_id']]['synonyms'].append(synonym['value'])

    return gazettes

  @staticmethod
  def fill_expressions(cai_dataset_intents, gazettes, dataset_expressions, language):
    """
    Update the list of intents by filling the expressions in a CAI-format

    Args :
      - new_dataset_intents (list) : list of all the intents of the CAI-format dataset
      - gazettes (list) : list of all the synonyms of the original dataset
      - dataset_expressions (list) : list of all the expressions of the original dataset
      - language (str) : the source language of the original dataset
    """
    for expression in dataset_expressions:
      if expression['language'] == language:
        dict_expression = {
          'source': expression['source'],
          'tokens': json.loads(expression['tokens'])
        }
        for token in dict_expression['tokens']:
          if 'entity_id' in token.keys():
            entity = gazettes[token['entity_id']]
            token['entity'] = {
              'name': entity['name'],
              'type': entity['type'],
              'is_custom': entity['type'] != 'gold'
            }
            del token['entity_id']
          else:
            token['entity'] = None
        cai_dataset_intents[expression['intent_id']]['expressions'].append(dict_expression)
