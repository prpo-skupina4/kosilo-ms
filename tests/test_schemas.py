import pytest
from datetime import time
from schemas import PostKosilo, Predmet, Aktivnost, Termin


def test_post_kosilo_creation():
    """Test PostKosilo schema creation"""
    data = {
        "uporabnik_id": 1,
        "dan": 3,
        "udelezenci": [1, 2, 3]
    }
    kosilo = PostKosilo(**data)
    assert kosilo.uporabnik_id == 1
    assert kosilo.dan == 3
    assert kosilo.udelezenci == [1, 2, 3]


def test_predmet_creation():
    """Test Predmet schema creation"""
    predmet = Predmet(predmet_id=1, oznaka="MAT", ime="Matematika")
    assert predmet.predmet_id == 1
    assert predmet.oznaka == "MAT"
    assert predmet.ime == "Matematika"


def test_aktivnost_creation():
    """Test Aktivnost schema creation"""
    aktivnost = Aktivnost(aktivnost_id=1, oznaka="KOS", ime="Kosilo")
    assert aktivnost.aktivnost_id == 1
    assert aktivnost.oznaka == "KOS"
    assert aktivnost.ime == "Kosilo"


def test_aktivnost_optional_id():
    """Test Aktivnost schema with optional aktivnost_id"""
    aktivnost = Aktivnost(oznaka="KOS", ime="Kosilo")
    assert aktivnost.aktivnost_id is None
    assert aktivnost.oznaka == "KOS"
    assert aktivnost.ime == "Kosilo"


def test_termin_creation():
    """Test Termin schema creation"""
    termin = Termin(
        termin_id=1,
        zacetek=time(12, 0),
        dolzina=30,
        dan=3,
        lokacija="Menza",
        tip="kosilo"
    )
    assert termin.termin_id == 1
    assert termin.zacetek == time(12, 0)
    assert termin.dolzina == 30
    assert termin.dan == 3
    assert termin.lokacija == "Menza"
    assert termin.tip == "kosilo"
    assert termin.predmet is None
    assert termin.aktivnost is None


def test_termin_with_aktivnost():
    """Test Termin schema with Aktivnost"""
    aktivnost = Aktivnost(aktivnost_id=1, oznaka="KOS", ime="Kosilo")
    termin = Termin(
        termin_id=1,
        zacetek=time(12, 0),
        dolzina=30,
        dan=3,
        lokacija="Menza",
        tip="kosilo",
        aktivnost=aktivnost
    )
    assert termin.aktivnost.oznaka == "KOS"
    assert termin.aktivnost.ime == "Kosilo"
