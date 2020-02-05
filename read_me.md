# How to create a download citation for a GBIF custom export

When GBIF Data Products team makes custom exports, we want these to have a citation file in a standard format. That format is the same that we provide to users that request the Darwin Core archive download (full columns download). The format for this is as follows:

> ['contacts', 'title', 'version', 'publishing Organization Key', 'type', 'DOI']

The citation_for_export.py module provides the way to do that. The execution method only requires an input csv file having the list of dataset keys (GBIF dataset UUIDs)
-one for each line- and the output file name that will contain the citation text itself.

