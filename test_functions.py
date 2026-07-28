from functions import pars_years
import pytest

@pytest.mark.parametrize(["wejscie", "oczekiwany"], [
    ("",""),
    ("  ",""),
    ("2015-2020","2015 - 2020"),
    ("2005 - 2010","2005 - 2010"),
    ("2006-obecnie","2006 - Obecnie"),
    ("1999 - obecnienienie","1999 - Obecnie"),
    ("2020-Obecnie","2020 - Obecnie"),
    ("2022 -oBeci","2022 - Obecnie"),
    ("obecnie","Obecnie"),
    ("2020","2020"),
    ("kot - pies","")
])

def test_pars_years(wejscie,oczekiwany):
    assert pars_years(wejscie) == oczekiwany