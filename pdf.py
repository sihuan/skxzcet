import tempfile
import zipfile
from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import requests


def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")
    return lines


def content_to_tmp_file(content):
    tmp = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    tmp.write(content)
    return tmp


def zip_files(tmp_file):
    zip_object = zipfile.ZipFile(tmp_file.name)
    pdf_file = zip_object.open(zip_object.namelist()[0])
    tmp_file.close()
    return pdf_file


def parse_number_from_content(content):
    pdf = zip_files(content_to_tmp_file(content))
    result = read_pdf(pdf)
    exam_name = result[0]
    number = result[6].replace("准考证号：", "")
    school = result[12].replace("所属学校：", "")
    return exam_name, school, number


if __name__ == '__main__':
    session = requests.Session()
    req = session.get("http://cet-bm.neea.edu.cn/Home/DownTestTicket?SID=6099C2BE25DF2B1E847811B7DB32008A1A0C6044A730D86D7B0CE19B3C7E776493CFE74E75D11F2E04D4A30D8B90A0D489273D0009BE2D8F43FD3BD4267AE522")
    exam, school, number = parse_number_from_content(req.content)
    print(exam, school, number)
