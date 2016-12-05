#!/usr/bin/python

""" English words batch translator """

from sys import argv
from os import getenv
from os.path import isfile
from requests import get


class Translator(object):

    def __init__(self, token):
        self.token = token
        self.endpoint = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def translate_word(self, word):
        """ We really send request here """
        params = {
            "text": word,
            "lang": "en-ru",
            "key": self.token
        }
        responce = get(self.endpoint, params=params).json().get(u'text', [])
        return len(responce) > 0 and responce[0] or None

    def translate_word_list(self, word_list):
        """ Reason why this code exist: multiple words translation """
        return {word: self.translate_word(word) for word in word_list}

    def translate_markdown_file(self, filename):
        """ I keep my words in markdown files with one list:
        - word1
        - word2
        """
        words = (line.strip().replace('- ', '') for line in open(filename, 'r').xreadlines())
        return self.translate_word_list(words)

    @staticmethod
    def translations_print(translations):
        """ Output format:
        - word1 - translation1
        - word2 - translation2
        """
        for word, translation in translations.items():
            print '- {0} - {1}'.format(word, translation.encode('utf-8'))


def main():
    """ To run it you should:
    1. define env variable 'TOKEN'
    2. pass filename as arg1
    Example: TOKEN=blabla ./translator.py TES.md
    """
    token = getenv('TOKEN')
    filename = argv[1]
    assert token, "'TOKEN' variable should be defined via env"
    assert isfile(filename), "{0} not found.".format(filename)
    translator = Translator(token)
    translations = translator.translate_markdown_file(filename)
    translator.translations_print(translations)

if __name__ == '__main__':
    main()
