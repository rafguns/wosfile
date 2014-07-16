import codecs
import logging

from .tags import is_iterable
from .unicodecsv import DictReader

__all__ = [
    "Record",
    "read",
    "read_parse",
    "utf8_file",
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
            # Since WoS files have a spurious tab at the end of each line, we
            # may get a 'ghost' None key, which is also ignored.
            if k is None:
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


def utf8_file(f):
    """Make sure that f is a UTF-8 encoded file

    :param f: Opened file object
    :type f: file object
    :return: The file object, recoded to UTF-8

    """
    encoding = 'utf-8'
    recoder = lambda f, from_encoding, to_encoding: \
        codecs.StreamRecoder(f, codecs.getencoder(to_encoding),
                             codecs.getdecoder(to_encoding),
                             codecs.getreader(from_encoding),
                             codecs.getwriter(to_encoding))

    sniff = f.read(10)

    if sniff.startswith(codecs.BOM_UTF16_LE):
        logger.debug("File '%s' encoded as UTF-16-LE" % f.name)
        f.seek(len(codecs.BOM_UTF16_LE))
        return recoder(f, 'utf-16-le', encoding)

    if sniff.startswith(codecs.BOM_UTF16_BE):
        logger.debug("File '%s' encoded as UTF-16-BE" % f.name)
        f.seek(len(codecs.BOM_UTF16_BE))
        return recoder(f, 'utf-16-be', encoding)

    if sniff.startswith(codecs.BOM_UTF8):
        logger.debug("File '%s' encoded as UTF-8 with BOM" % f.name)
        f.seek(len(codecs.BOM_UTF8))
        return f

    # WoS exports are always(?) UTF-8 or UTF-16
    logger.debug("File '%s' encoded as UTF-8 without BOM" % f.name)
    f.seek(0)
    return f


def get_reader(fh):
    """Get appropriate reader for the file type"""
    return DictReader


def read(fobj, delimiter="\t", **kwargs):
    """Read WoS CSV file recoding (if necessary) to UTF-8

    :param fobj: WoS CSV file name or handle
    :type fobj: str or file
    :param str delimiter: character delimiting different fields
    :return:
        iterator over records in *fobj*, where each record is a field code -
        value dict

    """
    # Make sure we have a file and not a file name
    if not hasattr(fobj, 'read'):
        f = open(fobj)
        close_f = True
    else:
        f = fobj
        close_f = False

    try:
        f = utf8_file(f)
        reader = get_reader(f)(f, delimiter=delimiter, **kwargs)
        for record in reader:
            yield record
    finally:
        if close_f:
            f.close()


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
