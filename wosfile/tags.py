# Source: https://webofscience.help.clarivate.com/en-us/Content/export-records.htm
# Format: (Abbreviation, Full label, Iterable?, One item per line?)
# - Abbreviation: WoS field tag
# - Full label: full label as provided by Thomson Reuters (or abbreviation if
#   not available)
# - Splittable: whether or not the field should be split into multiple items
# - One item per line: whether or not each item in an iterable field appears on
#   a new line in WoS plain text format
# Only the tags from the Web of Science core collection have been checked in terms of
# the last two fields. The others are marked with a comment as unchecked.
tags = (
    ("A2", "Other Abstract", False, False),  # unchecked
    ("AA", "Additional Authors", False, False),  # unchecked
    ("AB", "Abstract / BHTD Critical Abstract", False, False),
    ("AD", "Application Details and Date", False, False),  # unchecked
    ("AE", "Patent Assignee", False, False),  # unchecked
    ("AF", "Author Full Names", True, True),
    ("AK", "Abstract (Korean)", False, False),  # unchecked
    ("AN", "Accession Number or PubMedID", False, False),  # unchecked
    ("AR", "Article Number", False, False),
    ("AU", "Authors or Inventors", True, True),
    ("AW", "Item URL", False, False),  # unchecked
    ("BA", "Book Authors", True, True),
    ("BD", "Broad Descriptors or Broad Terms", False, False),  # unchecked
    ("BE", "Book Editor", True, True),
    ("BF", "Book Author Full Names", True, True),
    ("BN", "ISBN", False, False),
    ("BP", "Start Page", False, False),
    ("BS", "Book Series Subtitle", False, False),
    ("C1", "Addresses", False, True),
    ("C2", "Address (non-English)", False, False),  # unchecked
    ("C3", "Author Affiliations", True, False),
    ("CA", "Group Authors", False, False),
    ("CC", "Concept Codes or CABI Codes", False, False),  # unchecked
    ("CE", "Edition", False, False),  # unchecked
    ("CH", "Chemicals & Biochemicals", False, False),  # unchecked
    ("CI", "Derwent Compound Number", False, False),  # unchecked
    ("CL", "Conference Location", False, False),
    ("CN", "CAS Registry Numbers; Commercial Names; Chemical", False, False),  # unchecked
    ("CO", "CODEN", False, False),  # unchecked
    ("CP", "Cited Patent(s)", False, False),  # unchecked
    ("CR", "Cited References", True, True),
    ("CT", "Conference Title", False, False),
    ("CY", "Conference Date", False, False),
    ("D2", "Book DOI", False, False),
    ("DA", "Date of Export", False, False),
    ("DC", "Derwent Class Code(s)", False, False),  # unchecked
    ("DE", "Author Keywords; Descriptors", True, False),
    ("DF", "Date Filed or Submitted", False, False),  # unchecked
    ("DI", "DOI", False, False),
    ("DL", "DOI Link", False, False),  # unchecked
    ("DM", "Demography", False, False),  # unchecked
    ("DN", "DCR Number", False, False),  # unchecked
    ("DP", "Discipline; Diseases", False, False),  # unchecked
    ("DS", "Designated States", False, False),  # unchecked
    ("DT", "Document Type", False, False),
    ("DY", "Data Type", False, False),  # unchecked
    ("EA", "Early access date; Equivalent Abstract, Editor Address", False, False),
    ("EC", "Category", False, False),  # unchecked
    ("ED", "Editors", False, False),
    ("EF", "End of File", False, False),  # unchecked
    ("EI", "eISSN", False, False),
    ("EM", "E-mail Address", True, False),
    ("EP", "End Page", False, False),
    ("ER", "End of Record", False, False),  # unchecked
    ("EY", "Early access year", False, False),
    ("FD", "Further Application Details", False, False),  # unchecked
    ("FN", "File Name", False, False),  # unchecked
    ("FP", "Funding Name Preferred", False, False),  # unchecked
    ("FS", "Field of Search", False, False),  # unchecked
    ("FT", "Foreign Title", False, False),  # unchecked
    ("FU", "Funding Orgs", False, False),
    ("FX", "Funding Text", False, False),
    ("GA", "IDS Number", False, False),
    ("GE", "Geographic Data", False, False),  # unchecked
    ("GI", "Grant Information", False, False),  # unchecked
    ("GN", "Gene Name", False, False),  # unchecked
    ("GP", "Group Authors", False, False),
    ("GS", "Geospatial", False, False),  # unchecked
    ("GT", "Time", False, False),  # unchecked
    ("HC", "Highly Cited Status", False, False),
    ("HO", "Conference Host", False, False),
    ("HP", "Hot Paper Status", False, False),
    ("ID", "Keywords; Identifying Codes", True, False),
    ("IO", "Issuing Organization", False, False),  # unchecked
    ("IP", "International Patent Classification", False, False),  # unchecked
    ("IS", "Issue", False, False),
    ("IV", "Investigators", False, False),  # unchecked
    ("J9", "Journal Abbreviation", False, False),
    ("JC", "NLM Unique ID", False, False),  # unchecked
    ("JI", "Journal ISO Abbreviation", False, False),
    ("LA", "Language", False, False),
    ("LS", "Language of Summary", False, False),  # unchecked
    ("LT", "Literature Type", False, False),  # unchecked
    ("MA", "Meeting Abstract", False, False),
    ("MC", "Major Concepts or Derwent Manual Code(s)", False, False),  # unchecked
    ("ME", "Medium", False, False),  # unchecked
    ("MH", "MeSH Terms", False, False),  # unchecked
    ("MI", "Miscellaneous Descriptors", False, False),  # unchecked
    ("MN", "Markush Number", False, False),  # unchecked
    ("MQ", "Methods & Equipment", False, False),  # unchecked
    ("NM", "Personal Name Subject", False, False),  # unchecked
    ("NO", "Comments, Corrections, Erratum", False, False),  # unchecked
    ("NP", "Named Person", False, False),  # unchecked
    ("NR", "Cited Reference Count", False, False),
    ("NT", "Notes", False, False),  # unchecked
    ("OA", "Open Access Designations", False, False),
    ("OB", "Record Owner", False, False),  # unchecked
    ("OC", "Country of Original Patent Application Number", False, False),  # unchecked
    ("OD", "Method", False, False),  # unchecked
    ("OI", "ORCID numbers", True, False),
    ("OP", "Original Patent Application Number", False, False),  # unchecked
    ("OR", "Organism Descriptors; Systematics", False, False),  # unchecked
    ("OS", "Original Source", False, False),  # unchecked
    ("P1", "Part Number", False, False),  # unchecked
    ("P2", "Chapter Count", False, False),
    ("PA", "Publisher Address", False, False),
    ("PC", "Country of Patent", False, False),  # unchecked
    ("PD", "Publication Date; Patent Details", False, False),
    ("PE", "Published Electronically", False, False),  # unchecked
    ("PG", "Number of Pages", False, False),
    ("PI", "Publisher City; Patent Priority Information", False, False),
    ("PM", "PubMedID", False, False),
    ("PN", "Part Number; Patent Number", False, False),
    ("PR", "Parts, Structures & Systems; Price", False, False),  # unchecked
    ("PS", "Pages", False, False),  # unchecked
    ("PT", "Publication Type", False, False),
    ("PU", "Publisher", False, False),
    ("PV", "Place of Publication", False, False),  # unchecked
    ("PY", "Publication Year", False, False),
    ("RC", "Date Created, Date Completed, Date Revised", False, False),  # unchecked
    ("RG", "Derwent Registry Number", False, False),  # unchecked
    ("RI", "ResearcherIDs; Ring Index Number", True, False),
    ("RP", "Reprint Address", False, False),
    ("S1", "Source Title (non-English)", False, False),  # unchecked
    ("SA", "Status", False, False),  # unchecked
    ("SC", "Research Areas", True, False),
    ("SD", "Molecular Sequence Data", False, False),  # unchecked
    ("SE", "Book Series Title; Series", False, False),
    ("SF", "Space Flight Mission", False, False),  # unchecked
    ("SI", "Special Issue", False, False),
    ("SN", "ISSN", False, False),
    ("SO", "Source Title", False, False),
    ("SP", "Conference Sponsors", False, False),
    ("SS", "FSTA Section/Subsection; Citation Subset", False, False),  # unchecked
    ("ST", "Super Taxa", False, False),  # unchecked
    ("SU", "Supplement; Research Area", False, False),
    ("TA", "Taxonomic Data", False, False),  # unchecked
    ("TC", "Times Cited Count", False, False),
    ("TF", "Technology Focus Abstract", False, False),  # unchecked
    ("TI", "Article Title", False, False),
    ("TL", "Country of Translation", False, False),  # unchecked
    ("TM", "Geologic Time Data", False, False),  # unchecked
    ("TN", "Taxa Notes", False, False),  # unchecked
    ("TR", "Translators", False, False),  # unchecked
    ("TS", "Translated Source", False, False),  # unchecked
    ("U1", "180 Day Usage Count", False, False),
    ("U2", "Since 2013 Usage Count", False, False),
    ("UC", "Document Selection URL", False, False),  # unchecked
    ("UR", "URL", False, False),  # unchecked
    ("UT", "Accession Number", False, False),
    ("VL", "Volume", False, False),
    ("VN", "Version", False, False),  # unchecked
    ("VR", "Version Number", False, False),  # unchecked
    ("WC", "Web of Science Subject Categories", True, False),
    ("WE", "Web of Science Index", True, False),
    ("WP", "Publisher Web Address", False, False),  # unchecked
    ("X1", "Article Title (non-English)", False, False),  # unchecked
    ("X2", "Article Title (Transliterated)", False, False),  # unchecked
    ("X4", "Spanish Abstract", False, False),  # unchecked
    ("X5", "Spanish Author Keywords", False, False),  # unchecked
    ("Y1", "Portuguese Document Title", False, False),  # unchecked
    ("Y4", "Portuguese Abstract", False, False),  # unchecked
    ("Y5", "Author Keywords (non-English); Portuguese Author Keywords", False, False),  # unchecked
    ("Z1", "Article Title (Other Languages)", False, False),  # unchecked
    ("Z2", "Authors (non-English)", False, False),  # unchecked
    ("Z3", "Publication Name (Chinese)", False, False),  # unchecked
    ("Z4", "Abstract (non-English)", False, False),  # unchecked
    ("Z5", "Author Keywords (non-English)", False, False),  # unchecked
    ("Z6", "Author Address (non-English)", False, False),  # unchecked
    ("Z7", "E-mail Address (non-English)", False, False),  # unchecked
    ("Z8", "CSCD Times Cited Count", False, False),  # unchecked
    ("Z9", "Times Cited, All Databases", False, False),
    ("ZK", "Author Keywords (Korean)", False, False),  # unchecked
)
is_splittable = {abbr: iterable for abbr, _, iterable, _ in tags}
has_item_per_line = {abbr: item_per_line for abbr, _, _, item_per_line in tags}
