from ziptool import pipeline
from os.path import exists


def test_get_fips_code_from_abbr():
    assert pipeline.get_fips_code_from_abbr("RI") == "44"
    assert pipeline.get_fips_code_from_abbr("DC") == "11"
    assert pipeline.get_fips_code_from_abbr("AL") == "01"

def test_zip_to_tract():
    jamestown_test = pipeline.zip_to_tract('02835')
    assert jamestown_test[0] == [[44005041300, 1.0]]
    assert jamestown_test[1] == '44'

    pvd_east_test = pipeline.zip_to_tract('02906')
    assert pvd_east_test[0] == [[44007003200.0, 0.120752911150103],
                             [44007003700.0, 0.0813526878289998],
                             [44007003300.0, 0.154330834263837],
                             [44007003400.0, 0.168687190939543],
                             [44007016500.0, 0.0],
                             [44007003100.0, 0.0929175307066517],
                             [44007003601.0, 0.0880523209443292],
                             [44007003602.0, 0.0837454139416174],
                             [44007003500.0, 0.210161110224916]]
    assert pvd_east_test[1] == '44'

    ancorage_test = pipeline.zip_to_tract('99501')
    assert ancorage_test[0] == [[2020000500.0, 0.111827733277852],
                                 [2020001100.0, 0.0666805367731197],
                                 [2020001000.0, 0.278477062311453],
                                 [2020001200.0, 0.252678664308748],
                                 [2020000400.0, 0.000208051596796005],
                                 [2020000600.0, 0.00863414126703422],
                                 [2020000901.0, 0.119525642359305],
                                 [2020000902.0, 0.16196816810569]]
    assert ancorage_test[1] == '02'

def test_data_by_zip():
    test_data = pipeline.load_test_data()
    test_results = pipeline.data_by_zip(['02835', '45103'],test_data, {"HHINCOME": {"null": 9999999, "type": 'household'}, "EDUC": {"null": 0, "type": 'individual'}})

    assert test_results == {'02835': {"HHINCOME": {'mean': 119942.7, 'std': 135934.56, 'median' : 83000.0}, "EDUC": {'mean': 7.36, 'std': 3.01, 'median': 7.0}}, '45103': {"HHINCOME": {'mean': 89828.29, 'std': 80997.83, 'median': 68000.0}, "EDUC": {'mean': 6.27, 'std': 2.75, 'median': 6.0}}}

def test_get_shape_files():
    pipeline.get_shape_files('44')
    pipeline.get_shape_files('01')
    assert exists("tl_2019_44_tract.zip")
    assert exists("tl_2019_44_puma10.zip")
    assert exists("tl_2019_01_tract.zip")
    assert exists("tl_2019_01_puma10.zip")
