from utils import *

import utils

from os import path

import argparse
import os
import pickle
import requests
import time

import logging
logging.basicConfig(level=logging.INFO, format=log_format)

def main(url_fold_file):
  image_fold_dir = url_fold_file.replace('url_', 'image_')

  with open(url_fold_file) as fin:
    for line in fin.readlines():
      image_url = line.strip()
      image_file = utils.get_image_file(image_fold_dir, image_url)
      if path.isfile(image_file):
        latest_image_url = image_url
  print(image_url)
  exit()

  tot_image, num_image = 0, 0
  with open(url_fold_file) as fin:
    for line in fin.readlines():
      image_url = line.strip()
      image_file = utils.get_image_file(image_fold_dir, image_url)
      tot_image += 1
      if (tot_image % 100) == 0:
        logging.info('tot=%07d num=%d' % (tot_image, num_image))
      if path.isfile(image_file):
        num_image += 1
        continue
      while True:
        try:
          response = requests.get(image_url)
          time.sleep(1)
          break
        except Exception:
          time.sleep(10)
          logging.info('retry %s' % (image_url))
      if image_url != response.url:
        continue
      image_dir = path.dirname(image_file)
      if not path.exists(image_dir):
        os.makedirs(image_dir)
      with open(image_file, 'wb') as fout:
        fout.write(response.content)
      num_image += 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('url_fold_file', type=str)
  args = parser.parse_args()
  main(args.url_fold_file)
