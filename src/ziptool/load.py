import tempfile
import json
import shutil
import urllib
from functools import lru_cache
import os
from os.path import exists
from pathlib import Path
from typing import Dict, List, Union
import pkg_resources
import tempfile

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import us
import wquantiles

pd.options.mode.chained_assignment = None

from ziptool import shp_dir

def load_crosswalk():
    stream = pkg_resources.resource_stream(__name__, 'resources/ZIP_TRACT_122021.XLSX')
    return pd.read_excel(stream)

def load_test_data():
    stream = pkg_resources.resource_stream(__name__, 'resources/usa_00013.csv')
    return pd.read_csv(stream)
