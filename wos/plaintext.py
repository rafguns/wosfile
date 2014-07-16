from .tags import has_item_per_line


class ReaderError(Exception):
    pass


class PlainTextReader(object):

    def __init__(self, fh, encoding="utf-8", subdelimiter="; "):
        """Create a reader for WoS plain text file *fh*

        :param fh: WoS plain text file
        :type fh: file object
        :param str encoding: Encoding of file *fh*
        :param str subdelimiter:
            string delimiting different parts of a multi-part field,
            like author(s)

        """
        self.fh = fh
        self.encoding = encoding
        self.subdelimiter = unicode(subdelimiter)
        self.version = u"1.0"  # Expected version of WoS plain text format
        self.current_line = 0

        line = self._next_nonempty_line()
        if not line.startswith(u"FN"):
            raise ReaderError(u"Unknown file format")

        line = self._next_nonempty_line()
        label, version = line.split()
        if label != u"VR" or version != self.version:
            raise ReaderError(u"Unknown version: expected {} "
                              "but got {}".format(self.version, version))

    def _next_line(self):
        """Get next line as Unicode"""
        self.current_line += 1
        return self.fh.readline().decode(self.encoding).rstrip(u"\n")

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
                    raise ReaderError(
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
