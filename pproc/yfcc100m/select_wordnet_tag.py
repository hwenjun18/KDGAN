from utils import *

import utils

from nltk.corpus import wordnet
from os import path

import argparse
import calendar
import gzip
import io
import pickle
import pycountry
import string

import logging
logging.basicConfig(level=logging.INFO, format=log_format)

world_city_file = '/data/worldcitiespop.txt'
def get_wordnet_excl():
  wordnet_excl = set()

  for month in range(1, 13):
    wordnet_excl.add(calendar.month_name[month].lower())
    wordnet_excl.add(calendar.month_abbr[month].lower())
  for day in range(0, 7):
    wordnet_excl.add(calendar.day_name[day].lower())
    wordnet_excl.add(calendar.day_abbr[day].lower())

  for country in pycountry.countries:
    wordnet_excl.add(country.alpha_2.lower())
    wordnet_excl.add(country.alpha_3.lower())
    wordnet_excl.add(country.name.lower())
  for country in pycountry.historic_countries:
    wordnet_excl.add(country.alpha_3.lower())
    wordnet_excl.add(country.alpha_4.lower())
    wordnet_excl.add(country.name.lower())
  for subdivision in pycountry.subdivisions:
    wordnet_excl.add(subdivision.name.lower())
    wordnet_excl.add(subdivision.code.lower())

  city_names = []
  with open(world_city_file, encoding='iso-8859-1') as fin:
    line = fin.readline()
    while True:
      line = fin.readline()
      if not line:
        break
      fields = line.strip().split(',')
      country_code, city_name = fields[0], fields[1]
      wordnet_excl.add(country_code)
      city_names.extend(city_name.split())
  wordnet_excl = wordnet_excl.union(city_names)

  imagenet_tag_set = pickle.load(open(in_all_noun_pfile, 'rb'))
  wordnet_excl = wordnet_excl.union(imagenet_tag_set)

  return wordnet_excl

wordnet_char = string.ascii_lowercase + '-'
wordnet_excl = get_wordnet_excl()
def is_wordnet_tag(word):
  if word in wordnet_excl:
    return False
  if len(word) < 4:
    return False
  if any(c not in wordnet_char for c in word):
    return False
  synsets = wordnet.synsets(word)
  for synset in synsets:
    if synset.name().split('.')[1] != 'n':
      return False
  return True

def main():
  synsets = wordnet.all_synsets('n')
  word_list = [synset.name().split('.')[0] for synset in synsets]

  wordnet_tag_set = set()
  for word in word_list:
    if is_wordnet_tag(word):
      wordnet_tag_set.add(word)
  utils.save_set_readable(wordnet_tag_set, wn_all_noun_rfile)
  pickle.dump(wordnet_tag_set, open(wn_all_noun_pfile, 'wb'))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--override', action='store_true')
  args = parser.parse_args()
  if not path.isfile(wn_all_noun_pfile) or args.override:
    main()
  else:
    logging.info('do not override')