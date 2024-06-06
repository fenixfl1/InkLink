import os
import pytest

from config.default import TMP_DIR
from utils.helpers import download_document

url = "https://files.support.epson.com/docid/cpd6/cpd62501.pdf"


async def test_download_document():
    file_path = await download_document(url)
    assert file_path != ""
    assert file_path.startswith(TMP_DIR)
    assert file_path.endswith(".pdf")
    assert os.path.exists(file_path)
    os.remove(file_path)
