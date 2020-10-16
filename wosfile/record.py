import re
from collections import defaultdict
from typing import Dict, Iterable, Iterator, List, Optional, Union

from .read import read
from .tags import is_splittable

__all__ = ["Record", "parse_address_field", "records_from"]


def split_by(string: str, delimiter: str) -> List[str]:
    return [part.strip() for part in string.split(delimiter)]


class Record(dict):
    def __init__(
        self, wos_data: Dict[str, str] = None, skip_empty: bool = True
    ) -> None:
        """Create a record based on *wos_data*

        :param dict wos_data: a WoS record
        :param bool skip_empty: whether or not to skip empty fields

        """
        self.skip_empty = skip_empty
        if wos_data:
            self.parse(wos_data)

    def parse(self, wos_data: Dict[str, str]) -> None:
        """Parse *wos_data* into more structured format

        :param dict wos_data: a WoS record

        """
        self.clear()
        for field_name, value in wos_data.items():
            if self.skip_empty and not value:
                continue
            if is_splittable[field_name]:
                self[field_name] = split_by(value, ";")
            else:  # No parsing needed
                self[field_name] = value

    @property
    def record_id(self) -> str:
        """Get WoS record ID for current data"""
        import re

        first_author = re.sub(r"(.*), (.*)", r"\1 \2", self["AU"][0])
        year = self.get("PY")
        journal = self.get("J9", self.get("BS", self.get("SO")))
        volume = "V" + self["VL"] if "VL" in self else None
        page = "P" + self["BP"] if "BP" in self else None
        doi = "DOI " + self["DI"] if "DI" in self else None

        return ", ".join(
            item for item in (first_author, year, journal, volume, page, doi) if item
        )

    @property
    def author_address(self) -> Optional[Union[List[str], Dict[str, List[str]]]]:
        try:
            return parse_address_field(self['C1'])
        except KeyError:
            return None


def parse_address_field(field: str) -> Union[List[str], Dict[str, List[str]]]:
    """Parse author address field into author -> addresses dict"""
    # Only addresses, no authors
    if not field.startswith("["):
        addresses = field.split("; ")

        # It may happen that the first address(es) dont have authors but the rest do:
        # Remove the ones without authors in that case and reparse what remains.
        # See issue #8.
        if any(address.startswith("[") for address in addresses):
            m = re.search(r".+?;\s*(\[.+$)", field)
            trimmed_field = m.group(1)  # type: ignore
            return parse_address_field(trimmed_field)
        return addresses

    # Addresses with authors
    address_field_re = re.compile(
        r"""\s*\[(.*?)\] # Author part
        \s+(.*)          # Address part
        """,
        re.VERBOSE,
    )
    parsed: Dict[str, List[str]] = defaultdict(list)

    address_fields = re.split(r";(?=\s*\[)", field)
    for address_field in address_fields:
        match = address_field_re.match(address_field)
        if match:
            authors, address = match.groups()
        else:
            raise ValueError(f"Could not parse '{address_field}' as address field")

        for author in split_by(authors, ";"):
            parsed[author].append(address)

    return parsed


def records_from(
    fname: Union[str, Iterable[str]], skip_empty: bool = True, **kwargs
) -> Iterator[Record]:
    """Get records from WoS file *fobj*

    :param fname: WoS file name(s)
    :type fname: str or list of strings
    :param bool skip_empty: whether or not to skip empty fields
    :return:
        iterator over parsed records in *fobj*, where each parsed record is a
        :py:class:`wosfile.Record`

    """
    for wos_record in read(fname, **kwargs):
        yield Record(wos_record, skip_empty)
