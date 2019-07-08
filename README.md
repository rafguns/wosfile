# wosfile

[![Build Status](https://travis-ci.org/rafguns/wosfile.svg?branch=master)](https://travis-ci.org/rafguns/wosfile)
[![Coverage Status](https://coveralls.io/repos/rafguns/wosfile/badge.svg?branch=master&service=github)](https://coveralls.io/github/rafguns/wosfile?branch=master)

**wosfile** is a Python package designed to read and handle data exported from Thomson Reuters Web of Science™. It supports both tab-delimited files and so-called 'plain text' files.

Pros:
* It has no requirements beyond Python 3.6+ and the standard library.
* Completely iterator-based, so useful for working with large datasets. At no point should we ever have more than one single record in memory.
* Simple API: usually one needs just one function `wosfile.records_from()`.

Cons:
* Pure Python, so might be slow.
* At the moment, wosfile does little more than reading WoS files and generating *Record* objects for each record. While it does some niceties like parsing address fields, it does not have any analysis functionality.

## Other Python packages

The following packages also read WoS files (+ sometimes much more):
* [WOS+](https://pypi.org/project/WOSplus/)
* [metaknowledge](https://pypi.org/project/metaknowledge/)
* [wostools](https://pypi.org/project/wostools/)

Other packages query WoS directly through the API and/or by scraping the web interface:
* [pywos](https://pypi.org/project/pywos/) (elsewhere called [wos-statistics](https://github.com/refraction-ray/wos-statistics))
* [wos](https://pypi.org/project/wos/)
* [wosclient](https://pypi.org/project/wosclient/)
