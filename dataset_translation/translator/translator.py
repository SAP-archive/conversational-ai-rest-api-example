class Translator:
  """
  Interface for each translator, inherited for translator building.

  - `translate` method to translate an expression from a language to another
  - `batch_translate` method to translate a list of expressions from a language to another
  """

  def __init__(self, source_language, target_language):
    """
    Args :
        - source_language (str) : the isocode of the source language
        - target_language (str) : the isocode of the target language
    """
    self.source_language = source_language
    self.target_language = target_language

  def batch_translate(self, text, batch_size):
    raise NotImplementedError
