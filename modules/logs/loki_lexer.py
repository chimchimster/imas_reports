from pygments.lexer import RegexLexer
from pygments.token import *


class LokiLexer(RegexLexer):
    name = 'Loki loves highlight states and tracebacks.'

    tokens = {
        'root': [
            (r'(\'level.*?(?=,))', Generic.Error),
            (r'(\'logged_at.*?(?=,))', Literal.Date),
        ]
    }
