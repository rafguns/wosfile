import codecs
import logging
import pathlib
import sys
from csv import DictReader
from typing import (
    AnyStr,
    BinaryIO,
    Dict,
    IO,
    Iterable,
    Iterator,
    List,
    Optional,
    TextIO,
    Type,
    Union,
)

from .tags import has_item_per_line

logger = logging.getLogger(__name__)

__all__ = ["get_reader", "read", "PlainTextReader", "ReadError", "TabDelimitedReader"]

FileName = Union[str, pathlib.Path]


class ReadError(Exception):
    pass


class Reader:
    def __init__(self, fh: TextIO, **kwargs) -> None:
        self.fh = fh

    def __iter__(self):
        return self


def sniff_file(fh: IO[AnyStr], length: int = 10, offset: int = 0) -> AnyStr:
    sniff = fh.read(length)
    fh.seek(offset)

    return sniff


def sniff_encoding(fh: BinaryIO) -> str:
    """Guess encoding of file `fh`

    Note that this function is optimized for WoS text files and may yield
    incorrect results for other text files.

    :param fh: File opened in binary mode
    :return: best guess encoding

    """
    sniff = sniff_file(fh)

    # WoS files typically include a BOM, which we want to strip from the actual
    # data. The encodings 'utf-8-sig' and 'utf-16' do this for UTF-8 and UTF-16
    # respectively. When dealing with files with BOM, avoid the encodings
    # 'utf-8' (which is fine for non-BOM UTF-8), 'utf-16-le', and 'utf-16-be'.
    # See e.g. http://stackoverflow.com/a/8827604
    encodings = {codecs.BOM_UTF16: "utf-16", codecs.BOM_UTF8: "utf-8-sig"}
    for bom, encoding in encodings.items():
        if sniff.startswith(bom):
            return encoding
    # WoS export files are either UTF-8 or UTF-16
    return "utf-8"


def get_reader(fh: TextIO) -> Type[Reader]:
    """Get appropriate reader for the file type of `fh`"""
    sniff = sniff_file(fh)

    if sniff.startswith("FN "):
        return PlainTextReader
    elif "\t" in sniff:
        return TabDelimitedReader
    else:
        # XXX TODO Raised for empty file -- not very elegant
        raise ReadError("Could not determine appropriate reader for file {}".format(fh))


def read(
    fname: Union[FileName, Iterable[FileName]],
    using: Optional[Type[Reader]] = None,
    encoding: str = None,
    **kwargs
) -> Iterator[Dict[str, str]]:
    """Read WoS export file ('tab-delimited' or 'plain text')

    :param fname: name(s) of the WoS export file(s)
    :type fname: str or iterable of strings
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
    if not isinstance(fname, (str, pathlib.Path)):
        # fname is an iterable of file names
        for actual_fname in fname:
            yield from read(actual_fname)

    else:
        if encoding is None:
            with open(fname, "rb") as fh_sniff:
                encoding = sniff_encoding(fh_sniff)

        if using is None:
            with open(fname, encoding=encoding) as fh:
                reader_class = get_reader(fh)
        else:
            reader_class = using

        with open(fname, encoding=encoding) as fh:
            yield from reader_class(fh, **kwargs)


class TabDelimitedReader(Reader):
    def __init__(self, fh: TextIO, **kwargs) -> None:
        """Create a reader for tab-delimited file `fh` exported fom WoS

        If you do not know the encoding of a file, the :func:`.read` function
        tries to automatically Do The Right Thing.

        :param fh: WoS tab-delimited file, opened in text mode(!)
        :type fh: file object

        """
        super().__init__(fh, **kwargs)
        self.reader = DictReader(self.fh, delimiter="\t", **kwargs)

    def __next__(self) -> Dict[str, str]:
        record = next(self.reader)
        # Since WoS files have a spurious tab at the end of each line, we
        # may get a 'ghost' None key.
        try:
            del record[None]  # type: ignore
        except KeyError:
            pass
        return record


class PlainTextReader(Reader):
    def __init__(self, fh: TextIO, **kwargs) -> None:
        """Create a reader for WoS plain text file `fh`

        If you do not know the format of a file, the :func:`.read` function
        tries to automatically Do The Right Thing.

        :param fh: WoS plain text file, opened in text mode(!)
        :type fh: file object

        """
        super().__init__(fh, **kwargs)
        self.version = "1.0"  # Expected version of WoS plain text format
        self.current_line = 0

        line = self._next_nonempty_line()
        if not line.startswith("FN"):
            raise ReadError("Unknown file format")

        line = self._next_nonempty_line()
        label, version = line.split()
        if label != "VR" or version != self.version:
            raise ReadError(
                "Unknown version: expected {} "
                "but got {}".format(self.version, version)
            )

    def _next_line(self) -> str:
        """Get next line as string"""
        self.current_line += 1
        return next(self.fh).rstrip("\n")

    def _next_nonempty_line(self) -> str:
        """Get next line that is not empty"""
        line = ""
        while not line:
            line = self._next_line()
        return line

    def _next_record_lines(self) -> List[str]:
        """Gather lines that belong to one record"""
        lines: List[str] = []
        while True:
            try:
                line = self._next_nonempty_line()
            except StopIteration:
                raise ReadError("Encountered EOF before 'EF' marker")
            if line.startswith("EF"):
                if lines:  # We're in the middle of a record!
                    raise ReadError(
                        "Encountered unexpected end of file marker EF on line {}".format(
                            self.current_line
                        )
                    )
                else:  # End of file
                    raise StopIteration
            if line.startswith("ER"):  # end of record
                return lines
            else:
                lines.append(line)

    def _format_values(self, heading: str, values: List[str]) -> str:
        if has_item_per_line[heading]:  # Iterable field with one item per line
            return "; ".join(values)
        else:
            return " ".join(values)

    def __next__(self) -> Dict[str, str]:
        record = {}
        values: List[str] = []
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
