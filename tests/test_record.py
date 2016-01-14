from wos.record import Record, records_from

from nose.tools import *


class TestRecord:
    data = {
        'PT': 'J',
        'AU': 'Doe, J;  Foo, B',
        'TI': 'Title here',
        'DE': 'desc1; desc2; desc3',
        'PY': '2016',
        'J9': 'J9',
        'BS': 'BS',
        'SO': 'SO',
        'VL': '4',
        'BP': '102',
        'DI': '123',
        'AB': ''
    }

    def test_init(self):
        rec = Record(self.data, skip_empty=False)
        assert_equal(rec.skip_empty, False)

    def test_parse(self):
        # TODO: make Record accept
        rec = Record()
        rec.parse(self.data)

        assert_equal(dict(rec),
                     {'PT': 'J',
                      'AU': ['Doe, J',  'Foo, B'],
                      'TI': 'Title here',
                      'DE': ['desc1', 'desc2', 'desc3'],
                      'PY': '2016',
                      'J9': 'J9',
                      'BS': 'BS',
                      'SO': 'SO',
                      'VL': '4',
                      'BP': '102',
                      'DI': '123'})

        rec.skip_empty = False
        rec.parse(self.data)
        assert 'AB' in rec

    def test_parse_multiple_addresses(self):
        """Correctly split C1 (address) records like [A; B] foo; [C; D] bar"""

    def test_record_id(self):
        rec = Record(self.data)
        assert_equal(rec.record_id, 'Doe J, 2016, J9, V4, P102, DOI 123')


def test_records_from():
    pass
