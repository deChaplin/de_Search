import json
import API.apiUtils as apiUtils

from collections import namedtuple

def search_dict(word):
    response = json.loads(apiUtils.getDict(word))

    noun_definition = []
    verb_definition = []

    for i in response:
        for j in i['meanings']:
            if j['partOfSpeech'] == 'noun':
                for k in j['definitions']:
                    noun_definition.append(k['definition'])
            elif j['partOfSpeech'] == 'verb':
                for k in j['definitions']:
                    verb_definition.append(k['definition'])

    return noun_definition[:3], verb_definition[:3]
