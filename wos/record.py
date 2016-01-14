from __future__ import unicode_literals

from .read import read
from .tags import is_iterable

__all__ = [
    "Record",
    "records_from",
]


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
            if is_iterable[k]:
                v = [part.strip() for part in v.split(self.subdelimiter)]
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


def records_from(fobj, subdelimiter="; ", skip_empty=True, **kwargs):
    """Get records from WoS file *fobj*

    :param fobj: WoS file name or file handle
    :type fobj: str or file
    :param str subdelimiter:
        string delimiting different parts of a multi-part field, like author(s)
    :param bool skip_empty: whether or not to skip empty fields
    :return:
        iterator over parsed records in *fobj*, where each parsed record is a
        :py:class:`wos.Record`

    """
    for wos_record in read(fobj, **kwargs):
        yield Record(wos_record, subdelimiter, skip_empty)
