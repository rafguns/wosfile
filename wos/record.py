from __future__ import unicode_literals

import re
from collections import defaultdict

from .read import read
from .tags import is_address_field, is_iterable

__all__ = [
    "Record",
    "records_from",
]


def split_by(string, delimiter):
    return [part.strip() for part in string.split(delimiter)]


class Record(dict):
    def __init__(self, wos_data=None, subdelimiter="; ", skip_empty=True):
        """Create a record based on *wos_data*

        :param dict wos_data: a WoS record
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)
        :param bool skip_empty: whether or not to skip empty fields

        """
        self.subdelimiter = subdelimiter
        self.skip_empty = skip_empty
        if wos_data:
            self.parse(wos_data)

    def parse(self, wos_data):
        """Parse *wos_data* into more structured format

        :param dict wos_data: a WoS record

        """
        self.clear()
        for k, v in wos_data.items():
            if self.skip_empty and not v:
                continue
            if is_address_field[k]:
                v = parse_address_field(v, self.subdelimiter)
            elif is_iterable[k]:
                v = split_by(v, self.subdelimiter)
            self[k] = v

    @property
    def record_id(self):
        """Get WoS record ID for current data"""
        import re

        first_author = re.sub(r'(.*), (.*)', r'\1 \2', self["AU"][0])
        year = self["PY"]
        journal = self.get("J9",
                           self.get("BS", self.get("SO")))
        volume = "V" + self["VL"] if "VL" in self else None
        page = "P" + self["BP"] if "BP" in self else None
        doi = "DOI " + self["DI"] if "DI" in self else None

        return ", ".join(item for item in (first_author, year, journal,
                                           volume, page, doi) if item)


def parse_address_field(field, subdelimiter='; '):
    """Parse author address field into author -> addresses dict"""
    # Only addresses, no authors
    if not field.startswith('['):
        addresses = field.split('; ')
        return addresses

    # Addresses with authors
    address_field_re = re.compile(r"""\s*\[(.*?)\] # Author part
                                  \s+(.*)          # Address part
                                  """, re.VERBOSE)
    parsed = defaultdict(list)

    address_fields = re.split(';(?=\s*\[)', field)
    for address_field in address_fields:
        authors, address = address_field_re.match(address_field).groups()
        authors = split_by(authors, subdelimiter)

        for author in authors:
            parsed[author].append(address)

    return parsed


def records_from(fname, subdelimiter="; ", skip_empty=True, **kwargs):
    """Get records from WoS file *fobj*

    :param fobj: WoS file name(s)
    :type fobj: str or list of strings
    :param str subdelimiter:
        string delimiting different parts of a multi-part field, like author(s)
    :param bool skip_empty: whether or not to skip empty fields
    :return:
        iterator over parsed records in *fobj*, where each parsed record is a
        :py:class:`wos.Record`

    """
    for wos_record in read(fname, **kwargs):
        yield Record(wos_record, subdelimiter, skip_empty)
