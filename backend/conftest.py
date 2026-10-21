import tempfile

import pytest


@pytest.fixture(autouse=True)
def use_temp_media_root(settings):
    settings.MEDIA_ROOT = tempfile.mkdtemp()
