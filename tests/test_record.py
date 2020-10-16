import tempfile

import pytest

from wosfile.record import Record, parse_address_field, records_from


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
        "C1": "Univ Michigan; Stanford Univ",
    }

    def test_init(self):
        rec = Record(self.data, skip_empty=False)
        assert rec.skip_empty is False

    def test_parse(self):
        rec = Record()
        rec.parse(self.data)

        assert dict(rec) == {
            "PT": "J",
            "AU": ["Doe, J", "Foo, B"],
            "C1": "Univ Michigan; Stanford Univ",
            "TI": "Title here",
            "DE": ["desc1", "desc2", "desc3"],
            "PY": "2016",
            "J9": "J9",
            "BS": "BS",
            "SO": "SO",
            "VL": "4",
            "BP": "102",
            "DI": "123",
        }

        rec.skip_empty = False
        rec.parse(self.data)
        assert "AB" in rec

    def test_record_id(self):
        rec = Record(self.data)
        assert rec.record_id == "Doe J, 2016, J9, V4, P102, DOI 123"

    def test_record_author_address(self):
        rec = Record(self.data)
        assert rec.author_address == ["Univ Michigan", "Stanford Univ"]


def test_parse_address_field_simple():
    """Correctly split C1 (address) records like foo; bar; baz"""
    value = "Address A, Q; Address B, C; Address D, E"
    res = parse_address_field(value)
    expected = ["Address A, Q", "Address B, C", "Address D, E"]
    assert res == expected


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
    assert res == expected


def test_parse_invalid_address_field():
    value = "[a; b x"
    with pytest.raises(ValueError):
        parse_address_field(value)


def test_records_from():
    data = b"""FN Thomson Reuters Web of Science\nVR 1.0
PT J\nAU John\nER
PT J\nAU Mary\nER\nEF"""

    _, fname = tempfile.mkstemp()
    with open(fname, "wb") as f:
        f.write(data)

    results = list(records_from(fname))
    expected = [{"PT": "J", "AU": "John"}, {"PT": "J", "AU": "Mary"}]
    for res, exp in zip(results, expected):
        assert isinstance(res, Record)
        assert res == Record(exp)


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
        assert isinstance(res, Record)
        assert res == Record(exp)
