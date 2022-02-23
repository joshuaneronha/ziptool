from ziptool import pipeline


def test_get_fips_code_from_abbr():
    assert pipeline.get_fips_code_from_abbr("RI") == "44"
    assert pipeline.get_fips_code_from_abbr("DC") == "11"
    assert pipeline.get_fips_code_from_abbr("AL") == "01"
