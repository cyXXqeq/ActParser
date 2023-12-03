import pdfplumber

from utils import text_from_docx
from yargy_utils import RBM_RULE
from yargy_utils.get_value import get_field_value


def split_vds_by_rbm(paths: list[str]):
    rbm = []
    not_rbm = []
    for path in paths:
        text = ''
        match path.split('.')[-1].lower():
            case 'pdf':
                pdf = pdfplumber.open(path)
                for page in pdf.pages:
                    text += page.extract_text(
                        layout=True,
                        use_text_flow=True
                    )
            case 'docx':
                text = text_from_docx
            case other:
                print(f'[INFO] filetype "{other}" not supported')
                continue
        if get_field_value(RBM_RULE, text):
            rbm.append(path)
        else:
            not_rbm.append(path)
    return rbm, not_rbm
