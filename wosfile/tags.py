# ruff: noqa: E501
import warnings
from typing import NamedTuple


class Tag(NamedTuple):
    abbrev: str
    full_label: str
    splittable: bool
    one_item_per_line: bool

# Source: https://web.archive.org/web/20241208031254/https://webofscience.help.clarivate.com/en-us/Content/export-records.htm
# Only the tags from the Web of Science core collection have been checked in terms of
# the last two fields. The others are marked with a comment as unchecked.
tags = [
    Tag("A2", "Other Abstract", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AA", "Additional Authors", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AB", "Abstract / BHTD Critical Abstract", splittable=False, one_item_per_line=False),
    Tag("AD", "Application Details and Date", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AE", "Patent Assignee", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AF", "Author Full Names", splittable=True, one_item_per_line=True),
    Tag("AK", "Abstract (Korean)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AN", "Accession Number or PubMedID", splittable=False, one_item_per_line=False),  # unchecked
    Tag("AR", "Article Number", splittable=False, one_item_per_line=False),
    Tag("AU", "Authors or Inventors", splittable=True, one_item_per_line=True),
    Tag("AW", "Item URL", splittable=False, one_item_per_line=False),  # unchecked
    Tag("BA", "Book Authors", splittable=True, one_item_per_line=True),
    Tag("BD", "Broad Descriptors or Broad Terms", splittable=False, one_item_per_line=False),  # unchecked
    Tag("BE", "Book Editor", splittable=True, one_item_per_line=True),
    Tag("BF", "Book Author Full Names", splittable=True, one_item_per_line=True),
    Tag("BN", "ISBN", splittable=False, one_item_per_line=False),
    Tag("BP", "Start Page", splittable=False, one_item_per_line=False),
    Tag("BS", "Book Series Subtitle", splittable=False, one_item_per_line=False),
    Tag("C1", "Addresses", splittable=False, one_item_per_line=True),
    Tag("C2", "Address (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("C3", "Author Affiliations", splittable=True, one_item_per_line=False),
    Tag("CA", "Group Authors", splittable=False, one_item_per_line=False),
    Tag("CC", "Concept Codes or CABI Codes", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CE", "Edition", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CH", "Chemicals & Biochemicals", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CI", "Derwent Compound Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CL", "Conference Location", splittable=False, one_item_per_line=False),
    Tag("CN", "CAS Registry Numbers; Commercial Names; Chemical", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CO", "CODEN", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CP", "Cited Patent(s)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("CR", "Cited References", splittable=True, one_item_per_line=True),
    Tag("CT", "Conference Title", splittable=False, one_item_per_line=False),
    Tag("CY", "Conference Date", splittable=False, one_item_per_line=False),
    Tag("D2", "Book DOI", splittable=False, one_item_per_line=False),
    Tag("DA", "Date of Export", splittable=False, one_item_per_line=False),
    Tag("DC", "Derwent Class Code(s)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DE", "Author Keywords; Descriptors", splittable=True, one_item_per_line=False),
    Tag("DF", "Date Filed or Submitted", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DI", "DOI", splittable=False, one_item_per_line=False),
    Tag("DL", "DOI Link", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DM", "Demography", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DN", "DCR Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DP", "Discipline; Diseases", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DS", "Designated States", splittable=False, one_item_per_line=False),  # unchecked
    Tag("DT", "Document Type", splittable=False, one_item_per_line=False),
    Tag("DY", "Data Type", splittable=False, one_item_per_line=False),  # unchecked
    Tag("EA", "Early access date; Equivalent Abstract, Editor Address", splittable=False, one_item_per_line=False),
    Tag("EC", "Category", splittable=False, one_item_per_line=False),  # unchecked
    Tag("ED", "Editors", splittable=False, one_item_per_line=False),
    Tag("EF", "End of File", splittable=False, one_item_per_line=False),  # unchecked
    Tag("EI", "eISSN", splittable=False, one_item_per_line=False),
    Tag("EM", "E-mail Address", splittable=True, one_item_per_line=False),
    Tag("EP", "End Page", splittable=False, one_item_per_line=False),
    Tag("ER", "End of Record", splittable=False, one_item_per_line=False),  # unchecked
    Tag("EY", "Early access year", splittable=False, one_item_per_line=False),
    Tag("FD", "Further Application Details", splittable=False, one_item_per_line=False),  # unchecked
    Tag("FN", "File Name", splittable=False, one_item_per_line=False),  # unchecked
    Tag("FP", "Funding Name Preferred", splittable=False, one_item_per_line=False),  # unchecked
    Tag("FS", "Field of Search", splittable=False, one_item_per_line=False),  # unchecked
    Tag("FT", "Foreign Title", splittable=False, one_item_per_line=False),  # unchecked
    Tag("FU", "Funding Orgs", splittable=False, one_item_per_line=False),
    Tag("FX", "Funding Text", splittable=False, one_item_per_line=False),
    Tag("GA", "IDS Number", splittable=False, one_item_per_line=False),
    Tag("GE", "Geographic Data", splittable=False, one_item_per_line=False),  # unchecked
    Tag("GI", "Grant Information", splittable=False, one_item_per_line=False),  # unchecked
    Tag("GN", "Gene Name", splittable=False, one_item_per_line=False),  # unchecked
    Tag("GP", "Group Authors", splittable=False, one_item_per_line=False),
    Tag("GS", "Geospatial", splittable=False, one_item_per_line=False),  # unchecked
    Tag("GT", "Time", splittable=False, one_item_per_line=False),  # unchecked
    Tag("HC", "Highly Cited Status", splittable=False, one_item_per_line=False),
    Tag("HO", "Conference Host", splittable=False, one_item_per_line=False),
    Tag("HP", "Hot Paper Status", splittable=False, one_item_per_line=False),
    Tag("ID", "Keywords; Identifying Codes", splittable=True, one_item_per_line=False),
    Tag("IO", "Issuing Organization", splittable=False, one_item_per_line=False),  # unchecked
    Tag("IP", "International Patent Classification", splittable=False, one_item_per_line=False),  # unchecked
    Tag("IS", "Issue", splittable=False, one_item_per_line=False),
    Tag("IV", "Investigators", splittable=False, one_item_per_line=False),  # unchecked
    Tag("J9", "Journal Abbreviation", splittable=False, one_item_per_line=False),
    Tag("JC", "NLM Unique ID", splittable=False, one_item_per_line=False),  # unchecked
    Tag("JI", "Journal ISO Abbreviation", splittable=False, one_item_per_line=False),
    Tag("LA", "Language", splittable=False, one_item_per_line=False),
    Tag("LS", "Language of Summary", splittable=False, one_item_per_line=False),  # unchecked
    Tag("LT", "Literature Type", splittable=False, one_item_per_line=False),  # unchecked
    Tag("MA", "Meeting Abstract", splittable=False, one_item_per_line=False),
    Tag("MC", "Major Concepts or Derwent Manual Code(s)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("ME", "Medium", splittable=False, one_item_per_line=False),  # unchecked
    Tag("MH", "MeSH Terms", splittable=False, one_item_per_line=False),  # unchecked
    Tag("MI", "Miscellaneous Descriptors", splittable=False, one_item_per_line=False),  # unchecked
    Tag("MN", "Markush Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("MQ", "Methods & Equipment", splittable=False, one_item_per_line=False),  # unchecked
    Tag("NM", "Personal Name Subject", splittable=False, one_item_per_line=False),  # unchecked
    Tag("NO", "Comments, Corrections, Erratum", splittable=False, one_item_per_line=False),  # unchecked
    Tag("NP", "Named Person", splittable=False, one_item_per_line=False),  # unchecked
    Tag("NR", "Cited Reference Count", splittable=False, one_item_per_line=False),
    Tag("NT", "Notes", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OA", "Open Access Designations", splittable=False, one_item_per_line=False),
    Tag("OB", "Record Owner", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OC", "Country of Original Patent Application Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OD", "Method", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OI", "ORCID numbers", splittable=True, one_item_per_line=False),
    Tag("OP", "Original Patent Application Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OR", "Organism Descriptors; Systematics", splittable=False, one_item_per_line=False),  # unchecked
    Tag("OS", "Original Source", splittable=False, one_item_per_line=False),  # unchecked
    Tag("P1", "Part Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("P2", "Chapter Count", splittable=False, one_item_per_line=False),
    Tag("PA", "Publisher Address", splittable=False, one_item_per_line=False),
    Tag("PC", "Country of Patent", splittable=False, one_item_per_line=False),  # unchecked
    Tag("PD", "Publication Date; Patent Details", splittable=False, one_item_per_line=False),
    Tag("PE", "Published Electronically", splittable=False, one_item_per_line=False),  # unchecked
    Tag("PG", "Number of Pages", splittable=False, one_item_per_line=False),
    Tag("PI", "Publisher City; Patent Priority Information", splittable=False, one_item_per_line=False),
    Tag("PM", "PubMedID", splittable=False, one_item_per_line=False),
    Tag("PN", "Part Number; Patent Number", splittable=False, one_item_per_line=False),
    Tag("PR", "Parts, Structures & Systems; Price", splittable=False, one_item_per_line=False),  # unchecked
    Tag("PS", "Pages", splittable=False, one_item_per_line=False),  # unchecked
    Tag("PT", "Publication Type", splittable=False, one_item_per_line=False),
    Tag("PU", "Publisher", splittable=False, one_item_per_line=False),
    Tag("PV", "Place of Publication", splittable=False, one_item_per_line=False),  # unchecked
    Tag("PY", "Publication Year", splittable=False, one_item_per_line=False),
    Tag("RC", "Date Created, Date Completed, Date Revised", splittable=False, one_item_per_line=False),  # unchecked
    Tag("RG", "Derwent Registry Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("RI", "ResearcherIDs; Ring Index Number", splittable=True, one_item_per_line=False),
    Tag("RP", "Reprint Address", splittable=False, one_item_per_line=False),
    Tag("S1", "Source Title (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("SA", "Status", splittable=False, one_item_per_line=False),  # unchecked
    Tag("SC", "Research Areas", splittable=True, one_item_per_line=False),
    Tag("SD", "Molecular Sequence Data", splittable=False, one_item_per_line=False),  # unchecked
    Tag("SE", "Book Series Title; Series", splittable=False, one_item_per_line=False),
    Tag("SF", "Space Flight Mission", splittable=False, one_item_per_line=False),  # unchecked
    Tag("SI", "Special Issue", splittable=False, one_item_per_line=False),
    Tag("SN", "ISSN", splittable=False, one_item_per_line=False),
    Tag("SO", "Source Title", splittable=False, one_item_per_line=False),
    Tag("SP", "Conference Sponsors", splittable=False, one_item_per_line=False),
    Tag("SS", "FSTA Section/Subsection; Citation Subset", splittable=False, one_item_per_line=False),  # unchecked
    Tag("ST", "Super Taxa", splittable=False, one_item_per_line=False),  # unchecked
    Tag("SU", "Supplement; Research Area", splittable=False, one_item_per_line=False),
    Tag("TA", "Taxonomic Data", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TC", "Times Cited Count", splittable=False, one_item_per_line=False),
    Tag("TF", "Technology Focus Abstract", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TI", "Article Title", splittable=False, one_item_per_line=False),
    Tag("TL", "Country of Translation", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TM", "Geologic Time Data", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TN", "Taxa Notes", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TR", "Translators", splittable=False, one_item_per_line=False),  # unchecked
    Tag("TS", "Translated Source", splittable=False, one_item_per_line=False),  # unchecked
    Tag("U1", "180 Day Usage Count", splittable=False, one_item_per_line=False),
    Tag("U2", "Since 2013 Usage Count", splittable=False, one_item_per_line=False),
    Tag("UC", "Document Selection URL", splittable=False, one_item_per_line=False),  # unchecked
    Tag("UR", "URL", splittable=False, one_item_per_line=False),  # unchecked
    Tag("UT", "Accession Number", splittable=False, one_item_per_line=False),
    Tag("VL", "Volume", splittable=False, one_item_per_line=False),
    Tag("VN", "Version", splittable=False, one_item_per_line=False),  # unchecked
    Tag("VR", "Version Number", splittable=False, one_item_per_line=False),  # unchecked
    Tag("WC", "Web of Science Subject Categories", splittable=True, one_item_per_line=False),
    Tag("WE", "Web of Science Index", splittable=True, one_item_per_line=False),
    Tag("WP", "Publisher Web Address", splittable=False, one_item_per_line=False),  # unchecked
    Tag("X1", "Article Title (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("X2", "Article Title (Transliterated)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("X4", "Spanish Abstract", splittable=False, one_item_per_line=False),  # unchecked
    Tag("X5", "Spanish Author Keywords", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Y1", "Portuguese Document Title", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Y4", "Portuguese Abstract", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Y5", "Author Keywords (non-English); Portuguese Author Keywords", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z1", "Article Title (Other Languages)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z2", "Authors (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z3", "Publication Name (Chinese)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z4", "Abstract (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z5", "Author Keywords (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z6", "Author Address (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z7", "E-mail Address (non-English)", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z8", "CSCD Times Cited Count", splittable=False, one_item_per_line=False),  # unchecked
    Tag("Z9", "Times Cited, All Databases", splittable=False, one_item_per_line=False),
    Tag("ZK", "Author Keywords (Korean)", splittable=False, one_item_per_line=False),  # unchecked
]
_is_splittable = {abbrev: iterable for abbrev, _, iterable, _ in tags}
_has_item_per_line = {abbrev: item_per_line for abbrev, _, _, item_per_line in tags}


def is_splittable(abbrev: str) -> bool:
    try:
        return _is_splittable[abbrev]
    except KeyError:
        warnings.warn(
            f"Unknown code {abbrev} will be treated as non-splittable", stacklevel=2
        )
        return False


def has_item_per_line(abbrev: str) -> bool:
    try:
        return _has_item_per_line[abbrev]
    except KeyError:
        warnings.warn(
            f"Unknown code {abbrev} will be treated as not having an item per line",
            stacklevel=2
        )
        return False
