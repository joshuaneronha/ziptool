import tempfile

global shp_dir
shp_dir = tempfile.TemporaryDirectory()

from ziptool import data_by_zip
