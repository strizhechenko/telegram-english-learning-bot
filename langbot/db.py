#!/usr/bin/env python
# coding: utf-8

""" sqlite "backend" """

from sqlite3 import Connection
from random import randint
from pair import Pair


class LangDB(object):

    def __init__(self, filename='lang.db'):
        self.conn = Connection(filename)
        self.create_db_if_required()

    def create_db_if_required(self):
        check = """
        SELECT
            count(name)
        FROM
            sqlite_master
        WHERE
            type = 'table'
            AND name = 'words'
        """

        create = """
        CREATE TABLE words (
            id integer primary key autoincrement,
            ru varchar[256],
            en varchar[256],
            ok integer,
            fail intgeger
        );
        """
        if not self.conn.execute(check).next()[0]:
            self.conn.execute(create)

    def pairs_count(self):
        count = """
        SELECT
            count(ok)
        FROM
            words;
        """
        return list(self.conn.execute(count))[0][0]

    def pairs_random(self):
        count = self.pairs_count()
        return Pair(list(self.conn.execute(
            "SELECT * FROM words WHERE id == {0}".format(randint(1, count))
        ))[0])

    def pairs_add(self, ru, en):
        insert = """
        INSERT INTO words
            (ru, en, ok, fail)
        VALUES
            ('{0}', '{1}', 0, 0);
        """.format(ru, en)
        print insert
        self.conn.execute(insert)
        self.conn.commit()


if __name__ == '__main__':
    db = LangDB()
    # db.pairs_add("Ящерка", "Lizard")
    # db.pairs_add("ЕБМ", "EBM")
    # db.pairs_add("Кот", "Cat")
    pair = db.pairs_random()
    print pair.ru
    _en = raw_input()
    print _en.lower() == pair.en.lower() and 'OK' or 'FAIL'
