from data_from_text import (
    get_well_number,
    get_cycle_count,
    get_process_solution,
    get_clay_powder,
    get_buffer,
    get_wood_flour,
    get_primary_solution,
    get_neftenol_and_waste_water,
    get_hes,
    get_squeeze,
    get_injection_pressure,
    get_squeeze_final,
)

COLUMNS_VDS = [
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
DATA_FIELDS_VDS = [
    'well', 'cycle_count', 'process_solution',
    'clay_powder', 'buffer', 'wood_flour', 'squeeze',
    'injection_pressure', 'squeeze_final'
]
DATA_GET_FUNCTIONS_VDS = [
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
COLUMNS_HES = [
    'Скважина',
    'Приемистость скважины на 1-й скорости',
    'Приемистость скважины на 2-й скорости',
    'Приемистость скважины на 3-й скорости',
    'Объем первичного раствора',
    'Объем нефтенола в первичном растворе',
    'Объем воды в первичном растворе',
    'Объем ГЭР',
    'Концентрация ПАВ в ГЭР',
    'Давление закачки',
    'Объем продавки',
    'Приемистость скважины на 1-й скорости после закачки',
    'Приемистость скважины на 2-й скорости после закачки',
    'Приемистость скважины на 3-й скорости после закачки',
]
DATA_FIELDS_HES = [
    'well', 'primary_solution', 'neftenol_waste_water',
    'hes', 'injection_pressure', 'squeeze_final'
]
DATA_GET_FUNCTIONS_HES = [
    get_well_number,
    get_primary_solution,
    get_neftenol_and_waste_water,
    get_hes,
    get_injection_pressure,
    get_squeeze_final,
]
