import codecs
import logging

from .tags import has_item_per_line
from .unicodecsv import DictReader

logger = logging.getLogger(__name__)


class ReadError(Exception):
    pass


def utf8_file(fh):
    """Make sure that fh is a UTF-8 encoded file

    :param fh: Opened file object
    :type fh: file object
    :return: The file object, recoded to UTF-8

    """
    encoding = 'utf-8'
    recoder = lambda fh, from_encoding, to_encoding: \
        codecs.StreamRecoder(fh, codecs.getencoder(to_encoding),
                             codecs.getdecoder(to_encoding),
                             codecs.getreader(from_encoding),
                             codecs.getwriter(to_encoding))

    sniff = fh.read(10)

    if sniff.startswith(codecs.BOM_UTF16_LE):
        logger.debug("File '%s' encoded as UTF-16-LE" % fh)
        fh.seek(len(codecs.BOM_UTF16_LE))
        return recoder(fh, 'utf-16-le', encoding)

    if sniff.startswith(codecs.BOM_UTF16_BE):
        logger.debug("File '%s' encoded as UTF-16-BE" % fh)
        fh.seek(len(codecs.BOM_UTF16_BE))
        return recoder(fh, 'utf-16-be', encoding)

    if sniff.startswith(codecs.BOM_UTF8):
        logger.debug("File '%s' encoded as UTF-8 with BOM" % fh)
        fh.seek(len(codecs.BOM_UTF8))
        return fh

    # WoS exports are always(?) UTF-8 or UTF-16
    logger.debug("File '%s' encoded as UTF-8 without BOM" % fh)
    fh.seek(0)
    return fh


def get_reader(fh):
    """Get appropriate reader for the file type of *fh*"""
    sniff = fh.seek(10)

    if sniff.startswith(u"FN "):
        reader = PlainTextReader
    elif u"\t" in sniff:
        reader = TabDelimitedReader
    else:
        raise ReadError(u"Could not determine appropriate reader for file "
                        "{}".format(fh))
    # Go back to initial position
    fh.seek(-10, 1)
    return reader


def read(fobj, reader=None, **kwargs):
    """Read WoS CSV file recoding (if necessary) to UTF-8

    :param fobj: WoS CSV file name or handle
    :type fobj: str or file
    :return:
        iterator over records in *fobj*, where each record is a field code -
        value dict

    """
    # Make sure we have a file and not a file name
    if not hasattr(fobj, 'read'):
        fh = open(fobj)
        close_fh = True
    else:
        fh = fobj
        close_fh = False

    try:
        fh = utf8_file(fh)
        reader = get_reader(fh)(fh, **kwargs)
        for record in reader:
            yield record
    finally:
        if close_fh:
            fh.close()


class TabDelimitedReader(object):

    def __init__(self, fh, **kwargs):
        self.reader = DictReader(utf8_file(fh), delimiter="\t", **kwargs)

    def next(self):
        record = next(self.reader)
        # Since WoS files have a spurious tab at the end of each line, we
        # may get a 'ghost' None key.
        try:
            del record[None]
        except KeyError:
            pass
        return record

    def __iter__(self):
        return self


class PlainTextReader(object):

    def __init__(self, fh, subdelimiter="; "):
        """Create a reader for WoS plain text file *fh*

        :param fh: WoS plain text file
        :type fh: file object
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)

        """
        self.fh = utf8_file(fh)
        self.subdelimiter = unicode(subdelimiter)
        self.version = u"1.0"  # Expected version of WoS plain text format
        self.current_line = 0

        line = self._next_nonempty_line()
        if not line.startswith(u"FN"):
            raise ReadError(u"Unknown file format")

        line = self._next_nonempty_line()
        label, version = line.split()
        if label != u"VR" or version != self.version:
            raise ReadError(u"Unknown version: expected {} "
                            "but got {}".format(self.version, version))

    def _next_line(self):
        """Get next line as Unicode"""
        self.current_line += 1
        return self.fh.readline().decode("utf-8").rstrip(u"\n")

    def _next_nonempty_line(self):
        """Get next line that is not empty"""
        line = u""
        while not line:
            line = self._next_line()
        return line

    def _next_record_lines(self):
        """Gather lines that belong to one record"""
        lines = []
        while True:
            line = self._next_nonempty_line()
            if line.startswith(u"EF"):
                if lines:  # We're in the middle of a record!
                    raise ReadError(
                        u"Encountered unexpected end of file marker EF on "
                        "line {}".format(self.current_line))
                else:  # End of file
                    raise StopIteration
            if line.startswith(u"ER"):  # end of record
                return lines
            else:
                lines.append(line)

    def _format_values(self, heading, values):
        if has_item_per_line[heading]:  # Iterable field with one item per line
            return self.subdelimiter.join(values)
        else:
            return u" ".join(values)

    def next(self):
        record = {}
        values = []
        heading = u""
        lines = self._next_record_lines()

        # Parse record, this is mostly handling multi-line fields
        for line in lines:
            if not line.startswith(u"  "):  # new field
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

    def __iter__(self):
        return self
