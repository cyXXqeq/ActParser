from pandas import DataFrame
from pdf2docx import Converter


def get_resource_consumption(tables) -> DataFrame:
    for i, table in enumerate(tables):
        if {'Материал (реагент)', 'Количество'}.issubset(table[0]):
            df = DataFrame(table[1:], columns=table[0])
            df = df.loc[:, ['Материал (реагент)', 'Плотно сть г/см3', 'Количество']]
            df = df.replace([''], 'н/д')
            df = df.fillna(value='н/д')

            return df


def get_data_from_pdf_table(path):
    # временая статическая переменная
    path = '/home/cyxxqeq/Data4ActParser/ВДС_Размеченные_акты/AKT_KRS_5702_АН.pdf'

    cv = Converter(path)
    tables = cv.extract_tables()
    cv.close()

    get_resource_consumption(tables)

    return tables


if __name__ == '__main__':
    temp_tables = get_data_from_pdf_table('')
    # for temp_table in temp_tables:
    #     for row in temp_table:
    #         print(row)
    #     print('\n\n')
