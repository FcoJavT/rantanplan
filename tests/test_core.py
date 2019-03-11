import spacy

from skas.core import get_orthographic_accent
from skas.core import get_scansion
from skas.core import get_syllables
from skas.core import get_word_stress
from skas.core import have_prosodic_liason
from skas.core import hyphenate
from skas.core import is_paroxytone
from skas.core import spacy_tag_to_dict

nlp = spacy.load('es')


def test_have_prosodic_liason():
    first_syllable = {'syllable': 'ca', 'is_stressed': True}
    second_syllable = {'syllable': 'en', 'is_stressed': False}
    assert have_prosodic_liason(first_syllable, second_syllable) is True


def test_hyphenate():
    word = "platanero"
    output = ['pla', 'ta', 'ne', 'ro']
    assert hyphenate(word) == output


def test_get_orthographic_accent():
    syllable_list = ['plá', 'ta', 'no']
    output = 0
    assert get_orthographic_accent(syllable_list) == output


def test_get_orthographic_accent_with_no_tilde():
    syllable_list = ['pla', 'ta', 'ne', 'ro']
    assert get_orthographic_accent(syllable_list) is None


def test_is_paroxytone():
    syllable_list = ['pla', 'ta', 'ne', 'ro']
    assert is_paroxytone(syllable_list) is True


def test_is_paroxytone_with_tilde():
    syllable_list = ['cés', 'ped']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_proparoxytone():
    syllable_list = ['es', 'drú', 'ju', 'la']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_oxytone_with_tilde():
    syllable_list = ['a', 'com', 'pa', 'ñó']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_oxytone_no_tilde():
    syllable_list = ['tam', 'bor']
    assert is_paroxytone(syllable_list) is False


def test_get_word_stress():
    word = "plátano"
    pos = "NOUN"
    tag = {'Gender': 'Masc', 'Number': 'Sing'}
    output = {'syllables': [{'syllable': 'plá', 'is_stressed': True},
                            {'syllable': 'ta', 'is_stressed': False},
                            {'syllable': 'no', 'is_stressed': False}],
              'stress_position': -3}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_stressed_monosyllables_without_tilde():
    word = "yo"
    pos = "PRON"
    tag = {'Case': 'Nom', 'Number': 'Sing', 'Person': '1', 'PronType': 'Prs'}
    output = {'syllables': [{'syllable': 'yo', 'is_stressed': True}],
              'stress_position': -1}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_unstressed_monosyllables_without_tilde():
    word = "mi"
    pos = "DET"
    tag = {'Number': 'Sing', 'Number[psor]': 'Sing', 'Person': '1', 'Poss': 'Yes', 'PronType': 'Prs'}
    output = {'syllables': [{'syllable': 'mi', 'is_stressed': False}],
              'stress_position': 0}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_no_tilde():
    word = "campo"
    pos = "NOUN"
    tag = {'Gender': 'Masc', 'Number': 'Sing'}
    output = {'syllables': [{'syllable': 'cam', 'is_stressed': True},
                            {'syllable': 'po', 'is_stressed': False}],
              'stress_position': -2}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_oxytone():
    word = "tambor"
    pos = "NOUN"
    tag = {'Gender': 'Fem', 'Number': 'Sing'}
    output = {'syllables': [{'syllable': 'tam', 'is_stressed': False},
                            {'syllable': 'bor', 'is_stressed': True}],
              'stress_position': -1}
    assert get_word_stress(word, pos, tag) == output


def test_get_syllables():
    word = nlp('físico-químico')
    output = [{'syllables': [{'syllable': 'fí', 'is_stressed': True},
                             {'syllable': 'si', 'is_stressed': False},
                             {'syllable': 'co', 'is_stressed': False}],
               'stress_position': -3},
              {'symbol': '-'},
              {'syllables': [{'syllable': 'quí', 'is_stressed': True},
                             {'syllable': 'mi', 'is_stressed': False},
                             {'syllable': 'co', 'is_stressed': False}],
               'stress_position': -3}]
    assert get_syllables(word) == output


def test_get_scansion():
    text = """Siempre en octubre comenzaba el año.
    ¡Y cuántas veces esa luz de otoño
    me recordó a Fray Luis:
    «Ya el tiempo nos convida
    A los estudios nobles...»!"""
    output = [{'tokens': [{'syllables': [{'syllable': 'Siem', 'is_stressed': True},
                                         {'syllable': 'pre', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'en', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'oc', 'is_stressed': False},
                                         {'syllable': 'tu', 'is_stressed': True},
                                         {'syllable': 'bre', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'co', 'is_stressed': False},
                                         {'syllable': 'men', 'is_stressed': False},
                                         {'syllable': 'za', 'is_stressed': True},
                                         {'syllable': 'ba', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'el', 'is_stressed': False}],
                           'stress_position': 0},
                          {'syllables': [{'syllable': 'a', 'is_stressed': True},
                                         {'syllable': 'ño', 'is_stressed': False}],
                           'stress_position': -2},
                          {'symbol': '.'}]},
              {'tokens': [{'symbol': '¡'},
                          {'syllables': [{'syllable': 'Y', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'cuán', 'is_stressed': True},
                                         {'syllable': 'tas', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 've', 'is_stressed': True},
                                         {'syllable': 'ces', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'e', 'is_stressed': True},
                                         {'syllable': 'sa', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'luz', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'de', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'o', 'is_stressed': False},
                                         {'syllable': 'to', 'is_stressed': True},
                                         {'syllable': 'ño', 'is_stressed': False}],
                           'stress_position': -2}]},
              {'tokens': [{'syllables': [{'syllable': 'me', 'is_stressed': False}],
                           'stress_position': 0},
                          {'syllables': [{'syllable': 're', 'is_stressed': False},
                                         {'syllable': 'cor', 'is_stressed': False},
                                         {'syllable': 'dó', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'a', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'Fray', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'Luis', 'is_stressed': True}],
                           'stress_position': -1},
                          {'symbol': ':'}]},
              {'tokens': [{'symbol': '«'},
                          {'syllables': [{'syllable': 'Ya', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'el', 'is_stressed': False}],
                           'stress_position': 0},
                          {'syllables': [{'syllable': 'tiem', 'is_stressed': True},
                                         {'syllable': 'po', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'nos', 'is_stressed': False}],
                           'stress_position': 0},
                          {'syllables': [{'syllable': 'con', 'is_stressed': False},
                                         {'syllable': 'vi', 'is_stressed': True},
                                         {'syllable': 'da', 'is_stressed': False}],
                           'stress_position': -2}]},
              {'tokens': [{'syllables': [{'syllable': 'A', 'is_stressed': True}],
                           'stress_position': -1},
                          {'syllables': [{'syllable': 'los', 'is_stressed': False}],
                           'stress_position': 0},
                          {'syllables': [{'syllable': 'es', 'is_stressed': False},
                                         {'syllable': 'tu', 'is_stressed': True},
                                         {'syllable': 'dios', 'is_stressed': False}],
                           'stress_position': -2},
                          {'syllables': [{'syllable': 'no', 'is_stressed': True},
                                         {'syllable': 'bles', 'is_stressed': False}],
                           'stress_position': -2},
                          {'symbol': '...'},
                          {'symbol': '»'},
                          {'symbol': '!'}]}]
    assert get_scansion(text) == output


def test_spacy_tag_to_dict():
    tag = "DET__Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs"
    output = {'DET__Number': 'Sing', 'Number[psor]': 'Sing', 'Person': '1', 'Poss': 'Yes', 'PronType': 'Prs'}
    assert spacy_tag_to_dict(tag) == output


def test_spacy_tag_to_dict_no_tags():
    tag = "DET___"
    assert spacy_tag_to_dict(tag) == {}