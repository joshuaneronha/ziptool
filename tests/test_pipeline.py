from os.path import exists

import pandas as pd
import pkg_resources
import pytest

from ziptool import fetch_data, geo_conversion, shp_dir
from ziptool.query_by_zip import data_by_zip


@pytest.fixture
def test_data() -> pd.DataFrame:
    stream = pkg_resources.resource_stream(__name__, "usa_00013.csv.zip")
    return pd.read_csv(stream, compression = "zip")


def test_zip_to_tract():
    jamestown_test = geo_conversion.zip_to_tract("02835")
    assert jamestown_test[0] == [["44005041300", 1.0]]
    assert jamestown_test[1] == "44"

    pvd_east_test = geo_conversion.zip_to_tract("02906")
    assert pvd_east_test[0] == [
        ["44007003200", 0.120752911150103],
        ["44007003700", 0.0813526878289998],
        ["44007003300", 0.154330834263837],
        ["44007003400", 0.168687190939543],
        ["44007016500", 0.0],
        ["44007003100", 0.0929175307066517],
        ["44007003601", 0.0880523209443292],
        ["44007003602", 0.0837454139416174],
        ["44007003500", 0.210161110224916],
    ]
    assert pvd_east_test[1] == "44"

    ancorage_test = geo_conversion.zip_to_tract("99501")
    assert ancorage_test[0] == [
        ["02020000500", 0.111827733277852],
        ["02020001100", 0.0666805367731197],
        ["02020001000", 0.278477062311453],
        ["02020001200", 0.252678664308748],
        ["02020000400", 0.000208051596796005],
        ["02020000600", 0.00863414126703422],
        ["02020000901", 0.119525642359305],
        ["02020000902", 0.16196816810569],
    ]
    assert ancorage_test[1] == "02"


def test_data_by_zip(test_data):
    test_results = data_by_zip(
        ["02835", "45103"],
        test_data,
        {
            "HHINCOME": {"null": 9999999, "type": "household"},
            "EDUC": {"null": 0, "type": "individual"},
        },
    )

    assert test_results == {
        "02835": {
            "HHINCOME": {"mean": 119942.7, "std": 135934.56, "median": 83000.0},
            "EDUC": {"mean": 7.36, "std": 3.01, "median": 7.0},
        },
        "45103": {
            "HHINCOME": {"mean": 89828.29, "std": 80997.83, "median": 68000.0},
            "EDUC": {"mean": 6.27, "std": 2.75, "median": 6.0},
        },
    }


def test_get_shape_files():
    fetch_data.get_shape_files("44", "2019")
    fetch_data.get_shape_files("01", "2019")
    assert exists(shp_dir.name + "/" + "tl_2019_44_tract.zip")
    assert exists(shp_dir.name + "/" + "tl_2019_44_puma10.zip")
    assert exists(shp_dir.name + "/" + "tl_2019_01_tract.zip")
    assert exists(shp_dir.name + "/" + "tl_2019_01_puma10.zip")
