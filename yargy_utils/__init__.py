from yargy import or_, rule, and_
from yargy.predicates import gram, eq, length_eq, is_capitalized, type
from yargy.relations import gnc_relation
from yargy.tokenizer import MorphTokenizer, EOL

from yargy_utils.id_tokenizer import IdTokenizer
from yargy_utils.show_result import show_json, show_matches

# для согласования слов
gnc = gnc_relation()
# сущиствительное
NOUN = gram('NOUN')
# полное прилагательное
ADJF = gram('ADJF')
# краткое прилагательное
ADJS = gram('ADJS')

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
FLOAT = rule(INT, or_(COMMA, DOT), INT)
# разделитель в виде союза или знака препинания
SEPARATOR = or_(COMMA, CONJ)
# точка
DOT = eq('.')
# числительное
NUMR = gram('NUMR')
PERCENT = eq('%')
NUMERO_SIGN = eq('№')
SLASH = eq('/')
DECIMAL = rule(INT,
               or_(COMMA, DOT),
               INT)
COLON = eq(':')
EQUAL_SIGN = eq('=')
# аббревиатура
ABBR = and_(
    length_eq(3),
    is_capitalized()
)
# Стандартный токенизатор. Удаляем правило для переводом строк.
# Обычно токены с '\n' только мешаются.
TOKENIZER = MorphTokenizer().remove_types(EOL)
# IdTokenizer
ID_TOKENIZER = IdTokenizer(TOKENIZER)
