from cStringIO import StringIO
from nose.tools import raises, assert_dict_equal, assert_equal

from wos.read import (ReadError, PlainTextReader, TabDelimitedReader)

preamble = """FN Thomson Reuters Web of Science
VR 1.0
"""


class TestPlainTextReader:
    @raises(ReadError)
    def test_wrong_format(self):
        f = StringIO("XY Bla\nVR 1.0")
        PlainTextReader(f)

    @raises(ReadError)
    def test_wrong_version(self):
        f = StringIO("FN Thomson Reuters Web of Science\nVR 1.1")
        PlainTextReader(f)

    @raises(ReadError)
    def test_forgotten_EF(self):
        f = StringIO(preamble + "PT abc\nAU xuz\nER\n\nPT abc2\nEF")
        r = PlainTextReader(f)
        for rec in r:
            pass

    def test_ignore_empty_lines(self):
        f = StringIO("\nFN Thomson Reuters\n\nVR 1.0\nPT abc\n\nAU xyz\nER"
                     "\nEF")
        r = PlainTextReader(f)

        expected = {u"PT": u"abc", u"AU": u"xyz"}
        assert_dict_equal(next(r), expected)

    def test_multiple_records(self):
        f = StringIO(preamble + "PT abc\nAU xyz\nER\n\nPT abc2\n AU xyz2\n"
                     "AB abstract\nER\nEF")
        r = PlainTextReader(f)

        results = [result for result in r]
        expected = [{u"PT": u"abc", u"AU": u"xyz"},
                    {u"PT": u"abc2", u"AU": u"xyz2", u"AB": u"abstract"}]

        assert_equal(len(results), len(expected))
        for result, exp in zip(results, expected):
            assert_dict_equal(result, exp)

    def test_multiline_fields_split(self):
        f = StringIO(preamble + "PT abc\nSO J.Whatever\nAF Here\n   be\n"
                     "   dragons"
                     "\nER\nEF")

        r = PlainTextReader(f)
        expected = {u"PT": u"abc", u"SO": u"J.Whatever",
                    u"AF": u"Here; be; dragons"}
        assert_dict_equal(next(r), expected)

        f.seek(0)
        r = PlainTextReader(f, subdelimiter="##")
        expected[u"AF"] = u"Here##be##dragons"
        assert_dict_equal(next(r), expected)

    def test_multiline_fields_nosplit(self):
        f = StringIO(preamble + "PT abc\nSC Here; there\n  be dragons; Yes"
                     "\nER\nEF")

        r = PlainTextReader(f)
        expected = {u"PT": u"abc", u"SC": u"Here; there be dragons; Yes"}
        assert_dict_equal(next(r), expected)

    def test_wos_plaintext(self):
        with open("data/wos_plaintext.txt") as fh:
            r = PlainTextReader(fh)
            for record in r:
                pass


class TestTabDelimitedReader:

    def test_one_record(self):
        f = StringIO("PT\tAF\tC1\nJ\tAa; Bb\tX; Y")

        r = TabDelimitedReader(f)
        expected = {u"PT": u"J", u"AF": u"Aa; Bb", u"C1": u"X; Y"}

        assert_dict_equal(next(r), expected)

    def test_multiple_records(self):
        f = StringIO("PT\tAF\tC1\nJ\tAa; Bb\tX; Y\nJ\tBb; Cc\tY; Z")
        r = TabDelimitedReader(f)

        results = [result for result in r]
        expected = [{u"PT": u"J", u"AF": u"Aa; Bb", u"C1": u"X; Y"},
                    {u"PT": u"J", u"AF": u"Bb; Cc", u"C1": u"Y; Z"}]

        assert_equal(len(results), len(expected))
        for result, exp in zip(results, expected):
            assert_dict_equal(result, exp)

    def test_spurious_tab_at_end(self):
        f = StringIO("PT\tAU\tC1\nJ\ta\tb\t")
        r = TabDelimitedReader(f)

        expected = {u"PT": u"J", u"AU": u"a", u"C1": u"b"}
        assert_dict_equal(next(r), expected)

    def test_wos_tabdelimited_utf16(self):
        with open("data/wos_tab_delimited_win_utf16.txt") as fh:
            r = TabDelimitedReader(fh)
            for record in r:
                pass

    def test_wos_tabdelimited_utf8(self):
        with open("data/wos_tab_delimited_win_utf8.txt") as fh:
            r = TabDelimitedReader(fh)
            for record in r:
                pass

# This fails because of small differences between content of fields in the two
# formats...
#def test_plaintext_tabdelimited_equivalent():
#    with open("data/wos_plaintext.txt") as plaintext,\
#            open("data/wos_tab_delimited_win_utf8.txt") as tabdelimited:
#        pt_reader = PlainTextReader(plaintext)
#        td_reader = TabDelimitedReader(tabdelimited)
#        for pt in pt_reader:
#            td = next(td_reader)
#            for k, v in pt.iteritems():
#                assert_equal(v, td[k])
