#!/usr/bin/env python
# coding: utf-8

""" Bot to learn new words in english """

import os
from random import randint
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space


"""
$ python guess.py <token>
Guess a number:
1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a guess.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until guess is correct.
"""

from db import LangDB


class Player(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.db = LangDB()
        self.pair = self.db.pairs_random()

    @staticmethod
    def __hint__(word):
        index = randint(0, len(word) - 1)
        print word.encode('utf-8'), len(word), index
        hint = u'*' * (index) + word[index] + u'*' * (len(word) - index - 1)
        return hint

    def _hint(self):
        self.sender.sendMessage(u'Hint: {0}'.format(self.__hint__(self.pair.ru)).encode('utf-8'))

    def open(self, initial_msg, seed):
        self.sender.sendMessage('Try to translate word: {0}'.format(self.pair.en))
        return True  # prevent on_message() from being called on the initial message

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.sender.sendMessage('Talk with me with text messages please.')
            return

        text = msg['text']
        if text.startswith('/add') and len(text.split()) == 2:
            self.sender.sendMessage(
                'I supposed to add {0} word, but now I cant.'.format(text.split()[1]))

        if msg['text'].lower() != self.pair.ru.lower():
            hint = self._hint()
            self.sender.sendMessage(hint)
        else:
            self.sender.sendMessage('Correct! {0} is {1}'.format(
                self.pair.en, self.pair.ru.encode('utf-8')))
            self.close()

    def on__idle(self, event):
        self.sender.sendMessage('Game expired. The answer is %d' % self._answer)
        self.close()


def main():
    TOKEN = os.getenv(TOKEN)
    assert TOKEN, "You should export 'TOKEN' env variable"
    bot = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, Player, timeout=10),
    ])
    bot.message_loop(run_forever='Listening ...')


if __name__ == '__main__':
    main()
