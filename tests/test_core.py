from unittest import mock

import spacy

import rantanplan.core
from rantanplan.core import get_orthographic_accent
from rantanplan.core import get_scansion
from rantanplan.core import get_syllables
from rantanplan.core import get_word_stress
from rantanplan.core import have_prosodic_liaison
from rantanplan.core import is_paroxytone
from rantanplan.core import spacy_tag_to_dict
from rantanplan.core import syllabify

nlp = spacy.load('es_core_news_md')


class TokenMock(mock.MagicMock):
    _ = property(lambda self: mock.Mock(has_tmesis=self.has_tmesis,
                                        line=self.line))

    def __isinstance__(self, token):  # noqa
        return True

    @staticmethod
    def is_ancestor(token):  # noqa
        return True

    @staticmethod
    def nbor():  # noqa
        return TokenMock()


def test_get_scansion_spacy_doc(monkeypatch):
    token = TokenMock(text="Agüita", i=0, is_punct=False, has_tmesis=False, line=1)

    def mockreturn(lang=None):
        return lambda _: [
            token
        ]

    monkeypatch.setattr(rantanplan.core, 'load_pipeline', mockreturn)
    enjambment = get_scansion(token)
    assert enjambment == [
        {'tokens': [
            {'word': [
                {'syllable': 'A', 'is_stressed': False},
                {'syllable': 'güi', 'is_stressed': True},
                {'syllable': 'ta', 'is_stressed': False}],
                'stress_position': -2}],
            'phonological_groups': [
                {'syllable': 'A', 'is_stressed': False},
                {'syllable': 'güi', 'is_stressed': True},
                {'syllable': 'ta', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '-+-', 'type': 'pattern'},
            'rhythmical_length': 3}]


def test_have_prosodic_liaison():
    first_syllable = {'syllable': 'ca', 'is_stressed': True}
    second_syllable = {'syllable': 'en', 'is_stressed': False}
    assert have_prosodic_liaison(first_syllable, second_syllable) is True


def test_syllabify_exceptions_en():
    word = "entender"
    output = ['en', 'ten', 'der']
    assert syllabify(word)[0] == output


def test_syllabify_exceptions_en_2():
    word = "desentender"
    output = ['de', 'sen', 'ten', 'der']
    assert syllabify(word)[0] == output


def test_syllabify_exceptions_en_3():
    word = "desenmarañados"
    output = ['de', 'sen', 'ma', 'ra', 'ña', 'dos']
    assert syllabify(word)[0] == output


def test_syllabify_exceptions_prefix_des_consonant():
    word = "destapar"
    output = ['des', 'ta', 'par']
    assert syllabify(word)[0] == output


def test_syllabify_exceptions_prefix_sin_consonant():
    word = "sinhueso"
    output = ['sin', 'hue', 'so']
    assert syllabify(word)[0] == output


def test_syllabify_exceptions_rh_dipthong():
    word = "marhuenda"
    output = ['mar', 'huen', 'da']
    assert syllabify(word)[0] == output


def test_syllabify_tl():
    word = "atlante"
    output = ['a', 'tlan', 'te']
    assert syllabify(word)[0] == output


def test_syllabify_group_1():
    word = "antihumano"
    output = ['an', 'ti', 'hu', 'ma', 'no']
    assert syllabify(word)[0] == output


def test_syllabify_group_2():
    word = "entrehierro"
    output = ['en', 'tre', 'hie', 'rro']
    assert syllabify(word)[0] == output


def test_syllabify_group_3():
    word = "yihad"
    output = ['yi', 'had']
    assert syllabify(word)[0] == output


def test_syllabify_group_4():
    word = "coche"
    output = ['co', 'che']
    assert syllabify(word)[0] == output


def test_syllabify_group_4_rl():
    word = "abarloar"
    output = ['a', 'bar', 'lo', 'ar']
    assert syllabify(word)[0] == output


def test_syllabify_group_5():
    word = "checo"
    output = ['che', 'co']
    assert syllabify(word)[0] == output


def test_syllabify_group_6():
    word = "año"
    output = ['a', 'ño']
    assert syllabify(word)[0] == output


def test_syllabify_group_7():
    word = "desvirtúe"
    output = ['des', 'vir', 'tú', 'e']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_u_e():
    word = "güegüecho"
    output = ['güe', 'güe', 'cho']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_hyatus_with_consonant_1():
    word = "insacïable"
    output = ['in', 'sa', 'cï', 'a', 'ble']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_hyatus_with_consonant_2():
    word = "ruïdo"
    output = ['ru', 'ï', 'do']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_hyatus_with_vowel():
    word = "ruëa"
    output = ['ru', 'ë', 'a']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_u_i():
    word = "güito"
    output = ['güi', 'to']
    assert syllabify(word)[0] == output


def test_syllabify_umlaut_u_i_tilde():
    word = "agüío"
    output = ['a', 'güí', 'o']
    assert syllabify(word)[0] == output


def test_syllabify_alternatives():
    word = "arcaizabas"
    output = (['ar', 'cai', 'za', 'bas'],
              [(['ar', 'ca', 'i', 'za', 'bas'], (1, 2))])
    assert syllabify(word) == output


def test_syllabify_alternatives_2():
    word = "puntual"
    output = (['pun', 'tual'],
              [(['pun', 'tu', 'al'], (1, 2))])
    assert syllabify(word) == output


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
    output = {
        'word': [
            {'syllable': 'plá', 'is_stressed': True},
            {'syllable': 'ta', 'is_stressed': False},
            {'syllable': 'no', 'is_stressed': False}], 'stress_position': -3}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_stressed_monosyllables_without_tilde():
    word = "yo"
    pos = "PRON"
    tag = {'Case': 'Nom', 'Number': 'Sing', 'Person': '1', 'PronType': 'Prs'}
    output = {
        'word': [
            {'syllable': 'yo', 'is_stressed': True}],
        'stress_position': -1}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_unstressed_monosyllables_without_tilde():
    word = "mi"
    pos = "DET"
    tag = {'Number': 'Sing', 'Number[psor]': 'Sing', 'Person': '1', 'Poss': 'Yes', 'PronType': 'Prs'}
    output = {
        'word': [
            {'syllable': 'mi', 'is_stressed': False}],
        'stress_position': 0}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_no_tilde():
    word = "campo"
    pos = "NOUN"
    tag = {'Gender': 'Masc', 'Number': 'Sing'}
    output = {
        'word': [
            {'syllable': 'cam', 'is_stressed': True},
            {'syllable': 'po', 'is_stressed': False}],
        'stress_position': -2}
    assert get_word_stress(word, pos, tag) == output


def test_get_word_stress_oxytone():
    word = "tambor"
    pos = "NOUN"
    tag = {'Gender': 'Fem', 'Number': 'Sing'}
    output = {
        'word': [
            {'syllable': 'tam', 'is_stressed': False},
            {'syllable': 'bor', 'is_stressed': True}],
        'stress_position': -1}
    assert get_word_stress(word, pos, tag) == output


def test_get_syllables():
    word = nlp('físico-químico')
    output = [
        {
            'word': [
                {'syllable': 'fí', 'is_stressed': True}, {'syllable': 'si', 'is_stressed': False},
                {'syllable': 'co', 'is_stressed': False}], 'stress_position': -3}, {'symbol': '-'}, {
            'word': [
                {'syllable': 'quí', 'is_stressed': True}, {'syllable': 'mi', 'is_stressed': False},
                {'syllable': 'co', 'is_stressed': False}], 'stress_position': -3}]
    assert get_syllables(word) == output


def test_get_scansion():
    text = """Siempre en octubre comenzaba el año.
    ¡Y cuántas veces esa luz de otoño
    me recordó a Fray Luis:
    «Ya el tiempo nos convida
    A los estudios nobles...»!"""
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'Siem', 'is_stressed': True},
                {'syllable': 'pre', 'is_stressed': False, 'has_synalepha': True}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'en', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'oc', 'is_stressed': False},
                {'syllable': 'tu', 'is_stressed': True},
                {'syllable': 'bre', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'co', 'is_stressed': False},
                {'syllable': 'men', 'is_stressed': False},
                {'syllable': 'za', 'is_stressed': True},
                {'syllable': 'ba', 'is_stressed': False, 'has_synalepha': True}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'el', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'a', 'is_stressed': True},
                {'syllable': 'ño', 'is_stressed': False}],
                'stress_position': -2},
            {'symbol': '.'}],
            'phonological_groups': [
                {'syllable': 'Siem', 'is_stressed': True},
                {'is_stressed': False, 'syllable': 'preen', 'has_synalepha': True},
                {'syllable': 'oc', 'is_stressed': False},
                {'syllable': 'tu', 'is_stressed': True},
                {'syllable': 'bre', 'is_stressed': False},
                {'syllable': 'co', 'is_stressed': False},
                {'syllable': 'men', 'is_stressed': False},
                {'syllable': 'za', 'is_stressed': True},
                {'is_stressed': False, 'syllable': 'bael', 'has_synalepha': True},
                {'syllable': 'a', 'is_stressed': True},
                {'syllable': 'ño', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '+--+---+-+-', 'type': 'pattern'},
            'rhythmical_length': 11},
        {'tokens': [
            {'symbol': '¡'},
            {'word': [
                {'syllable': 'Y', 'is_stressed': True}], 'stress_position': -1},
            {'word': [
                {'syllable': 'cuán', 'is_stressed': True},
                {'syllable': 'tas', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 've', 'is_stressed': True},
                {'syllable': 'ces', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'e', 'is_stressed': True},
                {'syllable': 'sa', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'luz', 'is_stressed': True}], 'stress_position': -1},
            {'word': [
                {'syllable': 'de', 'is_stressed': False, 'has_synalepha': True}],
                'stress_position': 0},
            {'word': [
                {'syllable': 'o', 'is_stressed': False},
                {'syllable': 'to', 'is_stressed': True},
                {'syllable': 'ño', 'is_stressed': False}],
                'stress_position': -2}],
            'phonological_groups': [
                {'syllable': 'Y', 'is_stressed': True},
                {'syllable': 'cuán', 'is_stressed': True},
                {'syllable': 'tas', 'is_stressed': False},
                {'syllable': 've', 'is_stressed': True},
                {'syllable': 'ces', 'is_stressed': False},
                {'syllable': 'e', 'is_stressed': True},
                {'syllable': 'sa', 'is_stressed': False},
                {'syllable': 'luz', 'is_stressed': True},
                {'is_stressed': False, 'syllable': 'deo', 'has_synalepha': True},
                {'syllable': 'to', 'is_stressed': True},
                {'syllable': 'ño', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '++-+-+-+-+-', 'type': 'pattern'},
            'rhythmical_length': 11},
        {'tokens': [
            {'word': [
                {'syllable': 'me', 'is_stressed': False}],
                'stress_position': 0},
            {'word': [
                {'syllable': 're', 'is_stressed': False},
                {'syllable': 'cor', 'is_stressed': False},
                {'syllable': 'dó', 'is_stressed': True, 'has_synalepha': True}],
                'stress_position': -1},
            {'word': [
                {'syllable': 'a', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'Fray', 'is_stressed': True}],
                'stress_position': -1},
            {'word': [
                {'syllable': 'Luis', 'is_stressed': True}],
                'stress_position': -1},
            {'symbol': ':'}],
            'phonological_groups': [
                {'syllable': 'me', 'is_stressed': False},
                {'syllable': 're', 'is_stressed': False},
                {'syllable': 'cor', 'is_stressed': False},
                {'is_stressed': True, 'syllable': 'dóa', 'has_synalepha': True},
                {'syllable': 'Fray', 'is_stressed': True},
                {'syllable': 'Luis', 'is_stressed': True}],
            'rhythm': {'rhythmical_stress': '---+++-', 'type': 'pattern'},
            'rhythmical_length': 7},
        {'tokens': [
            {'symbol': '«'},
            {'word': [
                {'syllable': 'Ya', 'is_stressed': True, 'has_synalepha': True}],
                'stress_position': -1},
            {'word': [
                {'syllable': 'el', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'tiem', 'is_stressed': True},
                {'syllable': 'po', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'nos', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'con', 'is_stressed': False},
                {'syllable': 'vi', 'is_stressed': True},
                {'syllable': 'da', 'is_stressed': False}],
                'stress_position': -2}],
            'phonological_groups': [
                {'is_stressed': True,
                 'syllable': 'Yael',
                 'has_synalepha': True},
                {'syllable': 'tiem', 'is_stressed': True},
                {'syllable': 'po', 'is_stressed': False},
                {'syllable': 'nos', 'is_stressed': False},
                {'syllable': 'con', 'is_stressed': False},
                {'syllable': 'vi', 'is_stressed': True},
                {'syllable': 'da', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '++---+-', 'type': 'pattern'},
            'rhythmical_length': 7},
        {'tokens': [
            {'word': [
                {'syllable': 'A', 'is_stressed': False}],
                'stress_position': 0},
            {'word': [
                {'syllable': 'los', 'is_stressed': False}], 'stress_position': 0},
            {'word': [
                {'syllable': 'es', 'is_stressed': False},
                {'syllable': 'tu', 'is_stressed': True},
                {'syllable': 'dios', 'is_stressed': False}],
                'stress_position': -2},
            {'word': [
                {'syllable': 'no', 'is_stressed': True},
                {'syllable': 'bles', 'is_stressed': False}],
                'stress_position': -2},
            {'symbol': '...'},
            {'symbol': '»'},
            {'symbol': '!'}],
            'phonological_groups': [
                {'syllable': 'A', 'is_stressed': False},
                {'syllable': 'los', 'is_stressed': False},
                {'syllable': 'es', 'is_stressed': False},
                {'syllable': 'tu', 'is_stressed': True},
                {'syllable': 'dios', 'is_stressed': False},
                {'syllable': 'no', 'is_stressed': True},
                {'syllable': 'bles', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '---+-+-', 'type': 'pattern'},
            'rhythmical_length': 7}]
    assert get_scansion(text, rhythm_format="pattern") == output


def test_get_scansion_stressed_last_syl():
    text = "altavoz"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'al', 'is_stressed': False},
                {'syllable': 'ta', 'is_stressed': False},
                {'syllable': 'voz', 'is_stressed': True}],
                'stress_position': -1}],
            'phonological_groups': [
                {'syllable': 'al', 'is_stressed': False},
                {'syllable': 'ta', 'is_stressed': False},
                {'syllable': 'voz', 'is_stressed': True}],
            'rhythm': {'rhythmical_stress': '--+-', 'type': 'pattern'},
            'rhythmical_length': 4}]
    assert get_scansion(text, rhythm_format="pattern") == output


def test_get_scansion_stressed_last_syl_index_metrical_pattern():
    text = "altavoz"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'al', 'is_stressed': False},
                {'syllable': 'ta', 'is_stressed': False},
                {'syllable': 'voz', 'is_stressed': True}],
                'stress_position': -1}],
            'phonological_groups': [
                {'syllable': 'al', 'is_stressed': False},
                {'syllable': 'ta', 'is_stressed': False},
                {'syllable': 'voz', 'is_stressed': True}],
            'rhythm': {'rhythmical_stress': [2]},
            'type': 'indexed',
            'rhythmical_length': 4}]
    assert get_scansion(text, rhythm_format="indexed") == output


def test_get_scansion_sinaeresis():
    text = "héroe"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'hé', 'is_stressed': True},
                {'syllable': 'ro', 'is_stressed': False, 'has_sinaeresis': True},
                {'syllable': 'e', 'is_stressed': False}],
                'stress_position': -3}],
            'phonological_groups': [
                {'syllable': 'hé', 'is_stressed': True},
                {'is_stressed': False, 'syllable': 'roe', 'has_sinaeresis': True}],
            'rhythm': {'rhythmical_stress': '+-', 'type': 'pattern'},
            'rhythmical_length': 2}]
    assert get_scansion(text, rhythm_format="pattern") == output


def test_get_scansion_affixes():
    text = "antiquísimo"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'syllable': 'mo', 'is_stressed': False}],
                'stress_position': -3}],
            'phonological_groups': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'syllable': 'mo', 'is_stressed': False}],
            'rhythm': {'rhythmical_stress': '--+-', 'type': 'pattern'},
            'rhythmical_length': 4}]
    assert get_scansion(text, rhythm_format="pattern") == output


def test_get_scansion_sinaeresis_synalepha_affixes():
    text = "antiquísimo héroe"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'syllable': 'mo', 'is_stressed': False, 'has_synalepha': True}],
                'stress_position': -3},
            {'word': [
                {'syllable': 'hé', 'is_stressed': True},
                {'syllable': 'ro', 'is_stressed': False, 'has_sinaeresis': True},
                {'syllable': 'e', 'is_stressed': False}],
                'stress_position': -3}],
            'phonological_groups': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'is_stressed': True, 'syllable': 'mohé', 'has_synalepha': True},
                {'is_stressed': False, 'syllable': 'roe', 'has_sinaeresis': True}],
            'rhythm': {'rhythmical_stress': '--+-+-', 'type': 'pattern'},
            'rhythmical_length': 6}]
    assert get_scansion(text, rhythm_format="pattern") == output


def test_get_scansion_sinaeresis_synalepha_affixes_index_metrical_pattern():
    text = "antiquísimo héroe"
    output = [
        {'tokens': [
            {'word': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'syllable': 'mo', 'is_stressed': False, 'has_synalepha': True}],
                'stress_position': -3},
            {'word': [
                {'syllable': 'hé', 'is_stressed': True},
                {'syllable': 'ro', 'is_stressed': False, 'has_sinaeresis': True},
                {'syllable': 'e', 'is_stressed': False}],
                'stress_position': -3}],
            'phonological_groups': [
                {'syllable': 'an', 'is_stressed': False},
                {'syllable': 'ti', 'is_stressed': False},
                {'syllable': 'quí', 'is_stressed': True},
                {'syllable': 'si', 'is_stressed': False},
                {'is_stressed': True, 'syllable': 'mohé', 'has_synalepha': True},
                {'is_stressed': False, 'syllable': 'roe', 'has_sinaeresis': True}],
            'rhythm': {'rhythmical_stress': [2, 4]},
            'type': 'indexed',
            'rhythmical_length': 6}]
    assert get_scansion(text, rhythm_format="indexed") == output


def test_spacy_tag_to_dict():
    tag = "DET__Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs"
    output = {'DET__Number': 'Sing', 'Number[psor]': 'Sing', 'Person': '1', 'Poss': 'Yes', 'PronType': 'Prs'}
    assert spacy_tag_to_dict(tag) == output


def test_spacy_tag_to_dict_no_tags():
    tag = "DET___"
    assert spacy_tag_to_dict(tag) == {}
