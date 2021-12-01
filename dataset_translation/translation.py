#!/usr/bin/env python3

import argparse
import json
import zlib

from .dataset_translation import DatasetTranslation
from .dataset import Dataset


def open_file(dataset_path):
  """
  Open a JSON dataset in the dataset path

  Args :
    - dataset_path (str) :  the dataset path

  Returns :
    - dict : the loaded dataset
  """
  try :
    with open(dataset_path, 'r') as file:
      return json.load(file)
  except UnicodeDecodeError:
    with open(dataset_path, 'rb') as file:
      read_file = file.read()
      return json.loads(zlib.decompress(read_file), encoding='utf-8')


def write_file(dataset_path, dataset):
  """
  Save a JSON dataset in the dataset path

  Args :
      - dataset_path (str) : the dataset path
      - data (dict) : the dataset to save
  """
  with open(dataset_path, 'w') as outfile:
    json.dump(dataset, outfile, indent=4, ensure_ascii=False)


def main():
  argparser = argparse.ArgumentParser(prog='dataset_translation.py', description='Translate a CAI json dataset')
  argparser.add_argument('--path', '-p', nargs='?', metavar='DATASET_PATH', type=str, required=True,
                         help='the path of the dataset')
  argparser.add_argument('--api', '-a', choices=['saptranslationhub', 'none'], default='saptranslationhub',
                         nargs='?', metavar='API_TRANSLATOR', type=str,
                         help='the API translator (saptranslationhub or none)')
  argparser.add_argument('--sourcelang', '-s', choices=['en', 'de', 'fr', 'es'], default='en', nargs='?',
                         metavar='SOURCE_LANGUAGE', type=str, required=True, help='the source language')
  argparser.add_argument('--targetlang', '-t', choices=['en', 'fr', 'es', 'de'], default='fr', nargs='?',
                         metavar='TARGET_LANGUAGE', type=str, required=True,
                         help='the target language (en, fr, es or de)')
  argparser.add_argument('--userslug', '-user', nargs='?', metavar='USER_SLUG', type=str, required=True,
                         help='the user slug of the bot')
  argparser.add_argument('--botslug', '-bot', nargs='?', metavar='BOT_SLUG', type=str, required=True,
                         help='the bot slug of the bot')
  argparser.add_argument('--versionslug', '-version', nargs='?', metavar='VERSION_SLUG', type=str, required=True,
                         help='the version of the bot')
  argparser.add_argument('--developertoken', '-devtoken', nargs='?', metavar='DEV_TOKEN', type=str, required=True,
                         help='the CAI developer token of the bot')
  argparser.add_argument('--botclientid', '-botid', nargs='?', metavar='BOT_ID', type=str, required=True,
                         help='the CAI client id of the bot')
  argparser.add_argument('--botclientsecret', '-botsecret', nargs='?', metavar='BOT_SECRET', type=str, required=True,
                         help='the CAI client secret of the bot')
  argparser.add_argument('--clientid', '-id', nargs='?', metavar='CLIENT_ID', type=str,
                         help='the client ID for SAP Translation Hub')
  argparser.add_argument('--clientsecret', '-secret', nargs='?', metavar='CLIENT_SECRET', type=str,
                         help='the client secret for SAP Translation Hub')
  argparser.add_argument('--savefile', '-save', action='store_true',
                         help='to save the translated CAI JSON dataset')
  argparser.add_argument('--formatfile', '-format', choices=['cai_platform', 'cai'], default='cai_platform', nargs='?',
                         metavar='FORMAT_FILE', type=str, help='the format of the dataset in input')

  args = argparser.parse_args()

  if args.api == 'saptranslationhub':
    data_translator = DatasetTranslation(args.api, args.sourcelang, args.targetlang, args.userslug, args.botslug,
                                         args.versionslug, args.developertoken, args.botclientid, args.botclientsecret,
                                         client_id=args.clientid, client_secret=args.clientsecret)
  elif args.api == 'none':
    data_translator = DatasetTranslation(args.api, args.sourcelang, args.targetlang, args.userslug, args.botslug,
                                         args.versionslug, args.developertoken, args.botclientid, args.botclientsecret)
  else:
    raise ValueError('translator API is not valid')

  dataset = open_file(args.path)
  if args.formatfile == 'cai_platform':
    dataset = Dataset().to_cai_format(dataset, args.sourcelang)
  translated_data = data_translator.dataset_translation(dataset)

  if args.savefile:
    write_file(f"{args.path[:-5]}-{args.targetlang}-translated-{args.api}.json", translated_data)
