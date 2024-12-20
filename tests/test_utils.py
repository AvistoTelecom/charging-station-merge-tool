from src.utils import extract_power_rated, is_power_rated_data, is_int_data, compare_hash, write_hash_file
import os
import pytest

def test_extract_power_rated():
    assert(extract_power_rated("22 KW")) == 22.0
    assert(extract_power_rated("22KW")) == 22.0
    assert(extract_power_rated("3.6 kw")) == 3.6
    assert(extract_power_rated("3,6 kw")) == 3.6

    assert(extract_power_rated("kw")) is None
    assert(extract_power_rated("")) is None

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

def test_compare_hash():
    assert(compare_hash("tests/resources/test.hash", "tests/resources/data_gouv_page.html"))
    assert(not compare_hash("tests/resources/test_compare_hash.hash", "tests/resources/data_gouv_page.html"))
    assert(not compare_hash("tests/resources/test.hash", "tests/resources/gouv_page.html"))
    assert(not compare_hash("tests/resources/test_wrong.hash", "tests/resources/data_gouv_page.html"))

def test_write_hash_file():
    
    write_hash_file("tests/resources/test2.hash", "tests/resources/data_gouv_page.html")

    assert(os.path.exists("tests/resources/test2.hash"))
    
    with open("tests/resources/test2.hash", 'r') as f_to_test:
        with open("tests/resources/test.hash", 'r') as f_expected:
            assert(f_to_test.read() == f_expected.read())

    os.remove("tests/resources/test2.hash")

    with pytest.raises(FileNotFoundError):
        write_hash_file("tests/resources/test2.hash", "tests/resources/data_gouv_pag.html")