# http://images.webofknowledge.com/WOKRS520B4.1/help/WOK/hs_wos_fieldtags.html
# Format: (Abbreviation, Full label, Iterable?, One item per line?)
# - Abbreviation: WoS field tag
# - Full label: full label as provided by Thomson Reuters (or abbreviation if
#   not available)
# - Iterable: whether or not the field may consist of multiple items
# - One item per line: whether or not each item in an iterable field appears on
#   a new line in WoS plain text format
tags = (
    (u"AB", u"Abstract", False, False),
    (u"AF", u"Author Full Name", True, True),
    (u"AR", u"Article Number", False, False),
    (u"AU", u"Authors", True, True),
    (u"BA", u"Book Authors", True, True),  # Correct?
    (u"BE", u"Editors", True, True),
    (u"BF", u"Book Authors Full Name", True, True),  # Correct?
    (u"BN", u"International Standard Book Number (ISBN)", False, False),
    (u"BP", u"Beginning Page", False, False),
    (u"BS", u"Book Series Subtitle", False, False),
    (u"C1", u"Author Address", True, True),
    (u"CA", u"Group Authors", False, False),
    (u"CL", u"Conference Location", False, False),
    (u"CR", u"Cited References", True, True),
    (u"CT", u"Conference Title", False, False),
    (u"CY", u"Conference Date", False, False),
    (u"CL", u"Conference Location", False, False),
    (u"DE", u"Author Keywords", True, False),
    (u"DI", u"Digital Object Identifier (DOI)", False, False),
    (u"DT", u"Document Type", False, False),
    (u"D2", u"Book Digital Object Identifier (DOI)", False, False),
    (u"ED", u"Editors", False, False),
    (u"EM", u"E-mail Address", True, False),
    (u"EI", u"Electronic International Standard Serial Number "
            "(eISSN)", False, False),
    (u"EP", u"Ending Page", False, False),
    (u"FU", u"Funding Agency and Grant Number", False, False),
    (u"FX", u"Funding Text", False, False),
    (u"GA", u"Document Delivery Number", False, False),
    (u"GP", u"Book Group Authors", False, False),
    (u"HO", u"Conference Host", False, False),
    (u"ID", u"Keywords Plus", True, False),
    (u"IS", u"Issue", False, False),
    (u"J9", u"29-Character Source Abbreviation", False, False),
    (u"JI", u"ISO Source Abbreviation", False, False),
    (u"LA", u"Language", False, False),
    (u"MA", u"Meeting Abstract", False, False),
    (u"NR", u"Cited Reference Count", False, False),
    (u"OI", u"ORCID Identifier "
            "(Open Researcher and Contributor ID)", True, False),
    (u"P2", u"Chapter count (Book Citation Index)", False, False),
    (u"PA", u"Publisher Address", False, False),
    (u"PD", u"Publication Date", False, False),
    (u"PG", u"Page Count", False, False),
    (u"PI", u"Publisher City", False, False),
    (u"PM", u"PubMed ID", False, False),
    (u"PN", u"Part Number", False, False),
    (u"PT", u"Publication Type "
            "(J=Journal; B=Book; S=Series; P=Patent)", False, False),
    (u"PU", u"Publisher", False, False),
    (u"PY", u"Year Published", False, False),
    (u"RI", u"ResearcherID Number", True, False),
    (u"RP", u"Reprint Address", False, False),
    (u"SC", u"Research Areas", True, False),
    (u"SE", u"Book Series Title", False, False),
    (u"SI", u"Special Issue", False, False),
    (u"SN", u"International Standard Serial Number (ISSN)", False, False),
    (u"SO", u"Publication Name", False, False),
    (u"SP", u"Conference Sponsors", False, False),
    (u"SU", u"Supplement", False, False),
    (u"TC", u"Web of Science Core Collection Times Cited Count", False, False),
    (u"TI", u"Document Title", False, False),
    (u"U1", u"Usage Count (Last 180 Days)", False, False),
    (u"U2", u"Usage Count (Since 2013)", False, False),
    (u"UT", u"Unique Article Identifier", False, False),
    (u"VL", u"Volume", False, False),
    (u"WC", u"Web of Science Categories", True, False),
    (u"Z9", u"Total Times Cited Count (WoS Core, BCI, and CSCD)", False, False)
)
is_iterable = {abbr: iterable for abbr, _, iterable, _ in tags}
has_item_per_line = {abbr: item_per_line for abbr, _, _, item_per_line in tags}
