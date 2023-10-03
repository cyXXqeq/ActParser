from collections import namedtuple
from os import listdir
from os.path import join as path_join

import pandas as pd
import pdfplumber
from yargy import rule, Parser, or_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import eq

# from yargy.predicates import caseless

from yargy_utils import NUMERO_SIGN, show_json, INT, PREP, show_matches, COLON, EQUAL_SIGN, PERCENT, DOT, COMMA, \
    UNIT, DECIMAL, VOLUME, DASH, OPEN_BRACKET, CLOSE_BRACKET


def show_from_act(my_rule, lines):
    parser = Parser(my_rule)
    matches = list(parser.findall(lines))
    if matches:
        match = matches[0]
        fact = match.fact
        show_json(fact.as_json)


def get_field_value(my_rule, lines, all=False, remainder=False):
    parser = Parser(my_rule)
    result = []

    for line in lines:
        line = line.strip()
        match = list(parser.findall(line))

        if line is not None and len(line) and len(match):
            m_fact = match[0].fact

            if remainder:
                m_fact.value = line.replace(m_fact.field_name, '').strip()

            if all:
                result.append(m_fact)
            else:
                return m_fact

    return result


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
        rule(INT)
    ).interpretation(Well)

    result = get_field_value(WELL, lines, remainder=True)

    return result


def get_injectivity(lines) -> list[fact]:
    """

    :param lines:
    :return: list of injectivity fact
    """

    speed_word = morph_pipeline(['скорость'])
    # unit_word = morph_pipeline(['м3', 'м3/сут', 'атм'])
    # pressure_word = rule(or_(caseless('Р'), caseless('P')))

    Injectivity = fact(
        'Injectivity',
        ['speed', 'field_name', 'value']
    )

    injectivity_rule = rule(
        rule(
            rule(INT),
            rule(speed_word, COLON)
        ).interpretation(Injectivity.field_name),
        # rule(
        #     INT,
        #     unit_word,
        #     PREP,
        #     pressure_word,
        #     EQUAL_SIGN,
        #     INT,
        #     unit_word
        # ).interpretation(Injectivity.value)
    ).interpretation(Injectivity)

    # show_matches(injectivity_rule, lines)

    result = get_field_value(injectivity_rule, lines, all=True, remainder=True)
    for i, res in enumerate(result):
        result[i].speed = res.field_name.split()[0]
        result[i].value = res.value.replace(';', '').replace('.', '')
    return result


def get_process_solution(lines):
    """

    :param lines:
    :return:
    """

    ProcessSolution = fact(
        'ProcessSolution',
        ['value']
    )

    process_solution_rule = rule(
        morph_pipeline(['технологический', 'тех']),
        DOT.optional(),
        morph_pipeline(['раствор']),
        morph_pipeline(['ВДС']).optional(),
        PREP,
        VOLUME,
        rule(INT, UNIT).interpretation(ProcessSolution.value)
    ).interpretation(ProcessSolution)

    # show_matches(process_solution_rule, lines)
    return get_field_value(process_solution_rule, lines)


def get_cycle_count(lines):
    """

    :param lines:
    :return:
    """

    CycleCount = fact(
        'CycleCount',
        ['value']
    )

    cycle_count_rule = rule(
        PREP, rule(INT).interpretation(CycleCount.value), morph_pipeline(['цикл'])
    ).interpretation(CycleCount)

    # show_matches(cycle_count_rule, lines)
    return get_field_value(cycle_count_rule, lines)


def get_clay_powder(lines):
    """

    :param lines:
    :return:
    """

    clay_powder_word = or_(
        morph_pipeline(['ГП']),
        morph_pipeline(['глинопорошок'])
    )

    ClayPowder = fact(
        'ClayPowder',
        ['volume', 'concentration', 'mass']
    )

    clay_powder_rule = rule(
        clay_powder_word,
        DASH.optional(),
        OPEN_BRACKET,
        rule(
            INT, DASH, INT,
            rule(DASH, INT).optional(),
            PERCENT
        ).interpretation(ClayPowder.concentration),
        CLOSE_BRACKET,
        rule(
            DASH,
            rule(DECIMAL, UNIT).interpretation(ClayPowder.mass)
        ).optional()
    ).interpretation(ClayPowder)

    # show_matches(clay_powder_rule, lines)
    return get_field_value(clay_powder_rule, lines)


def get_buffer(lines):
    """

    :param lines:
    :return:
    """

    Buffer = fact(
        'Buffer',
        ['value']
    )

    buffer_rule = rule(
        morph_pipeline(['буфер']),
        rule(
            or_(rule(INT), DECIMAL),
            UNIT
        ).interpretation(Buffer.value)
    ).interpretation(Buffer)

    # show_matches(buffer_rule, lines)
    return get_field_value(buffer_rule, lines)


def get_wood_flour(lines):
    """

    :param lines:
    :return:
    """

    wood_flour_word = or_(
        morph_pipeline(['ДМ']),
        rule(morph_pipeline(['древесный']), morph_pipeline(['мука']))
    )

    WoodFlour = fact(
        'WoodFlour',
        ['volume', 'concentration', 'mass']
    )

    wood_flour_rule = rule(
        wood_flour_word,
        DASH.optional(),
        OPEN_BRACKET,
        rule(
            DECIMAL,
            rule(DASH, DECIMAL).optional(),
            PERCENT
        ).interpretation(WoodFlour.concentration),
        CLOSE_BRACKET,
        rule(
            DASH,
            rule(DECIMAL, UNIT).interpretation(WoodFlour.mass)
        ).optional()
    ).interpretation(WoodFlour)

    # show_matches(wood_flour_rule, lines)
    return get_field_value(wood_flour_rule, lines)


def get_squeeze(lines):
    """

    :param lines:
    :return:
    """

    Squeeze = fact(
        'Squeeze',
        ['value']
    )

    squeeze_rule = rule(
        morph_pipeline(['продавка']),
        rule(PREP, VOLUME).optional(),
        rule(
            or_(rule(INT), DECIMAL), UNIT
        ).interpretation(Squeeze.value)
    ).interpretation(Squeeze)

    # show_matches(squeeze_rule, lines)
    return get_field_value(squeeze_rule, lines)


def get_injection_pressure(lines):
    """

    :param lines:
    :return:
    """

    InjectionPressure = fact(
        'InjectionPressure',
        ['value']
    )
    return InjectionPressure()


def get_squeeze_final(lines):
    """

    :param lines:
    :return:
    """

    SqueezeFinal = fact(
        'SqueezeFinal',
        ['value']
    )

    squeeze_final_rule = rule(
        morph_pipeline(['продавить']),
        rule(
            or_(rule(INT), DECIMAL), UNIT
        ).interpretation(SqueezeFinal.value)
    ).interpretation(SqueezeFinal)

    # show_matches(squeeze_final_rule, lines)
    return get_field_value(squeeze_final_rule, lines)


def get_data_from_pdf(dir_path):
    """

    :param dir_path:
    :return:
    """

    paths = [path_join(dir_path, file) for file in listdir(dir_path)]
    columns = [
        'Скважина',
        'Приемистость скважины на 1-й скорости',
        'Приемистость скважины на 2-й скорости',
        'Приемистость скважины на 3-й скорости',
        'Количество циклов',
        'Объем технонологического раствора',
        'Объем раствора глинопорошка',
        'Концентрация глинопорошка',
        'Масса глинопопрошка',
        'Объем буфера ',
        'Объем раствора древесной муки',
        'Концентрация древесной муки',
        'Масса древесной муки',
        'Объем межцикловой продавки',
        'Давление закачки',
        'Объем финальной продавки',
        'Приемистость скважины на 1-й скорости после закачки',
        'Приемистость скважины на 2-й скорости после закачки',
        'Приемистость скважины на 3-й скорости после закачки',
    ]
    df = pd.DataFrame(columns=columns)
    NoneTuple = namedtuple(
        'NoneTuple',
        ['value', 'volume', 'concentration', 'mass', 'speed', 'field_name']
    )
    none_tuple = NoneTuple(None, None, None, None, None, None)

    # for path in paths:
    #     print('-'*5, path.split('/')[-1], '-'*5, '\n')
    #     pdf = pdfplumber.open(path)
    #     p0 = pdf.pages[0]
    #     text_act_0 = p0.extract_text(
    #         layout=True,
    #         use_text_flow=True
    #     )
    #     p1 = pdf.pages[1]
    #     text_act_1 = p1.extract_text(
    #         layout=True,
    #         use_text_flow=True
    #     )
    #
    #     lines0 = text_act_0.split('\n')
    #     lines1 = text_act_1.split('\n')
    #
    #     print('well number: ', get_well_number(lines0), '\n')
    #
    #     print('injectivity:\n')
    #     injectivity = get_injectivity(lines1)
    #     for inj in injectivity:
    #         print(inj)
    #     print('\n')
    #
    #     print('Объем тех раствора: ', get_process_solution(lines1), '\n')
    #     print('Количество циклов: ', get_cycle_count(lines1), '\n')
    #     print('Объем и концентрация глинопорошка: ', get_clay_powder(lines1), '\n')
    #     print('Объем буфера: ', get_buffer(lines1), '\n')
    #     print('Объем и концентрация глинопорошка: ', get_wood_flour(lines1), '\n')
    #     print('Объем межцикловой продавки: ', get_squeeze(lines1), '\n')
    #     print('Объем итоговой продавки: ', get_squeeze_final(lines1), '\n')
    #     print('Давление закачки: ', 'soon...\n')

    for path in paths:
        pdf = pdfplumber.open(path)
        data_fields = ['well', 'cycle_count', 'process_solution', 'clay_powder',
                       'buffer', 'wood_flour', 'squeeze', 'injection_pressure', 'squeeze_final']
        data = {field: None for field in data_fields}
        data_get_functions = [
            get_well_number,
            get_cycle_count,
            get_process_solution,
            get_clay_powder,
            get_buffer,
            get_wood_flour,
            get_squeeze,
            get_injection_pressure,
            get_squeeze_final,
        ]
        injectivity = []

        for page in pdf.pages:
            text_act = page.extract_text(
                layout=True,
                use_text_flow=True
            )
            lines = text_act.split('\n')

            injectivity += get_injectivity(lines)

            for field, func in zip(data_fields, data_get_functions):
                if not data[field]:
                    data[field] = func(lines)

        for key, value in data.items():
            if not value:
                data[key] = none_tuple

        inj_processed = [1, 2, 3, 1, 2, 3]
        i = 0
        j = 0
        while i < len(inj_processed):
            if int(injectivity[j].speed) == inj_processed[i]:
                inj_processed[i] = injectivity[j].value
                i += 1
                j += 1
            else:
                inj_processed[i] = None
                i += 1

        data_list = [data['well'].value]
        data_list += inj_processed[:3]
        data_list += [
            data['cycle_count'].value,
            data['process_solution'].value,
            data['clay_powder'].volume,
            data['clay_powder'].concentration,
            data['clay_powder'].mass,
            data['buffer'].value,
            data['wood_flour'].volume,
            data['wood_flour'].concentration,
            data['wood_flour'].mass,
            data['squeeze'].value,
            data['injection_pressure'].value,
            data['squeeze_final'].value
        ]
        data_list += inj_processed[3:]

        df.loc[len(df)] = data_list

    df = df.fillna(value='н/д')
    df.to_excel(path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'data_from_pdf.xlsx'))
    return df


if __name__ == '__main__':
    # get_data_from_pdf(path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'test'))
    get_data_from_pdf(path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'ВДС_Размеченные_акты'))
