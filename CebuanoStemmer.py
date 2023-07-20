import sys

PREFIXES = ['ipagpakig', 'ipagpaki', 'magapaka', 'mahapang',
              'mahipang', 'makapang', 'nagapaka', 'nahapang',
              'nahipang', 'nakapang', 'pagapaka', 'pagpakig',
              'pagpanig', 'gipakig', 'gipanag', 'gipangi',
              'gipanhi', 'gipanig', 'magpaka', 'mahapam',
              'mahapan', 'mahipam', 'mahipan', 'masighi',
              'nagpaka', 'nahapam', 'nahapan', 'nahipam',
              'nahipan', 'nakapam', 'nakapan', 'nasighi',
              'pagpaha', 'pagpahi', 'pagpaka', 'pagpaki',
              'pagpani', 'pasighi', 'gipaka', 'gipaki',
              'gipang', 'gipani', 'ipakig', 'magahi',
              'magaka', 'magapa', 'mapang', 'nagahi',
              'nagaka', 'nagapa', 'napang', 'pagahi',
              'pagaka', 'pagapa', 'pinaka', 'gipam',
              'gipan', 'ipaki', 'ipang', 'maghi',
              'magka', 'magpa', 'makig', 'manag',
              'mangi', 'manhi', 'manig', 'manum',
              'mapam', 'mapan', 'masig', 'naghi',
              'nagka', 'nagpa', 'nakig', 'nanag',
              'nangi', 'nanhi', 'nanig', 'nanum',
              'napam', 'napan', 'nasig', 'paghi',
              'pagka', 'pagpa', 'panag', 'pangi',
              'panhi', 'pasig', 'gihi', 'gika',
              'gina', 'gipa', 'hing', 'ikaw',
              'ipam', 'ipan', 'kina', 'maga',
              'maha', 'mahi', 'maka', 'maki',
              'mang', 'mani', 'mapa', 'ming',
              'naga', 'naha', 'nahi', 'naka',
              'naki', 'nang', 'nani', 'napa',
              'ning', 'paga', 'paha', 'pahi',
              'paka', 'pang', 'pani', 'hin',
              'iga', 'ika', 'ipa', 'mag', 'mai',
              'mam', 'man', 'nag', 'nai', 'nam',
              'nan', 'pag', 'pam', 'pan', 'ga',
              'gi', 'hi', 'ka', 'ma', 'mi', 'mo',
              'na', 'ni', 'pa', 'i']

INFIXES = ['in', 'g']

SUFFIXES = ['han', "'y", 'ng', 'an', 'on', 'ay', 'i', 'a', 'g']

def stemmer(source, info, mode):
  '''
    Main stemmer method
    STRING source - either text to stem or name of file to stem
    BOOLEAN info - True if print out all details of stemming
    INTEGER mode - 1) read from string
                   2) read from file, no write
                   3) read from file, write to new file
  '''
  chars = ".'?!@#$%^&*()_+=/\\{}[]\""

  src_text = ""
  
  if mode != 1:
    with open(source, 'r') as sr:
      src_text = sr.read()
  else:
    src_text = source

  for char in chars:
    src_text = src_text.replace(char, '')
  src_text = ' '.join(src_text.split('\n'))
  tokens = src_text.split(' ')

  stems_info = []
  stems = []

  for token in tokens:
    if token != '':
      word = {}
      duplicates = []
      prefs = []
      infs = []
      suffs = []
      token = token.lower().strip()

      dup_stem = check_duplicate(token, duplicates)
      pre_stem = check_prefix(dup_stem, prefs)
      suf_stem = check_suffix(pre_stem, suffs)
      inf_stem = check_infix(suf_stem, infs)
      suf_stem = check_suffix(inf_stem, suffs)
      dup_stem = check_duplicate(suf_stem, duplicates)
      stem = clean(dup_stem, word)

      word["original"] = token

      if validate(stem):
        word["root"] = stem
        stems.append(stem)

        if len(duplicates) != 0:
          word["duplication"] = duplicates

        if len(prefs) != 0:
          word["prefixes"] = prefs
        
        if len(infs) != 0:
          word["infixes"] = infs
        
        if len(suffs) != 0:
          word["suffixes"] = suffs
      else:
        word["root"] = token
        stems.append(token)

      stems_info.append(word)

  if mode == 3:
    name = source[:source.find(".")] + "_stemmed.txt"
    with open(name, 'w') as out:
      if info:
        for w in stems_info:
          out.write(str(w))
      else:
        out.write(str(stems))

  return stems


def check_duplicate(token, duplicates):
  '''
    Checks for duplication.
  '''
  if validate(token):
    return token

  if '-' in token:
    loc = token.find('-')
    if token[:loc] == token[(loc + 1):]:
      duplicates.append(token[:loc])
      return token[:loc]
    else:
      return token
  else:
    return token


def check_prefix(token, prefs):
  '''
    Checks for and removes prefixes.
  '''

  if validate(token):
    return token

  for prefix in PREFIXES:
    if token[:len(prefix)] == prefix:
      prefs.append(prefix)
      return token[len(prefix):]
    else:
      pass

  return token


def check_infix(token, infs):
  '''
    Checks for and removes infixes.
  '''

  if validate(token):
    return token

  for infix in INFIXES:
    if infix in token:
      sep = token.find(infix)
      if validate(token[:sep] + token[(sep + len(infix)):]) and token[(sep + len(infix)):] != '':
        infs.append(infix)
        return token[:sep] + token[(sep + len(infix)):]
      else:
        new_text = token[(sep + len(infix)):]
        if infix in new_text:
          sep2 = new_text.find(infix)
          test = token[:(sep + len(infix) + sep2)] + token[(sep + (2 * len(infix)) + sep2):]
          if validate(test):
            infs.append(infix)
            return test
          else:
            return token
    else:
      pass
  return token


def check_suffix(token, suffs):
  '''
    Checks for and removes suffixes.
  '''

  if validate(token):
    return token

  for suffix in SUFFIXES:
    if token[-len(suffix):] == suffix:
      suffs.append(suffix)
      return token[:-len(suffix)]
    else:
      pass

  return token


def clean(token, word_dict):
  '''
    Cleans stemmed token.
  '''
  return token


def validate(token):
  '''
    Checks if token is a valid token.
  '''

  with open("cebuano_dict.txt", 'r') as validation:
    val_set = validation.read().split('\n')

  return token in val_set