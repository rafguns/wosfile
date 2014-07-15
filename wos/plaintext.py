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
        self.subdelimiter = subdelimiter
        self.version = "1.0"  # Expected version of WoS plain text format
        self.current_line = 0

        line = self._next_line()
        if not line.startswith(u"FN"):
            raise ReaderError(u"Unknown file format")

        line = self._next_line()
        label, version = line.split()
        if label != u"VR" or version != self.version:
            raise ReaderError(u"Unknown version: expected {} "
                              "but got {}".format(self.version, version))

    def _next_line(self):
        """Get next line as Unicode"""
        self.current_line += 1
        return self.fh.readline().decode(self.encoding).rstrip(u"\n")

    def _next_record_lines(self):
        """Gather lines that belong to one record"""
        lines = []
        while True:
            line = self._next_line()
            if not line:  # Skip blank lines
                continue
            if line.startswith(u"EF"):
                if lines:  # We're in the middle of a record!
                    raise ReaderError(
                        u"Encountered unexpected end of file marker EF on "
                        "line {}".format(self.current_line))
                else:  # End of file
                    raise StopIteration
            if not line.startswith(u"ER"):
                lines.append(line)
            else:
                return lines

    def next(self):
        record = {}
        values = []
        heading = u""
        lines = self._next_record_lines()

        # Parse record, this is mostly handling multi-line fields
        for line in lines:
            if not line.startswith(u"  "):
                if heading:
                    # XXX This is too naive: some fields, like FU, should be
                    # joined by a space.
                    record[heading] = self.subdelimiter.join(values)
                heading, v = line.split(None, 1)
                values = [v]
            else:
                values.append(line.strip())

        # Add last field
        record[heading] = self.subdelimiter.join(values)

        return record

    def __iter__(self):
        return self
