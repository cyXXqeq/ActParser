from collections import namedtuple

import pandas as pd
from yargy import rule, or_
from yargy.interpretation import fact
from yargy.interpretation.fact import Fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import caseless, eq

from utils import text_from_docx, fill_data_list
from utils.get_text import text_from_pdf
from yargy_utils import (
    NUMERO_SIGN, INT, PREP, COLON, EQUAL_SIGN, PERCENT, DOT, UNIT,
    DECIMAL, VOLUME, DASH, OPEN_BRACKET, CLOSE_BRACKET, SLASH, CONJ,
    INTORDEC, PLUS, ANY_LETTER, VALUE_RULE, VALUE_OPT_RULE
)
from yargy_utils.get_value import get_field_value, get_field_value_with_skip

NoneTuple = namedtuple(
    'NoneTuple',
    ['value', 'volume', 'concentration', 'mass', 'speed', 'field_name', 'neftenol', 'waste_water']
)
none_tuple = NoneTuple(None, None, None, None, None, None, None, None)


def get_well_number(text: str):
    """

    :param text: Текст, из которого будет извлекаться номер скважины
    :return: номер скважины
    """

    well_word = morph_pipeline(['Скв'])
    Well = fact(
        'Well',
        ['field_name', 'value']
    )
    well_rule = rule(
        rule(well_word, NUMERO_SIGN).interpretation(Well.field_name),
        rule(INT)
    ).interpretation(Well)
    well_rule_2 = rule(
        well_word,
        DOT.optional(),
        COLON.optional(),
        rule(INT, ANY_LETTER.optional()).interpretation(Well.value)
    ).interpretation(Well)

    result = get_field_value(well_rule, text, remainder=True)

    return result or get_field_value(well_rule_2, text)


def get_injectivity(text: str):
    """

    :param text:
    :return: list of injectivity fact
    """

    speed_word = morph_pipeline(['скорость'])
    pressure_word = rule(or_(caseless('Р'), caseless('P')))

    Injectivity = fact(
        'Injectivity',
        ['speed', 'field_name', 'value']
    )

    injectivity_rule = rule(
        rule(
            rule(INT),
            rule(speed_word, COLON)
        ).interpretation(Injectivity.field_name),
        rule(
            INT,
            UNIT,
            PREP,
            pressure_word,
            EQUAL_SIGN,
            INT,
            UNIT
        ).interpretation(Injectivity.value)
    ).interpretation(Injectivity)

    # result = get_field_value(injectivity_rule, text, all_match=True, remainder=True)
    result = get_field_value(injectivity_rule, text, lines=False, all_match=True)
    for i, res in enumerate(result):
        result[i].speed = res.field_name.split()[0]
        # value = res.value.replace(';', '').replace('.', '').replace('приемистость:', '').replace('(сid:9)', '')
        # value = ' '.join(value.split())
        # result[i].value = value
    return result


def get_process_solution(text: str):
    """

    :param text:
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
        VALUE_RULE.interpretation(ProcessSolution.value)
    ).interpretation(ProcessSolution)

    return get_field_value(process_solution_rule, text)


def get_cycle_count(text: str):
    """

    :param text:
    :return:
    """

    CycleCount = fact(
        'CycleCount',
        ['value']
    )

    cycle_count_rule = rule(
        PREP, rule(INT).interpretation(CycleCount.value), morph_pipeline(['цикл'])
    ).interpretation(CycleCount)

    return get_field_value(cycle_count_rule, text)


def get_clay_powder(text: str):
    """

    :param text:
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

    clay_powder_rule_2_1 = rule(
        clay_powder_word,
        PREP,
        caseless('V'),
        EQUAL_SIGN,
        rule(INT, UNIT).interpretation(ClayPowder.volume)
    )

    clay_powder_rule_2_2 = rule(
        morph_pipeline(['концентрация']),
        rule(
            INT, DASH, INT, rule(DASH, INT).optional(), PERCENT
        ).interpretation(ClayPowder.concentration)
    )

    clay_powder_rule_2 = or_(
        clay_powder_rule_2_1,
        clay_powder_rule_2_2
    )

    weird_volume_rule = rule(INT, eq('ц'), PREP, VALUE_RULE)

    clay_powder_rule_3 = rule(
        clay_powder_word,
        OPEN_BRACKET,
        rule(
            weird_volume_rule,
            rule(PLUS, weird_volume_rule).optional()
        ).interpretation(ClayPowder.volume),
        CLOSE_BRACKET
    ).interpretation(ClayPowder)

    value = get_field_value(clay_powder_rule, text)

    if value:
        return value

    value = get_field_value(clay_powder_rule_3, text)

    if value:
        return value

    value = get_field_value_with_skip(clay_powder_rule_2, text)

    if value:
        result = ''

        for s in value:
            result += s + ' '

        return get_field_value(
            rule(
                clay_powder_rule_2_1,
                clay_powder_rule_2_2
            ).interpretation(ClayPowder),
            result
        )


def get_buffer(text: str):
    """

    :param text:
    :return:
    """

    Buffer = fact(
        'Buffer',
        ['value']
    )

    buffer_word = morph_pipeline(['буфер'])

    buffer_rule = rule(
        buffer_word,
        DASH.optional(),
        VALUE_RULE.interpretation(Buffer.value)
    ).interpretation(Buffer)

    buffer_rule_2 = rule(
        morph_pipeline(['смена']),
        morph_pipeline(['закачка']),
        morph_pipeline(['химреагенты']).optional(),
        morph_pipeline(['продавка']),
        morph_pipeline(['составить']).optional(),
        VALUE_RULE.interpretation(Buffer.value)
    ).interpretation(Buffer)

    buffer_rule_3 = rule(
        caseless('V'),
        EQUAL_SIGN,
        or_(rule(INT), DECIMAL).interpretation(Buffer.value)
    )

    value = get_field_value(buffer_rule, text)

    if value:
        return value

    value = get_field_value(buffer_rule_2, text)

    if value:
        return value

    value = get_field_value_with_skip(
        or_(buffer_word, buffer_rule_3),
        text
    )

    if value:
        result = ' '.join(value)

        return get_field_value(
            rule(
                buffer_word,
                buffer_rule_3
            ).interpretation(Buffer),
            result
        )


def get_wood_flour(text: str):
    """

    :param text:
    :return:
    """

    wood_flour_word = or_(
        morph_pipeline(['ДМ']),
        rule(
            morph_pipeline(['древесная']),
            rule(CONJ, morph_pipeline(['доломитовый'])).optional(),
            morph_pipeline(['мука'])
        )
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
            rule(DASH, DECIMAL).optional(),
            PERCENT
        ).interpretation(WoodFlour.concentration),
        CLOSE_BRACKET,
        rule(
            DASH,
            rule(
                DECIMAL,
                rule(PLUS, DECIMAL).optional(),
                UNIT
            ).interpretation(WoodFlour.mass)
        ).optional()
    ).interpretation(WoodFlour)

    wood_flour_rule_2_1 = rule(
        wood_flour_word,
        PREP,
        caseless('V'),
        EQUAL_SIGN,
        rule(INT, UNIT).interpretation(WoodFlour.volume)
    )

    wood_flour_rule_2_2 = rule(
        morph_pipeline(['концентрация']),
        rule(
            DECIMAL, DASH, DECIMAL, rule(DASH, DECIMAL).optional(), PERCENT
        ).interpretation(WoodFlour.concentration)
    )

    wood_flour_rule_2 = or_(
        wood_flour_rule_2_1,
        wood_flour_rule_2_2
    )

    weird_volume_rule = rule(INT, eq('ц'), PREP, VALUE_RULE)

    wood_flour_rule_3 = rule(
        wood_flour_word,
        OPEN_BRACKET,
        rule(
            weird_volume_rule,
            rule(PLUS, weird_volume_rule).optional()
        ).interpretation(WoodFlour.volume),
        CLOSE_BRACKET
    ).interpretation(WoodFlour)

    result = (
            get_field_value(wood_flour_rule, text, lines=False)
            or get_field_value(wood_flour_rule_3, text, lines=False)
    )
    if result:
        return result

    value = get_field_value_with_skip(wood_flour_rule_2, text)

    if value:
        result = ''

        for s in value:
            result += s + ' '

        return get_field_value(
            rule(
                wood_flour_rule_2_1,
                wood_flour_rule_2_2
            ).interpretation(WoodFlour),
            result
        )


def get_primary_solution(text: str):
    PrimarySolution = fact(
        'PrimarySolution',
        ['value']
    )

    primary_solution_rule = rule(
        morph_pipeline(['первичный']),
        morph_pipeline(['раствор']),
        rule(PREP, morph_pipeline(['объем'])).optional(),
        VALUE_RULE.interpretation(PrimarySolution.value)
    ).interpretation(PrimarySolution)

    return get_field_value(primary_solution_rule, text)


def get_neftenol_and_waste_water(text: str):
    NeftenolWasteWater = fact(
        'NeftenolWasteWater',
        ['neftenol', 'waste_water']
    )

    solution_rule = rule(
        morph_pipeline(['первичный']),
        morph_pipeline(['раствор'])
    )

    neftenol_rule = rule(
        OPEN_BRACKET.optional(),
        morph_pipeline(['Нефтенол'])
    )

    waste_water_rule = rule(
        OPEN_BRACKET.optional(),
        or_(
            rule(
                morph_pipeline(['сточный', 'сточн', 'сточ', 'пресный', 'пресн', 'соль']),
                DOT.optional(),
                SLASH.optional(),
                morph_pipeline(['вода'])
            ),
            rule(
                morph_pipeline(['облагороженный', 'обл']).optional(),
                DOT.optional(),
                morph_pipeline(['тех', 'технологический']),
                DOT.optional(),
                morph_pipeline(['жидкость'])
            ),
            rule(
                morph_pipeline(['сольводы'])
            )
        )
    )

    neftenol_waste_water_rule = or_(
        solution_rule,
        rule(
            VALUE_OPT_RULE,
            or_(neftenol_rule, waste_water_rule)
        )
    )

    neftenol_waste_water_rule_2 = rule(
        morph_pipeline(['первичный']),
        morph_pipeline(['раствор']),
        VALUE_OPT_RULE.interpretation(NeftenolWasteWater.neftenol),
        neftenol_rule,
        VALUE_OPT_RULE.interpretation(NeftenolWasteWater.waste_water),
        waste_water_rule
    ).interpretation(NeftenolWasteWater)

    extract_text = get_field_value_with_skip(
        neftenol_waste_water_rule,
        text,
        lines=False,
        first_value=False
    )

    return get_field_value(neftenol_waste_water_rule_2, extract_text)


def get_hes(text: str):
    Hes = fact(
        'Hes',
        ['volume', 'concentration']
    )

    conc_rule = rule(
        INTORDEC,
        PERCENT
    )

    hes_rule_1 = rule(
        morph_pipeline(['ГЭР']),
        conc_rule.interpretation(Hes.concentration).optional(),
        PREP,
        morph_pipeline(['объем']),
        VALUE_RULE.interpretation(Hes.volume),
        rule(
            OPEN_BRACKET,
            or_(
                conc_rule.interpretation(Hes.concentration),
                rule(
                    INTORDEC, DASH, INTORDEC, PERCENT
                ).interpretation(Hes.concentration)
            ),
            CLOSE_BRACKET
        ).optional()
    ).interpretation(Hes)

    hes_rule_2 = rule(
        morph_pipeline(['аналогично']),
        PREP,
        VALUE_RULE.interpretation(Hes.volume),
        CONJ,
        morph_pipeline(['закачать']),
        conc_rule.interpretation(Hes.concentration),
        morph_pipeline(['гидрофобный']),
        morph_pipeline(['эмульсия'])
    ).interpretation(Hes)

    hes_rule_3 = rule(
        conc_rule.interpretation(Hes.concentration).optional(),
        morph_pipeline(['гидрофобный']),
        morph_pipeline(['эмульсия']),
        conc_rule.interpretation(Hes.concentration).optional(),
        PREP,
        morph_pipeline(['объем']),
        VALUE_RULE.interpretation(Hes.volume),
        or_(
            rule(
                PREP,
                morph_pipeline(['концентрация']),
                morph_pipeline(['НЗ-ТАТ']).optional(),
                conc_rule.interpretation(Hes.concentration)
            ),
            rule(
                OPEN_BRACKET,
                conc_rule.interpretation(Hes.concentration),
                CLOSE_BRACKET
            )
        ).optional()
    ).interpretation(Hes)

    hes_rule_4 = rule(
        VALUE_RULE.interpretation(Hes.volume),
        morph_pipeline(['гидрофобная']),
        morph_pipeline(['эмульсия']),
        PREP,
        morph_pipeline(['концентрация']),
        conc_rule.interpretation(Hes.concentration)
    ).interpretation(Hes)

    return (get_field_value(hes_rule_1, text, lines=False)
            or get_field_value(hes_rule_2, text, lines=False)
            or get_field_value(hes_rule_3, text, lines=False)
            or get_field_value(hes_rule_4, text, lines=False))


def get_squeeze(text: str):
    """

    :param text:
    :return:
    """

    Squeeze = fact(
        'Squeeze',
        ['value']
    )

    squeeze_word = morph_pipeline(['продавка'])

    squeeze_rule = rule(
        squeeze_word,
        rule(PREP, VOLUME).optional(),
        DASH.optional(),
        VALUE_RULE.interpretation(Squeeze.value)
    ).interpretation(Squeeze)

    squeeze_rule_2 = rule(
        caseless('V'),
        EQUAL_SIGN,
        or_(rule(INT), DECIMAL).interpretation(Squeeze.value)
    )

    result = get_field_value(squeeze_rule, text)

    if result:
        return result

    value = get_field_value_with_skip(
        or_(squeeze_word, squeeze_rule_2),
        text,
        lines=False
    )

    if value:
        result = ''.join(value)

        return get_field_value(
            rule(
                squeeze_word,
                squeeze_rule_2
            ).interpretation(Squeeze),
            result
        )


def get_injection_pressure(text: str):
    """

    :param text:
    :return:
    """

    InjectionPressure = fact(
        'InjectionPressure',
        ['value']
    )

    injection_pressure_rule = rule(
        morph_pipeline(['Pзак', 'Рзак']),
        EQUAL_SIGN,
        rule(
            INT, DASH, INT, rule(DASH, INT).optional(), UNIT
        ).interpretation(InjectionPressure.value)
    ).interpretation(InjectionPressure)

    return (get_field_value(injection_pressure_rule, text)
            or get_field_value(injection_pressure_rule, text, lines=False))


def get_squeeze_final(text: str):
    """

    :param text:
    :return:
    """

    squeeze_word = morph_pipeline(['продавить'])

    SqueezeFinal = fact(
        'SqueezeFinal',
        ['value']
    )

    squeeze_final_rule = rule(
        squeeze_word,
        VALUE_RULE.interpretation(SqueezeFinal.value)
    ).interpretation(SqueezeFinal)

    result = get_field_value(squeeze_final_rule, text)

    if result:
        return result

    squeeze_final_rule_2_1 = rule(
        PREP,
        morph_pipeline(['объем']),
        VALUE_RULE.interpretation(SqueezeFinal.value)
    )

    squeeze_final_rule_2 = or_(
        squeeze_word,
        squeeze_final_rule_2_1
    ).interpretation(SqueezeFinal)

    squeeze_final_rule_3 = rule(
        squeeze_word,
        squeeze_final_rule_2_1
    ).interpretation(SqueezeFinal)

    extract_text = get_field_value_with_skip(
        squeeze_final_rule_2,
        text,
        lines=True,
        first_value=False
    )

    if not extract_text:
        return result

    return get_field_value(
        squeeze_final_rule_3,
        extract_text
    )


def extract_data_from_text(text_act, data_fields, data_get_functions, data, injectivity):
    text_act = text_act.replace('c', 'с').replace('o', 'о')
    injectivity += get_injectivity(text_act)

    for field, func in zip(data_fields, data_get_functions):
        if not data[field]:
            data[field] = func(text_act)


def get_data_from_text(
        paths: list[str],
        columns: list[str],
        data_fields: list[str],
        data_get_functions: list,
        act_kind: str,
        log: bool = False,
) -> pd.DataFrame:
    """

    :param paths: список путей к документам
    :param columns: столбцы конкретного типа акта
    :param data_fields: ключи столбцов в словаре
    :param data_get_functions: функции для получения информации из текста
    :param act_kind: VDS or HES
    :param log: output log if true
    :return:
    """

    df = pd.DataFrame(columns=columns)

    for path in paths:

        if log:
            print(f'[INFO] path: {path}')

        data: dict[str, None | NoneTuple | Fact] = {field: None for field in data_fields}
        injectivity = []

        match path.split('.')[-1].lower():
            case 'docx':
                text_act = text_from_docx(path)
            case 'pdf':
                text_act = text_from_pdf(path)
            case other:
                if log:
                    print(f'[INFO] filetype "{other}" not supported')
                continue

        extract_data_from_text(text_act, data_fields, data_get_functions, data, injectivity)

        for key, value in data.items():
            if not value:
                data[key] = none_tuple

        inj_processed: list[int | None] = [1, 2, 3, 1, 2, 3]
        i = 0
        j = 0
        while i < len(inj_processed):
            if j >= len(injectivity):
                inj_processed[i] = None
                i += 1
            elif int(injectivity[j].speed) == inj_processed[i]:
                inj_processed[i] = injectivity[j].value
                i += 1
                j += 1
            else:
                inj_processed[i] = None
                i += 1

        data_list = fill_data_list(data, inj_processed, act_kind)

        df.loc[len(df)] = data_list

    df = df.fillna(value='н/д')

    return df