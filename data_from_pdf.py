import pdfplumber


def get_borehole_number(text):
    ...


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


if __name__ == '__main__':
    get_data_from_pdf('')
