from cStringIO import StringIO
from nose.tools import raises, assert_dict_equal, assert_equal

from wos.read import ReadError, PlainTextReader

preamble = """FN Thomson Reuters Web of Science
VR 1.0
"""


@raises(ReadError)
def test_wrong_format():
    f = StringIO("XY Bla\nVR 1.0")
    PlainTextReader(f)


@raises(ReadError)
def test_wrong_version():
    f = StringIO("FN Thomson Reuters Web of Science\nVR 1.1")
    PlainTextReader(f)


@raises(ReadError)
def test_forgotten_EF():
    f = StringIO(preamble + "PT abc\nAU xuz\nER\n\nPT abc2\nEF")
    r = PlainTextReader(f)
    for rec in r:
        pass


def test_ignore_empty_lines():
    f = StringIO("\nFN Thomson Reuters\n\nVR 1.0\nPT abc\n\nAU xyz\nER\nEF")
    r = PlainTextReader(f)

    expected = {u"PT": u"abc", u"AU": u"xyz"}
    assert_dict_equal(next(r), expected)


def test_multiple_records():
    f = StringIO(preamble + "PT abc\nAU xyz\nER\n\nPT abc2\n AU xyz2\n"
                 "AB abstract\nER\nEF")
    r = PlainTextReader(f)

    results = []
    for result in r:
        results.append(result)

    expected = [{u"PT": u"abc", u"AU": u"xyz"},
                {u"PT": u"abc2", u"AU": u"xyz2", u"AB": u"abstract"}]

    assert_equal(len(results), len(expected))
    for result, exp in zip(results, expected):
        assert_dict_equal(result, exp)


def test_multiline_fields_split():
    f = StringIO(preamble + "PT abc\nSO J.Whatever\nAF Here\n   be\n   dragons"
                 "\nER\nEF")

    r = PlainTextReader(f)
    expected = {u"PT": u"abc", u"SO": u"J.Whatever",
                u"AF": u"Here; be; dragons"}
    assert_dict_equal(next(r), expected)

    f.seek(0)
    r = PlainTextReader(f, subdelimiter="##")
    expected[u"AF"] = u"Here##be##dragons"
    assert_dict_equal(next(r), expected)


def test_multiline_fields_nosplit():
    f = StringIO(preamble + "PT abc\nSC Here; there\n  be dragons; Yes"
                 "\nER\nEF")

    r = PlainTextReader(f)
    expected = {u"PT": u"abc", u"SC": u"Here; there be dragons; Yes"}
    assert_dict_equal(next(r), expected)


def test_wos1():
    with open("examples/wos1.txt") as fh:
        r = PlainTextReader(fh)
        for record in r:
            pass
