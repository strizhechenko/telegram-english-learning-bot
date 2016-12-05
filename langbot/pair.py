class Pair(object):

    def __init__(self, _tuple):
        assert len(_tuple) == 5
        self.id, self.ru, self.en, self.ok, self.fail = _tuple

    def __str__(self):
        return u"id={0} ru={1} en={2} ok={3} fail={4}".format(self.id, self.ru,
                                                              self.en, self.ok, self.fail).encode('utf-8')
