from antlr4 import *
from .fukushuuLexer import fukushuuLexer
from .fukushuuParser import fukushuuParser
from .fukushuuVisitor import fukushuuVisitor


def main(source_code):
    _input = InputStream(source_code)
    lexer = fukushuuLexer(_input)
    stream = CommonTokenStream(lexer)
    parser = fukushuuParser(stream)
    tree = parser.start_rule()
    visitor = fukushuuVisitor()
    visitor.setParser(parser)
    return visitor.visit(tree)


if __name__ == '__main__':
    main("")
