from sys import path
import pytest

path.append('.')

from cs.quality import Quality

def test_get_status_name_bad():
    quality = Quality("mock")

    expected = 'bad'
    result = quality.get_status_name(-1)

    assert expected == result

def test_get_status_name_acceptable():
    quality = Quality("mock")

    expected = 'acceptable'
    result = quality.get_status_name(0)

    assert expected == result

def test_get_status_name_great():
    quality = Quality("mock")

    expected = 'great'
    result = quality.get_status_name(1)

    assert expected == result
