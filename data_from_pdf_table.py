from pdf2docx import Converter


def get_data_from_pdf_table(path):
    # временая статическая переменная
    path = '/home/cyxxqeq/Data4ActParser/ВДС_Размеченные_акты/AKT_KRS_1255_ДН.pdf'

    cv = Converter(path)
    tables = cv.extract_tables()
    cv.close()
    return tables


if __name__ == '__main__':
    tables = get_data_from_pdf_table('')
    for table in tables:
        for row in table:
            print(row)
        print('\n\n')
