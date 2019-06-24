import tempfile
from wos.record import Record, records_from, parse_address_field

from nose.tools import assert_dict_equal, assert_equal, assert_is_instance


class TestRecord:
    data = {
        "PT": "J",
        "AU": "Doe, J;  Foo, B",
        "TI": "Title here",
        "DE": "desc1; desc2; desc3",
        "PY": "2016",
        "J9": "J9",
        "BS": "BS",
        "SO": "SO",
        "VL": "4",
        "BP": "102",
        "DI": "123",
        "AB": "",
    }

    def test_init(self):
        rec = Record(self.data, skip_empty=False)
        assert_equal(rec.skip_empty, False)

    def test_parse(self):
        rec = Record()
        rec.parse(self.data)

        assert_equal(
            dict(rec),
            {
                "PT": "J",
                "AU": ["Doe, J", "Foo, B"],
                "TI": "Title here",
                "DE": ["desc1", "desc2", "desc3"],
                "PY": "2016",
                "J9": "J9",
                "BS": "BS",
                "SO": "SO",
                "VL": "4",
                "BP": "102",
                "DI": "123",
            },
        )

        rec.skip_empty = False
        rec.parse(self.data)
        assert "AB" in rec

    def test_record_id(self):
        rec = Record(self.data)
        assert_equal(rec.record_id, "Doe J, 2016, J9, V4, P102, DOI 123")


def test_parse_address_field_simple():
    """Correctly split C1 (address) records like foo; bar; baz"""
    value = "Address A, Q; Address B, C; Address D, E"
    res = parse_address_field(value)
    expected = ["Address A, Q", "Address B, C", "Address D, E"]
    assert_equal(res, expected)


def test_parse_address_field_complex():
    """Correctly split C1 (address) records like [A; B] foo; [C; D] bar"""
    value = "[A; B] address AB; [C] address C 1; [C] address C 2; " "[C; D] address CD"
    res = parse_address_field(value)
    expected = {
        "A": ["address AB"],
        "B": ["address AB"],
        "C": ["address C 1", "address C 2", "address CD"],
        "D": ["address CD"],
    }
    assert_dict_equal(res, expected)


def test_records_from():
    data = b"""FN Thomson Reuters Web of Science\nVR 1.0
PT J\nAU John\nER
PT J\nAU Mary\nER\nEF"""

    fd, fname = tempfile.mkstemp()
    with open(fname, "wb") as f:
        f.write(data)

    results = list(records_from(fname))
    expected = [{"PT": "J", "AU": "John"}, {"PT": "J", "AU": "Mary"}]
    for res, exp in zip(results, expected):
        assert_is_instance(res, Record)
        assert_equal(res, Record(exp))


def test_records_from_multiple_files():
    data = [
        b"FN Thomson Reuters Web of Science\nVR 1.0\n" b"PT J\nAU John\nER\nEF",
        b"FN Thomson Reuters Web of Science\nVR 1.0\n" b"PT J\nAU Mary\nER\nEF",
    ]

    files = []
    for d in data:
        fd, fname = tempfile.mkstemp()
        with open(fname, "wb") as f:
            f.write(d)
        files.append((fd, fname))

    results = list(records_from([fname for _, fname in files]))
    expected = [{"PT": "J", "AU": "John"}, {"PT": "J", "AU": "Mary"}]
    for res, exp in zip(results, expected):
        assert_is_instance(res, Record)
        assert_equal(res, Record(exp))
