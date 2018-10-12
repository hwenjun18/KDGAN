from nltk.corpus import wordnet
from operator import itemgetter
from sys import stdout

import string

dataset_file = '/data/yfcc100m/yfcc100m_dataset'
tag_file = '/data/yfcc100m/yfcc100m_tag'
tmp_file = '/data/yfcc100m/yfcc100m_tmp'

sup_tag = 20

num_field = 25
idx_field = 10
idx_marker = 24

sep_tag = ','
sep_word = '+'

wn_nouns = {synset.name().split('.')[0] for synset in wordnet.all_synsets('n')}
def is_valid(tag):
  ### one word tag
  if sep_word in tag:
    return False
  v_char = string.ascii_lowercase + '-'
  if any(c not in v_char for c in tag):
    return False
  # if not wordnet.synsets(tag):
  #   return False
  if not tag in wn_nouns:
    return False
  return True

def main():
  count = 0
  tags = []
  with open(tag_file) as fin:
    while True:
      line = fin.readline()
      if not line:
        break

      tag = line.strip().split()[0]
      valid = is_valid(tag)
      if valid:
        count += 1
        tags.append(tag)
  assert count == len(tags)
  with open(tmp_file, 'w') as fout:
    for tag in tags:
      fout.write('%s\n' % (tag))
  print('%d valid tags' % (count))

def test():
  tag_count = {}
  t_line = 0
  with open(dataset_file) as fin:
    while True:
      line = fin.readline()
      if not line:
        break

      fields = line.strip().split('\t')
      assert len(fields) == num_field

      if fields[idx_marker] != '0': # not image
        continue
      if len(fields[idx_field]) == 0: # no tags
        continue
      tags = fields[idx_field].split(sep_tag)
      for tag in tags:
        tag = tag.lower()
        words = tag.split(sep_word)
        valid = True
        for word in words:
          if not is_valid(word):
            valid = False
            break
        if valid:
          tag_count[tag] = tag_count.get(tag, 0) + 1

      t_line += 1
      # if t_line == 50000:
      #   break
      if (t_line % 5000000) == 0:
        print('line#%09d' % (t_line))
  print('%s contains %d lines in total' % (dataset_file, t_line))

  tag_count = sorted(tag_count.items(), key=itemgetter(1), reverse=True)
  with open(tag_file, 'w') as fout:
    for tag, count in tag_count:
      if count < sup_tag:
        break
      fout.write('%s\t%d\n' % (tag, count))

if __name__ == '__main__':
  main()


