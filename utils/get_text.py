import docx
import pdfplumber


def text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [para.text for para in doc.paragraphs]
    text = '\n'.join(paragraphs)

    return text


def text_from_pdf(path: str) -> str:
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text(
                layout=False,
                use_text_flow=True
            )
    return text


if __name__ == '__main__':
    # print(text_from_docx('../documents/АЗН/2015_ворд/ARHKRS_OPIS_2893.docx'))
    print(text_from_pdf('../documents/single_test/AKT_KRS_2831_АЗН2.PDF'))
