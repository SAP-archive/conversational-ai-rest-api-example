#!/usr/bin/env python3
import re
import string
import time
import logging
from datetime import timedelta
from tqdm import tqdm
from .translator import SAPTranslationHubTranslator, NoneTranslator
from .cai_client import CaiClient

class DatasetTranslation:
  """
  Translates a CAI-format json dataset and imports the translated expressions and synonyms to the CAI platform and/or
  saves the translated CAI-format json dataset.
  """
  SIZE_BATCH = 10

  def __init__(self, api, source_language, target_language, user_slug, bot_slug, version_slug, developer_token, bot_client_id, bot_client_secret, client_id=None, client_secret=None):  # pylint: disable=line-too-long,too-many-arguments
    """
    Args :
        - api (str) : the Translator API
        - source_language (str) : the isocode of the source language
        - target_language (str) : the isocode of the target language
        - user_slug (str) : the user slug of the bot owner on the CAI platform
        - bot_slug (str) : the bot slug of the bot on the CAI platform
        - version_slug (str) : the version of the bot on the CAI platform
        - developer_token (str) : the developer token of the bot owner on the CAI platform
        - bot_client_id (str) : the bot's OAuth client id for authentication of Designtime APIs on the CAI platform
        - bot_client_secret (str) : the bot's OAuth client secret for authentication of Designtime APIs on the CAI platform
        - client_id (str) : the client id of the SAP Translation Hub API account (optional)
        - client_secret (str) : the client secret of the SAP Translation Hub API account (optional)
    """
    if api == 'saptranslationhub':
      self.translator = SAPTranslationHubTranslator(source_language, target_language, client_id, client_secret)
    else:
      self.translator = NoneTranslator(source_language, target_language)
    self.source_language = source_language
    self.target_language = target_language
    self.cai_client = CaiClient(user_slug, bot_slug, version_slug, developer_token, bot_client_id, bot_client_secret)
    self.logger = logging.getLogger(__name__)

  def dataset_translation(self, original_dataset):
    """
    Translates the expressions and synonyms and imports them on the platform,
    and/or saves the translated CAI-format json dataset.

    Args :
        - original_dataset (dict) : the CAI-format json dataset

    Returns :
        - dict : the translated datase
    """
    dataset = original_dataset
    dataset['language'] = self.target_language
    start = time.time()

    self.logger.info('Translating synonyms')
    dataset['gazettes'] = self.translate_synonyms(dataset['gazettes'])
    self.logger.debug('Translated synonyms')
    self.logger.info('Translating expressions')
    with tqdm(total=len([0 for intent in dataset['intents'] for _ in intent['expressions']]), desc='intents') as pbar:
      for intent in dataset['intents']:
        list_translations = self.translator.batch_translate([expression['source'] for expression in intent['expressions']],
                                                            self.SIZE_BATCH)
        for j, translation in enumerate(list_translations):
          intent['expressions'][j]['source'] = translation

        for expression in intent['expressions']:
          if not expression['source']:
            continue
          translated_non_gold_tokens = self.translate_non_gold_tokens(expression['tokens'], dataset['gazettes'])
          response_expression = self.cai_client.post_expression(intent['name'], expression['source'], self.target_language)
          list_tokens = self.convert_token_cai(response_expression['tokens'])
          expression['tokens'], expression['compiled'] = self.update_and_compile_expressions(list_tokens, translated_non_gold_tokens, expression, intent['name'], response_expression["id"])
        pbar.update(len(intent['expressions']))
    self.logger.debug('Translated expressions')
    self.logger.info(" Handled in %s", timedelta(seconds=round(time.time()-start)))
    return dataset

  def translate_synonyms(self, dataset_gazettes):
    """
    Translate the synonyms of the CAI-format dataset

    Args:
      - dataset_gazettes (list) : the list of all the synonyms of the dataset

    Returns:
      - list : the list of the translated synonyms
    """
    for entity_gazettes in tqdm(dataset_gazettes, desc='synonyms'):
      if entity_gazettes['synonyms']:
        entity_gazettes['synonyms'] = self.translator.batch_translate(entity_gazettes['synonyms'], self.SIZE_BATCH)
        self.cai_client.post_synonyms(entity_gazettes['slug'], entity_gazettes['synonyms'], self.target_language)
    return dataset_gazettes

  def translate_non_gold_tokens(self, tokens, dataset_gazettes):
    """
    Translate the tokens that are free or restricted entities and gather them in a hashmap with the corresponding
    index of the token in the expression

    Args:
      - tokens (dict) : all the tokens in the expression
      - dataset_gazettes (list) : the list of the synonyms

    Returns:
      - dict : all the possible translations of the free/restricted token with the corresponding index in the expression
    """
    translation_nongold_tokens = {}
    for token_key, original_token in enumerate(tokens):
      translation_tokens = []
      if original_token['entity'] is not None and original_token['entity']['type'] != 'gold':
        for gazette in dataset_gazettes:
          if original_token['entity']['name'] == gazette['name']:
            translation_token = self.translator.batch_translate([original_token['word']], 1)[0].lower()
            translations_to_add = gazette['synonyms'] if len(gazette['synonyms']) != 0 else translation_token
            translation_tokens.append(translations_to_add)
            if len(gazette['synonyms']) != 0 and translation_token not in gazette['synonyms']:
              translation_tokens.append(translation_token)
            translation_nongold_tokens[token_key] = translation_tokens
    for key, value in translation_nongold_tokens.items():
      translation_nongold_tokens[key] = self.flatten(value)
    return translation_nongold_tokens

  def update_and_compile_expressions(self, list_tokens, translated_non_gold_tokens, expression, intent_name, expression_id):
    """
    Update the expression with free and restricted entities, and update the compiled expression

    Args:
    - list_tokens (list) : the list of CAI-format tokens
    - translation_nongold_tokens (dict): all the possible translations of the free/restricted token with the
    corresponding index in the expression
    - expression (dict) : the expression
    - intent_name (str) : the intent name of the expression

    Returns:
      - list : the list of updated tokens
      - str : the updated compiled expression
    """
    expression_compiled = ''
    for index, token in enumerate(list_tokens):
      list_non_gold_tokens = [key for key, values in translated_non_gold_tokens.items() if token['word'].lower() in values]
      if len(list_non_gold_tokens) != 0:
        list_tokens[index] = expression['tokens'][list_non_gold_tokens[0]]
        list_tokens[index]['word'] = token['word']
        self.cai_client.update_expression(index, list_tokens[index], intent_name, expression['source'], expression_id)
        expression_compiled = self.add_entity_name(list_tokens[index]['entity']['name'], expression_compiled)
      elif token['entity'] is not None and token['entity']['type'] == 'gold':
        expression_compiled = self.add_entity_name(list_tokens[index]['entity']['name'], expression_compiled)
      else:
        expression_compiled += token['word'] + " " if token['pos'] != 'PUNCT' else ''
    return list_tokens, expression_compiled

  @staticmethod
  def convert_token_cai(tokens):
    """
    Convert import-format token to a CAI-format token

    Args :
        - tokens (list) : the import-format list of tokens

    Returns:
        - list : the list of CAI-format tokens
    """
    list_tokens = []
    for token in tokens:
      token_formatted = {
        'word': token['word']['name'],
        'space': token['space'],
        'pos': token['part_of_speech'],
        'entity': {'name': token['entity']['name'], 'type': token['entity']['type'], 'is_custom': token['entity']['custom']} if 'entity' in token else None
      }
      list_tokens.append(token_formatted)
    return list_tokens

  @staticmethod
  def flatten(list_to_flatten):
    """
    Flatten an irregular list of lists

    Args:
      - list_to_flatten (list) : the list to flatten

    Returns:
      - list : the flatten list
    """
    final_list = []
    for i in list_to_flatten:
      if isinstance(i, list):
        final_list.extend(i)
      else:
        final_list.append(i)
    return final_list

  @staticmethod
  def add_entity_name(entity_name, expression_compiled):
    """
    Add an entity name without punctuations in the compiled expression without duplication of the entity name

    Args :
      - entity_name (str) : the name of the entity
      - expression_compiled (str) : the compiled expression

    Returns:
      - str : the compiled expression with the entity name
    """
    regex = re.compile(f"[{re.escape(string.punctuation)}]")
    new_token_name = regex.sub('', entity_name)
    return re.sub(r"\b({})( \1\b)+".format(new_token_name), r"\1", expression_compiled + new_token_name + " ")
