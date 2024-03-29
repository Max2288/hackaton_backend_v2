import os
from contextlib import contextmanager
from uuid import uuid4

import tempfile
import shutil


@contextmanager
def tmp_image_folder():
    """Генерирует уникальную временную папку, при выходе удаляет папку и ее содержимое."""
    tmp_dir = tempfile.mkdtemp()
    try:
        yield tmp_dir
    finally:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)