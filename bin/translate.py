#!/usr/bin/env python
# coding: utf-8

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from dataset_translation.translation import main  # pylint: disable=wrong-import-position


if __name__ == '__main__':
  main()
