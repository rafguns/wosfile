import codecs
import csv

# Based on http://images.webofknowledge.com/WOK46/help/WOS/h_fieldtags.html
# Format: (Abbreviation, Full label, Iterable?)
headings = (
        ("AB", "Abstract", False),
        ("AF", "Author Full Name", True),
        ("AR", "Article Number", False),
        ("AU", "Authors", True),
        ("BA", "BA", False), # Unknown
        ("BE", "Book Editors", True),
        ("BN", "ISBN", False),
        ("BP", "Beginning Page", False),
        ("BS", "Book Series Subtitle", False),
        ("C1", "Author Address", True),
        ("CA", "Group Authors", False),
        ("CL", "Conference Location", False),
        ("CR", "Cited References", True),
        ("CT", "Conference Title", False),
        ("CY", "Conference Date", False),
        ("DE", "Author Keywords", True),
        ("DI", "Digital Object Identifier (DOI)", False),
        ("DT", "Document Type", False),
        ("D2", "D2", False), # Unknown
        ("ED", "Editors", False),
        ("EF", "End of File", False),
        ("EM", "E-mail Address", True),
        ("EP", "Ending Page", False),
        ("ER", "End of Record", False),
        ("FU", "Funding Agency and Grant Number", False),
        ("FX", "Funding Text", False),
        ("GA", "Document Delivery Number", False),
        ("GP", "GP", False), # unknown
        ("HO", "Conference Host", False),
        ("ID", "Keywords Plus", True),
        ("IS", "Issue", False),
        ("J9", "29-Character Source Abbreviation", False),
        ("JI", "ISO Source Abbreviation", False),
        ("LA", "Language", False),
        ("NR", "Cited Reference Count", False),
        ("PA", "Publisher Address", False),
        ("PD", "Publication Date", False),
        ("PG", "Page Count", False),
        ("PI", "Publisher City", False),
        ("PN", "Part Number", False),
        ("PT", "Publication type", False),
        ("PU", "Publisher", False),
        ("PY", "Year Published", False),
        ("P2", "P2", False), # Unknown
        ("RP", "Reprint Address", False),
        ("SC", "Subject Category", True),
        ("SE", "Book Series Title", False),
        ("SI", "Special Issue", False),
        ("SN", "ISSN", False),
        ("SO", "Publication Name", False),
        ("SP", "Conference Sponsors", False),
        ("SU", "Supplement", False),
        ("TC", "Times Cited", False),
        ("TI", "Document Title", False),
        ("UT", "Unique Article Identifier", False),
        ("VL", "Volume", False),
        ("WC", "Web of Science Category", True),
        ("Z9", "Z9", False) # unknown
)
heading_dict = dict((abbr, full) for abbr, full, _ in headings)
is_iterable  = dict((abbr, iterable) for abbr, _, iterable in headings)

def read_file(fname, encoding="utf-8-sig", delimiter="\t", **kwargs):
    with codecs.open(fname, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter, **kwargs)
        for record in reader:
            yield record

def get_id(rec):
    import re

    first_author = re.sub(r'(.*), (.*)', r'\1 \2', rec["AU"][0])
    year         = rec["PY"]
    journal      = rec.get("J9", rec.get("BS", rec.get("SO")))
    volume       = "V" + rec["VL"] if "VL" in rec else None
    page         = "P" + rec["BP"] if "BP" in rec else None
    doi          = "DOI " + rec["DI"] if "DI" in rec else None

    itemlist = [item for item in (first_author, year, journal, volume, page, doi)\
                if item]
    return ", ".join(itemlist)

def parse_record(rec, delimiter="; ", full_labels=True, skip_empty=True):
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
        #if full_labels:
        #    k = heading_dict[k]
        parsed_rec[k] = v

    rec_id = get_id(parsed_rec)

    return rec_id, parsed_rec

def read_parse_file(fname, encoding="utf-8-sig", delimiter="\t",
                        subdelimiter="; ", full_labels=False, skip_empty=True,
                        **kwargs):
    for rec in read_file(fname, encoding, delimiter, **kwargs):
        yield parse_record(rec, subdelimiter, full_labels, skip_empty)
