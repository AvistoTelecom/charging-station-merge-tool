from chargingstationmergedtool.utils import extract_power_rated

def test_extract_power_rated():
    assert(extract_power_rated("22 KW")) == 22.0
    assert(extract_power_rated("22KW")) == 22.0
    assert(extract_power_rated("3.6 kw")) == 3.6
    assert(extract_power_rated("3,6 kw")) == 3.6

    assert(extract_power_rated("kw")) == None
    assert(extract_power_rated("")) == None