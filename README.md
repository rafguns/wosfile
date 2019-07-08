# wos

[![Build Status](https://travis-ci.org/rafguns/wos.svg?branch=master)](https://travis-ci.org/rafguns/wos)
[![Coverage Status](https://coveralls.io/repos/rafguns/wos/badge.svg?branch=master&service=github)](https://coveralls.io/github/rafguns/wos?branch=master)

**wos** is a Python package designed to read and handle data exported from Thomson Reuters Web of Science™. It supports both tab-delimited files and so-called 'plain text' files.

Pros:
* It has no requirements beyond Python 3.6+ and the standard library.
* Completely iterator-based, so useful for working with large datasets. At no point should we ever have more than one single record in memory.
* Simple API: usually one needs just one function `wos.read()`.

Cons:
* Pure Python, so might be slow.
* At the moment, **wos** does little more than reading WoS files and generating *Record* objects for each record. While it does some niceties like parsing address fields, it does not have any analysis functionality.

## Comparison to other Python packages

When I srtaed developing this package, I did not immediately find any similar Python packages. That has changed. Here's a brief set of notes on related packages that can be found on PyPI:

* [wos](https://pypi.org/project/wos/) is different in scope, since it is a client for the Web of Science search API.
* [wosclient](https://pypi.org/project/wosclient/) is different in scope, since it is a client for the Web of Science search API.
* [WOS+](https://pypi.org/project/WOSplus/):
    * reads Excel and WoS plaintext files?
    * has a lot of code for stuff I don't really udnerstand, e.g. to handle files in Google Drive etc.
    * according to the README also handles Scopus, Scielo...
* [metaknowledge](https://pypi.org/project/metaknowledge/)
    * handles many different sources (WoS, Scopus, Pubmed etc.)
    * uses camelCase :-/
    * functionality for (co-)citation networks, etc.
    * maybe most mature package, albeit with some technical debt, it seems
* [wostools](https://pypi.org/project/wostools/) is closest to my own taste in coding style
    * lazy evaluation of WoS files
    * only WoS plain text?
* [pywos](https://pypi.org/project/pywos/)
    * or is it called [wos-statistics](https://github.com/refraction-ray/wos-statistics)?
    * queries the web interface and parses results!
    * async!

Questions:
* char encoding handling?
* handling of addresses (+address-author coupling)?
* 

 
