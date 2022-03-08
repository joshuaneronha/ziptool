from ctypes import util

from ziptool import utils


def test_cast_fips_code():
    assert utils.cast_fips_code(11) == "11"
    assert utils.cast_fips_code("11") == "11"

    assert utils.cast_fips_code(1) == "01"
    assert utils.cast_fips_code("01") == "01"


def test_cast_zipcode():
    assert utils.cast_zipcode("01234") == "01234"
    assert utils.cast_zipcode(2912) == "02912"


def test_get_fips_code_from_abbr():
    assert utils.get_fips_code_from_abbr("RI") == "44"
    assert utils.get_fips_code_from_abbr("DC") == "11"
    assert utils.get_fips_code_from_abbr("AL") == "01"
