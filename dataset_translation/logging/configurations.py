# coding: utf-8

import inspect

# Gets the package of the importing module to dynamically set the top-level logger level.
#
# If we used the 'root' logger config key, ALL libraries would be logging with a debug level.
#
# One drawback is that the '12th' frame of the stack is hardcoded and require the line importing
# this config to be like the following: `from dataset_translation.logging import [...]`.
# If it's not, we will most probably use a frame belonging to importlib, thus not have a __package__
# and we fall back to 'dataset_translation'
module = inspect.getmodule(inspect.stack()[12][0])
IMPORTER = module.__package__ if module and module.__package__ else 'dataset_translation'


STANDARD_CONSOLE_CONFIGURATION = {
  'version': 1,
  'disable_existing_loggers': True,
  'incremental': False,
  'formatters': {
    'default': {
      'format': '%(asctime)s - %(name)s - %(processName)s - %(levelname)s - %(message)s'
    }
  },
  'filters': {},
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'default'
    },
  },
  'loggers': {
    IMPORTER: {
      'level': 'DEBUG',
      'handlers': ['console']
    }
  }
}
