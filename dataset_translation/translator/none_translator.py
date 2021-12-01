from .translator import Translator

class NoneTranslator(Translator):

  def batch_translate(self, expressions, batch_size=None):
    return expressions
