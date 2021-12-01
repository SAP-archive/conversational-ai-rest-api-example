import requests

class CaiClient:
  """
  The CAI public API
  """
  def __init__(self, user_slug, bot_slug, version_slug, developer_token, bot_client_id, bot_client_secret):
    """
    Args :
        - user_slug (str) : the user slug of the bot owner on the CAI platform
        - bot_slug (str) : the bot slug of the bot on the CAI platform
        - version_slug (str) : the version of the bot on the CAI platform
        - developer_token (str) : the developer token of the bot owner on the CAI platform
        - bot_client_id (str) : the bot's OAuth client id for authentication of Designtime APIs on the CAI platform
        - bot_client_secret (str) : the bot's OAuth client secret for authentication of Designtime APIs on the CAI platform
    """
    self.headers = {
                      'Authorization': f"Bearer {self.get_access_token(bot_client_id, bot_client_secret)}",
                      'Content': 'application/json',
                      'X-Token': 'Token ' + developer_token
                   }
    self.url_prefix = f"https://api.cai.tools.sap/train/v2/users/{user_slug}/bots/{bot_slug}/versions/{version_slug}/dataset"
    self.list_entities = self.get_entities()

  @staticmethod
  def get_access_token(bot_client_id, bot_client_secret):
    """
    Getter of access token for the authentication on the CAI platform

    Returns:
      - str : the access token
    """
    payload = {'grant_type': 'client_credentials', 'client_id': bot_client_id, 'client_secret': bot_client_secret}
    response = requests.post('https://sapcai-community.authentication.eu10.hana.ondemand.com/oauth/token', data=payload)
    return response.json()['access_token']

  def get_entities(self):
    """
    Getter of the entities of the bot on the CAI platform

    Returns:
        - list : all the entities of the bot
    """
    response = requests.get(f"{self.url_prefix}/entities", headers=self.headers)
    return response.json()['results']


  def convert_token_cai(self, index, token_cai_format):
    """
    Convert a CAI-format token to an import-format token

    Args :
        - index (int) : the index of the token in the expression
        - token_CAI_format (dict) : the CAI-format token

    Returns:
        - dict : the import-format token
    """
    token_formatted = {
      'ind': index,
      'space': token_cai_format['space'],
      'part_of_speech': token_cai_format['pos'],
      'word': {'name': token_cai_format['word']}
    }
    if token_cai_format['entity'] is not None:
      token_formatted["entity"] = [entity for entity in self.list_entities if entity['name'] == token_cai_format['entity']['name']][0]
    return token_formatted

  def update_expression(self, index, token, intent, expression, expression_id):
    """
    Update an expression on the CAI platform

    Args :
    - index (int) : the index of the token in the expression
    - token (dict) : the import-format token
    - intent (str) : the corresponding intent of the token and expression
    - expression (str) : the corresponding expression of the token
    - expression_id (str) : the corresponding id of the expression of the token
    """
    response = requests.put(f"{self.url_prefix}/intents/{intent}/expressions/{expression_id}",
                            json={'source': expression, 'tokens': [self.convert_token_cai(index, token)]},
                            headers=self.headers
                            )
    if response.status_code != 200:
      raise ValueError(response.text)


  def post_expression(self, intent, expression, target_language):
    """
    Import an expression on the CAI platform

    Args :
    - intent (str) : the corresponding intent of the expressions
    - expression (str) : the expression to import
    - target_language (str) : the isocode of the target language
    """
    response = requests.post(f"{self.url_prefix}/intents/{intent}/expressions",
                             json={
                               'source': expression,
                               'language': {'isocode': target_language}
                             },
                             headers=self.headers
                             )
    if response.status_code in (200, 201):
      return response.json()['results']
    raise ValueError(response.text)


  def post_synonyms(self, entity_slug, synonyms, target_language):
    """
    Import a list of synonyms on the CAI platform

    Args :
    - entity_slug (str) : the corresponding entity slug
    - synonyms (list) : the list of synonyms to import
    - target_language (str) : the isocode of the target language
    """
    list_synonyms = []
    for synonym in synonyms:
      synonym_formatted = {'value': synonym, 'language': {'isocode': target_language}}
      list_synonyms.append(synonym_formatted)
    response = requests.post(f"{self.url_prefix}/entities/{entity_slug}/synonyms/bulk_create",
                             json={'synonyms': list_synonyms}, headers=self.headers)
    if response.status_code not in (200, 201):
      raise ValueError(response.text)
