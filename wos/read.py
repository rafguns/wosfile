from __future__ import unicode_literals

import codecs
import logging
import sys
# Do we also need unicodecsv for Python 2.7?
from csv import DictReader

if sys.version_info[0] == 2:
    from io import open

from .tags import has_item_per_line

logger = logging.getLogger(__name__)

__all__ = [
    "get_reader",
    "read",
    "PlainTextReader",
    "ReadError",
    "TabDelimitedReader",
]


class ReadError(Exception):
    pass


def sniff_encoding(fh):
    """Guess encoding of file `fh`

    Note that this function is optimized for WoS text files and may yield
    incorrect results for other text files.

    :param fh: File opened in binary mode
    :type fh: file object
    :return: best guess encoding as str

    """
    sniff = fh.read(5)
    fh.seek(0)

    encodings = {codecs.BOM_UTF16_LE: 'utf-16-le',
                 codecs.BOM_UTF16_BE: 'utf-16-be',
                 codecs.BOM_UTF8: 'utf-8-sig'}
    for k, v in encodings.items():
        if sniff.startswith(k):
            return v
    # WoS export files are always(?) either UTF-8 or UTF-16
    return 'utf-8'


def get_reader(fh):
    """Get appropriate reader for the file type of `fh`"""
    sniff = fh.read(10)

    if sniff.startswith("FN "):
        reader = PlainTextReader
    elif "\t" in sniff:
        reader = TabDelimitedReader
    else:
        raise ReadError("Could not determine appropriate reader for file "
                        "{}".format(fh))
    # Go back to initial position
    fh.seek(0)
    return reader


def read(fname, using=None, encoding=None, **kwargs):
    """Read WoS export file ('tab-delimited' or 'plain text')

    :param str fname: name of the WoS export file
    :param using:
        class used for reading `fname`. If None, we try to automatically
        find best reader
    :param str encoding:
        encoding of the file. If None, we try to automatically determine the
        file's encoding
    :return:
        iterator over records in `fname`, where each record is a field code -
        value dict

    """
    if encoding is None:
        with open(fname, 'rb') as fh:
            encoding = sniff_encoding(fh)

    with open(fname, 'rt', encoding=encoding) as fh:
        reader_class = using or get_reader(fh)
        reader = reader_class(fh, **kwargs)
        for record in reader:
            yield record


class TabDelimitedReader(object):

    def __init__(self, fh, **kwargs):
        """Create a reader for tab-delimited file `fh` exported fom WoS

        If you do not know the encoding of a file, the :func:`.read` function
        tries to automatically Do The Right Thing.

        :param fh: WoS tab-delimited file, opened in text mode(!)
        :type fh: file object

        """
        self.reader = DictReader(fh, delimiter="\t", **kwargs)

    def next(self):
        record = next(self.reader)
        # Since WoS files have a spurious tab at the end of each line, we
        # may get a 'ghost' None key.
        try:
            del record[None]
        except KeyError:
            pass
        return record
    __next__ = next

    def __iter__(self):
        return self


class PlainTextReader(object):

    def __init__(self, fh, subdelimiter="; "):
        """Create a reader for WoS plain text file `fh`

        If you do not know the encoding of a file, the :func:`.read` function
        tries to automatically Do The Right Thing.

        :param fh: WoS plain text file, opened in text mode(!)
        :type fh: file object
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)

        """
        self.fh = fh
        self.subdelimiter = subdelimiter
        self.version = "1.0"  # Expected version of WoS plain text format
        self.current_line = 0

        line = self._next_nonempty_line()
        if not line.startswith("FN"):
            raise ReadError("Unknown file format")

        line = self._next_nonempty_line()
        label, version = line.split()
        if label != "VR" or version != self.version:
            raise ReadError("Unknown version: expected {} "
                            "but got {}".format(self.version, version))

    def _next_line(self):
        """Get next line as Unicode"""
        self.current_line += 1
        return next(self.fh).rstrip("\n")

    def _next_nonempty_line(self):
        """Get next line that is not empty"""
        line = ""
        while not line:
            line = self._next_line()
        return line

    def _next_record_lines(self):
        """Gather lines that belong to one record"""
        lines = []
        while True:
            try:
                line = self._next_nonempty_line()
            except StopIteration:
                raise ReadError("Encountered EOF before 'EF' marker")
            if line.startswith("EF"):
                if lines:  # We're in the middle of a record!
                    raise ReadError(
                        "Encountered unexpected end of file marker EF on "
                        "line {}".format(self.current_line))
                else:  # End of file
                    raise StopIteration
            if line.startswith("ER"):  # end of record
                return lines
            else:
                lines.append(line)

    def _format_values(self, heading, values):
        if has_item_per_line[heading]:  # Iterable field with one item per line
            return self.subdelimiter.join(values)
        else:
            return " ".join(values)

    def next(self):
        record = {}
        values = []
        heading = ""
        lines = self._next_record_lines()

        # Parse record, this is mostly handling multi-line fields
        for line in lines:
            if not line.startswith("  "):  # new field
                # Add previous field, if available, to record
                if heading:
                    record[heading] = self._format_values(heading, values)
                heading, v = line.split(None, 1)
                values = [v]
            else:
                values.append(line.strip())

        # Add last field
        record[heading] = self._format_values(heading, values)

        return record
    __next__ = next

    def __iter__(self):
        return self
