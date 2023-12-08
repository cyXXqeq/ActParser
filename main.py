import argparse
import logging
import os

from data_to_table import data_to_excel


def files_is_docx(dir_path):
    files = os.listdir(dir_path)
    file_extensions = ''
    for file in files:
        if not file_extensions:
            file_extensions = file.lower().split('.')[-1]
        if not file.lower().endswith(file_extensions):
            raise AttributeError('Files in directory must be only pdf or only docx')
    return file_extensions == 'docx'


def main():
    parser = argparse.ArgumentParser(
        description='Парсер актов, берет информацию из документов '
                    'расположенных в папке и заполняет таблицу. '
                    'Поддерживает ВДС, ВДС РБМ и ГЭР акты.'
                    'В одной папке с актамы должны быть файлы только pdf или docx, '
                    'если в одной папке будут и pdf и docx файлы, программа '
                    'отработает некорректно'
    )

    parser.add_argument('input_dir', help='Путь к папке с актами')
    parser.add_argument('output_table', help='Путь к итоговой таблице')
    parser.add_argument('document_type', help='Тип документа: VDS для ВДС и HES для ГЭР, '
                                              'с другими параметрами работать не будет')
    parser.add_argument('--enable_logs', action='store_true', help='Включить логи')

    args = parser.parse_args()
    args.document_type = args.document_type.upper()
    is_docx = files_is_docx(args.input_dir)
    if not args.output_table.lower().endswith('.xlsx'):
        args.output_table += '.xlsx'
    if args.enable_logs:
        logging.disable(logging.NOTSET)
    data_to_excel(args.input_dir, args.output_table, args.document_type, args.enable_logs, is_docx)


if __name__ == '__main__':
    main()
