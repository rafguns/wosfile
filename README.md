wos
===

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
