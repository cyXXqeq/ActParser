import pdfplumber
from yargy import rule, Parser
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

from yargy_utils import NUMERO_SIGN, show_json, INT


def show_from_act(my_rule, lines):
    parser = Parser(my_rule)
    matches = list(parser.findall(lines))
    if matches:
        match = matches[0]
        fact = match.fact
        show_json(fact.as_json)


def get_field_value(my_rule, text):
    parser = Parser(my_rule)
    matches = list(parser.findall(text))
    if matches:
        match = matches[0]
        fact = match.fact
        return fact


def get_field_value_second(my_rule, lines):
    parser = Parser(my_rule)
    for line in lines:
        line = line.strip()
        match = list(parser.findall(line))
        if line is not None and len(line) and len(match):
            fact = match[0].fact
            # fact.value = line.replace(fact.field_name, '').strip()
            # print('fact', fact)
            return fact


def get_well_number(lines) -> int:
    """
    Название поля: Скважина;
    Значение: число;
    Примечание: универсально

    :param lines: Текст, из которого будет извлекаться номер скважины
    :return: номер скважины
    """

    WELL_WORD = morph_pipeline(['Скв'])
    Well = fact(
        'Well',
        ['field_name', 'value']
    )
    WELL = rule(
        rule(WELL_WORD, NUMERO_SIGN).interpretation(Well.field_name),
        rule(INT).interpretation(Well.value)
    ).interpretation(Well)

    result = get_field_value_second(WELL, lines)

    return result


def get_data_from_pdf(path):
    # временная статическая переменная
    path = '/home/cyxxqeq/Data4ActParser/ВДС_Размеченные_акты/AKT_KRS_1255_ДН.pdf'

    pdf = pdfplumber.open(path)
    p0 = pdf.pages[0]
    text_act = p0.extract_text(
        layout=True,
        use_text_flow=True
    )

    print(text_act)

    lines = text_act.split('\n')

    print(get_well_number(lines))


if __name__ == '__main__':
    get_data_from_pdf('')
