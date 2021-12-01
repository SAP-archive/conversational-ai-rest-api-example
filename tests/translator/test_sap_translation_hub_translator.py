# coding: utf-8
import ast
import random
import requests
import pytest
from mock import patch, Mock
from dataset_translation.translator.sap_translation_hub_translator import SAPTranslationHubTranslator

def requests_mocked(status):
  mocked_requests = Mock()
  response = requests.Response()
  response.status_code = status
  response._content = b'{"access_token": "token"}'
  mocked_requests.post.return_value = response
  mocked_requests.request.return_value = response
  return mocked_requests

@pytest.fixture
@patch('dataset_translation.translator.sap_translation_hub_translator.requests', requests_mocked(200))
def sap_translation_hub_translator():
  return SAPTranslationHubTranslator('en', 'fr', 'id', 'secret')

class TestSAPTranslationHubTranslator:

  def test_supported_translation(self, sap_translation_hub_translator):
    combinations = [('en', 'fr'), ('en', 'es'), ('en', 'de'), ('fr', 'en'),
                    ('de', 'en'), ('de', 'fr'), ('de', 'es'), ('es', 'en')]
    randn = random.randint(0, len(combinations)-1)
    assert sap_translation_hub_translator.supported_translation(combinations[randn][0], combinations[randn][1]) is True

  def test_not_supported_translation(self, sap_translation_hub_translator):
    assert sap_translation_hub_translator.supported_translation('language1', 'language2') is False

  def test_sapcode_language(self, sap_translation_hub_translator):
    assert sap_translation_hub_translator.sapcode_language('fr') == 'fr-FR'
    assert sap_translation_hub_translator.sapcode_language('en') == 'en-US'
    assert sap_translation_hub_translator.sapcode_language('es') == 'es-ES'
    assert sap_translation_hub_translator.sapcode_language('de') == 'de-DE'

  def test_sapcode_language_error(self, sap_translation_hub_translator):
    with pytest.raises(KeyError):
      assert sap_translation_hub_translator.sapcode_language('language1')

  @patch('dataset_translation.translator.sap_translation_hub_translator.requests', requests_mocked(200))
  def test_batch_translate(self, sap_translation_hub_translator):
    translation = sap_translation_hub_translator.batch_translate(['hello'], 1)
    assert ast.literal_eval(translation[0])['access_token'] == 'token'
    assert isinstance(translation[0], str)
    assert isinstance(ast.literal_eval(translation[0]), dict)

  @patch('dataset_translation.translator.sap_translation_hub_translator.requests', requests_mocked(400))
  def test_batch_translate_error(self, sap_translation_hub_translator):
    with pytest.raises(ValueError):
      assert sap_translation_hub_translator.batch_translate(['hello'], 1)
