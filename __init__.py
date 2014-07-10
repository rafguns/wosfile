import codecs
import logging

from wos.unicodecsv import DictReader

logger = logging.getLogger(__name__)


# Based on http://images.webofknowledge.com/WOK46/help/WOS/h_fieldtags.html
# Format: (Abbreviation, Full label, Iterable?)
headings = (
    (u"AB", u"Abstract", False),
    (u"AF", u"Author Full Name", True),
    (u"AR", u"Article Number", False),
    (u"AU", u"Authors", True),
    (u"BA", u"BA", False),  # Unknown
    (u"BE", u"Book Editors", True),
    (u"BN", u"ISBN", False),
    (u"BP", u"Beginning Page", False),
    (u"BS", u"Book Series Subtitle", False),
    (u"C1", u"Author Address", True),
    (u"CA", u"Group Authors", False),
    (u"CL", u"Conference Location", False),
    (u"CR", u"Cited References", True),
    (u"CT", u"Conference Title", False),
    (u"CY", u"Conference Date", False),
    (u"DE", u"Author Keywords", True),
    (u"DI", u"Digital Object Identifier (DOI)", False),
    (u"DT", u"Document Type", False),
    (u"D2", u"D2", False),  # Unknown
    (u"ED", u"Editors", False),
    (u"EF", u"End of File", False),
    (u"EM", u"E-mail Address", True),
    (u"EP", u"Ending Page", False),
    (u"ER", u"End of Record", False),
    (u"FU", u"Funding Agency and Grant Number", False),
    (u"FX", u"Funding Text", False),
    (u"GA", u"Document Delivery Number", False),
    (u"GP", u"GP", False),  # unknown
    (u"HO", u"Conference Host", False),
    (u"ID", u"Keywords Plus", True),
    (u"IS", u"Issue", False),
    (u"J9", u"29-Character Source Abbreviation", False),
    (u"JI", u"ISO Source Abbreviation", False),
    (u"LA", u"Language", False),
    (u"NR", u"Cited Reference Count", False),
    (u"PA", u"Publisher Address", False),
    (u"PD", u"Publication Date", False),
    (u"PG", u"Page Count", False),
    (u"PI", u"Publisher City", False),
    (u"PN", u"Part Number", False),
    (u"PT", u"Publication type", False),
    (u"PU", u"Publisher", False),
    (u"PY", u"Year Published", False),
    (u"P2", u"P2", False),  # Unknown
    (u"RI", u"RI", False),  # Unknown
    (u"RP", u"Re Address", False),
    (u"SC", u"Subject Category", True),
    (u"SE", u"Book Series Title", False),
    (u"SI", u"Special Issue", False),
    (u"SN", u"ISSN", False),
    (u"SO", u"Publication Name", False),
    (u"SP", u"Conference Sponsors", False),
    (u"SU", u"Supplement", False),
    (u"TC", u"Times Cited", False),
    (u"TI", u"Document Title", False),
    (u"UT", u"Unique Article Identifier", False),
    (u"VL", u"Volume", False),
    (u"WC", u"Web of Science Category", True),
    (u"Z9", u"Z9", False)  # unknown
)
heading_dict = {abbr: full for abbr, full, _ in headings}
is_iterable = {abbr: iterable for abbr, _, iterable in headings}


class Record(dict):
    def __init__(self, wos_data, subdelimiter="; ", skip_empty=True):
        """Create a record based on *wos_data*

        :param dict wos_data: a WoS record
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)
        :param bool skip_empty: whether or not to skip empty fields

        """
        self.parse(wos_data)

    def parse(self, wos_data, subdelimiter="; ", skip_empty=True):
        """Parse *wos_data* into more structured format

        :param dict wos_data: a WoS record
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)
        :param bool skip_empty: whether or not to skip empty fields

        """
        self.clear()
        for k, v in wos_data.iteritems():
            if skip_empty and not v:
                continue
            # Since WoS files have a spurious tab at the end of each line, we
            # may get a 'ghost' None key, which is also ignored.
            if k is None:
                continue
            if is_iterable[k]:
                v = v.split(subdelimiter)
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
        reader = DictReader(f, delimiter=delimiter, **kwargs)
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
