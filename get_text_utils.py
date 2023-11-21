import docx


def text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [para.text for para in doc.paragraphs]
    text = '\n'.join(paragraphs)

    return text


if __name__ == '__main__':
    print(text_from_docx('./documents/АЗН/2015_ворд/ARHKRS_OPIS_2893.docx'))
