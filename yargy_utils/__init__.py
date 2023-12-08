import logging

from yargy import or_, rule, and_
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram, eq, length_eq, is_capitalized, type
from yargy.relations import gnc_relation
from yargy.tokenizer import MorphTokenizer, EOL

from yargy_utils.id_tokenizer import IdTokenizer
from yargy_utils.show_result import show_json, show_matches

logging.disable(logging.CRITICAL)

# для согласования слов
gnc = gnc_relation()
# сущиствительное
NOUN = gram('NOUN')
# полное прилагательное
ADJF = gram('ADJF')
# краткое прилагательное
ADJS = gram('ADJS')
# любая буква русского алфавита
ANY_LETTER = morph_pipeline(list('абвгдеёжзийклмнопрстуфхцчшщьыъэюя'))

# предлог
PREP = gram('PREP')
# союз
CONJ = gram('CONJ')
# запятая
COMMA = eq(',')
# точка
DOT = eq('.')
# число
INT = type('INT')
# разделитель в виде союза или знака препинания
SEPARATOR = or_(COMMA, CONJ)
# числительное
NUMR = gram('NUMR')
PERCENT = eq('%')
NUMERO_SIGN = eq('№')
SLASH = eq('/')
DECIMAL = rule(INT,
               or_(COMMA, DOT),
               INT)
INTORDEC = or_(rule(INT), DECIMAL)
ANY_NUM = rule(or_(
    rule(INT),
    DECIMAL
))
COLON = eq(':')
SEMICOLON = eq(';')
EQUAL_SIGN = eq('=')
PLUS = eq('+')
OPEN_BRACKET = eq('(')
CLOSE_BRACKET = eq(')')
DASH = eq('-')
QUOT = eq('"')
# единицы измерения
UNIT = morph_pipeline(['м3', 'м3/сут', 'атм', 'тн'])
# объем
VOLUME = morph_pipeline(['объем'])

# аббревиатура
ABBR = and_(
    length_eq(3),
    is_capitalized()
)
# Стандартный токенизатор. Удаляем правило для переводов строк.
# Обычно токены с '\n' только мешаются.
TOKENIZER = MorphTokenizer().remove_types(EOL)
# IdTokenizer
ID_TOKENIZER = IdTokenizer(TOKENIZER)

VALUE_RULE = rule(or_(DECIMAL, rule(INT)), UNIT)
VALUE_OPT_RULE = rule(or_(DECIMAL, rule(INT)), UNIT.optional())

RBM_RULE = morph_pipeline(['РБМ', 'РБМ-10', 'РБМ 10'])
