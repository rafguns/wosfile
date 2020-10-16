# wosfile

[![Build Status](https://travis-ci.org/rafguns/wosfile.svg?branch=master)](https://travis-ci.org/rafguns/wosfile)
[![Coverage Status](https://coveralls.io/repos/rafguns/wosfile/badge.svg?branch=master&service=github)](https://coveralls.io/github/rafguns/wosfile?branch=master)

**wosfile** is a Python package designed to read and handle data exported from Clarivate Analytics [Web of Science™](https://www.webofknowledge.com). It supports both tab-delimited files and so-called ‘plain text’ files.

The point of wosfile is to read export files from WoS and give you a simple data structure—essentially a dict—that can be further analyzed with tools available in standard Python or with third-party packages. If you're looking for a ‘one-size-fits-all’ solution, this is probably not it.

Pros:
* It has no requirements beyond Python 3.6+ and the standard library.
* Completely iterator-based, so useful for working with large datasets. At no point should we ever have more than one single record in memory.
* Simple API: usually one needs just one function `wosfile.records_from()`.

Cons:
* Pure Python, so might be slow.
* At the moment, wosfile does little more than reading WoS files and generating *Record* objects for each record. While it does some niceties like parsing address fields, it does not have any analysis functionality.

## Examples

These examples use a dataset exported from Web of Science in multiple separate files(the maximum number of exported records per file is 500).

### Subject categories in our data

```python
import glob
import wosfile
from collections import Counter

subject_cats = Counter()
# Create a list of all relevant files. Our folder may contain multiple export files.
files = glob.glob("data/savedrecs*.txt")

# wosfile will read each file in the list in turn and yield each record
# for further handling
for rec in wosfile.records_from(files):
    # Records are very thin wrappers around a standard Python dict,
    # whose keys are the WoS field tags.
    # Here we look at the SC field (subject categories) and update our counter
    # with the categories in each record.
    subject_cats.update(rec.get("SC"))

# Show the five most common subject categories in the data and their number.
print(subject_cats.most_common(5))
```

### Citation network

For this example you will need the [NetworkX](http://networkx.github.io/) package. The data must be exported as ‘Full Record and Cited References’.

```python
import networkx as nx
import wosfile

# Create a directed network (empty at this point).
G = nx.DiGraph()
nodes_in_data = set()

for rec in wosfile.records_from(files):
    # Each record has a record_id, a standard string uniquely identifying the reference.
    nodes_in_data.add(rec.record_id)
    # The CR field is a list of cited references. Each reference is formatted the same
    # as a record_id. This means that we can add citation links by connecting the record_id
    # to the reference.
    for reference in rec.get("CR", []):
        G.add_edge(rec.record_id, reference)

# At this point, our network also contains all references that were not in the original data.
# The line below ensures that we only retain publications from the original data set.
G.remove_nodes_from(set(G) - nodes_in_data)
# Show some basic statistics and save as Pajek file for visualization and/or further analysis.
print(nx.info(G))
nx.write_pajek(G, 'network.net')
```

## Other Python packages

The following packages also read WoS files (+ sometimes much more):
* [WOS+](https://pypi.org/project/WOSplus/)
* [metaknowledge](https://pypi.org/project/metaknowledge/)
* [wostools](https://pypi.org/project/wostools/)

Other packages query WoS directly through the API and/or by scraping the web interface:
* [pywos](https://pypi.org/project/pywos/) (elsewhere called [wos-statistics](https://github.com/refraction-ray/wos-statistics))
* [wos](https://pypi.org/project/wos/)
* [wosclient](https://pypi.org/project/wosclient/)
