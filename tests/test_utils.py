from chargingstationmergedtool.utils import extract_power_rated, is_power_rated_data, is_int_data

def test_extract_power_rated():
    assert(extract_power_rated("22 KW")) == 22.0
    assert(extract_power_rated("22KW")) == 22.0
    assert(extract_power_rated("3.6 kw")) == 3.6
    assert(extract_power_rated("3,6 kw")) == 3.6

    assert(extract_power_rated("kw")) == None
    assert(extract_power_rated("")) == None

def test_is_power_rated_data():
    assert(is_power_rated_data("22 KW"))
    assert(is_power_rated_data("22KW"))
    assert(is_power_rated_data("3.6 kw"))
    assert(is_power_rated_data("3,6 kw"))

    assert(not is_power_rated_data("kw"))
    assert(not is_power_rated_data(""))

def test_is_int_data():
    assert(is_int_data("22"))
    assert(not is_int_data("test"))