from optparse import OptionParser


class ConverterOptionParser(OptionParser):

    def __init__(self):
        OptionParser.__init__(self)
        self.add_option("-f", "--file")
        self.add_option("-s", "--src-format",
                        help="[markdown | json], default: markdown", default="markdown")
        self.add_option("-d", "--dst-format",
                        help="[markdown | json], default: json", default="json")
        self.add_option("-a", "--answers",
                        help="use it if input file contains answers", action="store_true", default=False)


if __name__ == '__main__':
    parser = ConverterOptionParser()
    options, args = parser.parse_args()
    print options
