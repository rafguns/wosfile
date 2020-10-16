import tempfile

import pytest

from wosfile.record import Record, parse_address_field, records_from


records = [
    # (data, record_id, author_address)
    (
        {
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
        },
        "Doe J, 2016, J9, V4, P102, DOI 123",
        ["Univ Michigan", "Stanford Univ"],
    ),
]


@pytest.mark.parametrize("data, record_id, author_address", records)
def test_record_init(data, record_id, author_address):
    rec = Record(data, skip_empty=False)
    assert rec.skip_empty is False


@pytest.mark.parametrize("data, record_id, author_address", records)
def test_record_parse(data, record_id, author_address):
    rec = Record()
    rec.parse(data)
    assert rec["PT"] == data["PT"]
    assert type(rec["AU"]) == list


@pytest.mark.parametrize("data, record_id, author_address", records)
def test_record_skip_empty(data, record_id, author_address):
    rec = Record()
    rec.parse(data)
    assert "AB" not in rec

    rec.skip_empty = False
    rec.parse(data)
    assert "AB" in rec


@pytest.mark.parametrize("data, record_id, author_address", records)
def test_record_id(data, record_id, author_address):
    rec = Record(data)
    assert rec.record_id == record_id


@pytest.mark.parametrize("data, record_id, author_address", records)
def test_record_author_address(data, record_id, author_address):
    rec = Record(data)
    assert rec.author_address == author_address


addresses = [
    # (input, expected, exception)
    (
        "Address A, Q; Address B, C; Address D, E",
        ["Address A, Q", "Address B, C", "Address D, E"],
        None,
    ),
    (
        "[A; B] address AB; [C] address C 1; [C] address C 2; " "[C; D] address CD",
        {
            "A": ["address AB"],
            "B": ["address AB"],
            "C": ["address C 1", "address C 2", "address CD"],
            "D": ["address CD"],
        },
        None,
    ),
    ("[a; b x", None, ValueError),
    # Mixture of with and without authors (issue #8), slightly simplified from WOS:000381400500004
    (
        (
            "Univ Leuven, Dept Earth & Environm Sci, Leuven, Belgium; "
            "Univ Leuven, Dept Earth & Environm Sci, Leuven, Belgium; "
            "[Bi, Lingling; Vanneste, Dominique] Univ Leuven, Dept Earth & Environm Sci, Leuven, Belgium; "
            "[Bi, Lingling] Xian Int Studies Univ, Sch Tourism, Xian, Peoples R China"
        ),
        {
            "Bi, Lingling": [
                "Univ Leuven, Dept Earth & Environm Sci, Leuven, Belgium",
                "Xian Int Studies Univ, Sch Tourism, Xian, Peoples R China",
            ],
            "Vanneste, Dominique": [
                "Univ Leuven, Dept Earth & Environm Sci, Leuven, Belgium"
            ],
        },
        None,
    ),
]


@pytest.mark.parametrize("input, expected, exception", addresses)
def test_parse_address_field(input, expected, exception):
    """Correctly parse C1 (address) fields"""
    if exception is not None:
        with pytest.raises(exception):
            parse_address_field(input)
    else:
        res = parse_address_field(input)
        assert res == expected


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
