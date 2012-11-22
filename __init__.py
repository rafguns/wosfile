import csv
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
        (u"BA", u"BA", False), # Unknown
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
        (u"D2", u"D2", False), # Unknown
        (u"ED", u"Editors", False),
        (u"EF", u"End of File", False),
        (u"EM", u"E-mail Address", True),
        (u"EP", u"Ending Page", False),
        (u"ER", u"End of Record", False),
        (u"FU", u"Funding Agency and Grant Number", False),
        (u"FX", u"Funding Text", False),
        (u"GA", u"Document Delivery Number", False),
        (u"GP", u"GP", False), # unknown
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
        (u"P2", u"P2", False), # Unknown
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
        (u"Z9", u"Z9", False) # unknown
)
heading_dict = dict((abbr, full) for abbr, full, _ in headings)
is_iterable  = dict((abbr, iterable) for abbr, _, iterable in headings)

def utf8_file(f):
    """Make sure that f is a UTF-8 encoded file"""

    encoding = 'utf-8'
    recoder = lambda f, from_encoding, to_encoding : \
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
    
    logger.debug("File '%s' encoded as UTF-8 without BOM" % f.name)
    f.seek(0)
    return f

def read(fobj, delimiter="\t", quoting=csv.QUOTE_NONE, **kwargs):
    """
    Read WoS CSV file recoding (if necessary) to UTF-8
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
        reader = DictReader(f, delimiter=delimiter, quoting=quoting, **kwargs)
        for record in reader:
            yield record
    finally:
        if close_f:
            f.close()

def get_id(rec):
    import re

    first_author = re.sub(r'(.*), (.*)', r'\1 \2', rec[u"AU"][0])
    year         = rec[u"PY"]
    journal      = rec.get(u"J9", rec.get(u"BS", rec.get(u"SO")))
    volume       = u"V" + rec[u"VL"] if u"VL" in rec else None
    page         = u"P" + rec[u"BP"] if u"BP" in rec else None
    doi          = u"DOI " + rec[u"DI"] if u"DI" in rec else None

    itemlist = [item for item in (first_author, year, journal, volume, page, doi)\
                if item]
    return u", ".join(itemlist)

def parse(rec, delimiter="; ", full_labels=False, skip_empty=True):
    parsed_rec = {}

    for k, v in rec.iteritems():
        if skip_empty and not v:
            continue
        # Since WoS files have a spurious tab at the end of each line, we may
        # get a 'ghost' None key, which is also ignored. 
        if k is None:
            continue
        if is_iterable[k]:
            v = v.split(delimiter)
        if full_labels:
            k = heading_dict[k]
        parsed_rec[k] = v

    rec_id = get_id(parsed_rec)

    return rec_id, parsed_rec

def read_parse(fobj, subdelimiter="; ", full_labels=False,
               skip_empty=True, **kwargs):
    for rec in read(fobj, **kwargs):
        yield parse(rec, subdelimiter, full_labels, skip_empty)
