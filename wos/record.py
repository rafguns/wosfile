import logging

from .read import read
from .tags import is_iterable

__all__ = [
    "Record",
    "read_parse",
]


logger = logging.getLogger(__name__)


class Record(dict):
    def __init__(self, wos_data, subdelimiter="; ", skip_empty=True):
        """Create a record based on *wos_data*

        :param dict wos_data: a WoS record
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)
        :param bool skip_empty: whether or not to skip empty fields

        """
        self.subdelimiter = subdelimiter
        self.skip_empty = skip_empty
        self.parse(wos_data)

    def parse(self, wos_data):
        """Parse *wos_data* into more structured format

        :param dict wos_data: a WoS record

        """
        self.clear()
        for k, v in wos_data.iteritems():
            if self.skip_empty and not v:
                continue
            if is_iterable[k]:
                v = v.split(self.subdelimiter)
            self[k] = v

    @property
    def record_id(self):
        """Get WoS record ID for current data"""
        import re

        first_author = re.sub(r'(.*), (.*)', r'\1 \2', self[u"AU"][0])
        year = self[u"PY"]
        journal = self.get(u"J9",
                           self.get(u"BS", self.get(u"SO")))
        volume = u"V" + self[u"VL"] if u"VL" in self else None
        page = u"P" + self[u"BP"] if u"BP" in self else None
        doi = u"DOI " + self[u"DI"] if u"DI" in self else None

        return u", ".join(item for item in (first_author, year, journal,
                                            volume, page, doi) if item)


def read_parse(fobj, delimiter="\t", subdelimiter="; ", skip_empty=True,
               **kwargs):
    """Read and parse WoS file *fobj*

    :param fobj: WoS CSV file name or handle
    :type fobj: str or file
    :param str delimiter: string delimiting different fields
    :param str subdelimiter:
        string delimiting different parts of a multi-part field, like author(s)
    :param bool skip_empty: whether or not to skip empty fields
    :return:
        iterator over parsed records in *fobj*, where each parsed record is a
        :py:class:`wos.Record`

    """
    for wos_record in read(fobj, delimiter, **kwargs):
        yield Record(wos_record, subdelimiter, skip_empty)
