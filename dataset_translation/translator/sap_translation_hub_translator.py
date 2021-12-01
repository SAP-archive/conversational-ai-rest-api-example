import unicodedata
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .translator import Translator


class SAPTranslationHubTranslator(Translator):
  """Translator using the SAP Translation Hub API"""
  def __init__(self, source_language, target_language, client_id, client_secret):
    """
    Args :
    - source_language (str) : the isocode of the source language
    - target_language (str) : the isocode of the target language
    - client_id (str) : the client id of the SAP Translation Hub API account
    - client_secret (str) : the client secret of the SAP Translation Hub API account
    """
    if self.supported_translation(source_language, target_language):
      source_language_sapcode = self.sapcode_language(source_language)
      target_language_sapcode = self.sapcode_language(target_language)
      super().__init__(source_language_sapcode, target_language_sapcode)
      self.client_id = client_id
      self.client_secret = client_secret
      self.token = self.login()
      self.url = f"https://document-translation.cfapps.sap.hana.ondemand.com/api/v1/translation?sourceLanguage={source_language_sapcode}&targetLanguage={target_language_sapcode}"
    else:
      raise ValueError('Translation not supported')

  def login(self):
    """Login method

    Returns :
        - str : the access token
    """
    token_url = 'https://translation.authentication.sap.hana.ondemand.com/oauth/token'
    access_token_response = requests.post(token_url, data={'grant_type': 'client_credentials'}, verify=False,
                                          allow_redirects=False, auth=(self.client_id, self.client_secret))
    return access_token_response.json()['access_token']


  def batch_translate(self, expressions, batch_size):
    """Translation method

    Args :
        - expressions (list) : a list of expressions to be translated
        - batch_size (int) : the size of the batch to split the expressions to translate

    Returns:
        - list : the list of translated expressions
    """
    translations = []
    for i in range(0, len(expressions), batch_size):
      batch_expressions = []
      for expression in expressions[i:min(i+batch_size, len(expressions))]:
        batch_expressions.append(expression)

        encoder = MultipartEncoder(
          fields={
            'file': ('null', ' \n '.join(batch_expressions), 'text/plain'),
          }
        )

        headers = {
          'Authorization': f"Bearer {self.token}",
          'Content-type': encoder.content_type
        }

      response = requests.request('POST', self.url, headers=headers, data=encoder)

      if response.status_code == 200:
        translations.append(unicodedata.normalize('NFKD', response.text).split(' \n '))
      else:
        raise ValueError(response.text)
    return [item for sublist in translations for item in sublist]

  @staticmethod
  def sapcode_language(language):
    """
    Convert the language isocode to the SAP Translation Hub code.

    Args :
        - language (str) : the language isocode

    Returns :
        - str : the SAP Translation Hub code of the language
    """
    sapcode_language = {
      'fr': 'fr-FR',
      'en': 'en-US',
      'es': 'es-ES',
      'de': 'de-DE'
    }
    return sapcode_language[language]

  @staticmethod
  def supported_translation(source_language, target_language):
    """
    Verify if the translation is supported by the SAP Translation Hub API
    Args :
        - source_language (str) : the isocode of the source language
        - target_language (str) : the isocode of the target language

    Returns:
        - boolean : the state if the translation is supported by SAP Translation Hub or not
    """
    combinations = [('en', 'fr'), ('en', 'es'), ('en', 'de'), ('fr', 'en'),
                    ('de', 'en'), ('de', 'fr'), ('de', 'es'), ('es', 'en')]
    return (source_language, target_language) in combinations
