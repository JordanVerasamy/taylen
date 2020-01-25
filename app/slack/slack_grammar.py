from price_parser import Price
from pyparsing import Suppress, alphanums, Word, nums, printables, Combine, Regex, Literal, Optional

_String = Word(printables)
_Int = Word(nums).setParseAction(lambda s, loc, toks: int(toks[0]))
# <@U088EGWEL> --> U088EGWEL
_User = Combine(
    Suppress('<@') +
    Word(alphanums) +
    Suppress('>')
)
# <#C052EM50K|waterloo> --> C052EM50K
_Channel = Combine(
    Suppress('<#') +
    Word(alphanums) +
    Word(printables.replace('>', '')).suppress() +
    Suppress('>')
)
# <mailto:tsohlson@gmail.com|tsohlson@gmail.com> --> tsohlson@gmail.com
_Email = Combine(
    Suppress('<mailto:') +
    Word(alphanums + '@.') +
    Word(printables.replace('>', '')).suppress() +
    Suppress('>')
)
# :simple_smile:
_Emoji = Combine(
    Suppress(':') +
    Word(printables.replace(':', '')) +
    Suppress(':')
)

_Money = Regex(r'[0-9$\.]+').setParseAction(lambda s, loc, toks: Price.fromstring(toks[0]).amount_float)
_RestOfInput = Regex(r'.*')
_Direction = Literal('to') | Literal('from')
_Full = Optional(Literal('full'))
_Commands = Literal('help') | Literal('ping') | Literal('pong') | Literal('sw') | Literal('mmr') | Literal('record')

_help = Literal('.help')
_help_advanced = Literal('.help') + Optional('.').suppress() + _Commands
_ping = Literal('.ping')
_pong = Literal('.pong')
_splitwise = Literal('.sw') + _Money + _Direction + _User + _RestOfInput
_mmr = Literal('.mmr') + _String + _RestOfInput
_record = Literal('.record') + _Emoji + _Full

grammar = _help_advanced \
          | _help \
          | _ping \
          | _pong \
          | _splitwise \
          | _mmr \
          | _record
