# How to create a download citation for a GBIF custom export

When GBIF Data Products team makes custom exports, we want these to have a citation file in a standard format. That format is the same that we provide to users that request the Darwin Core archive download (full columns download). The format for this is as follows:

> ['contacts', 'title', 'version', 'publishing Organization Key', 'type', 'DOI']

Here is a small sample:
```
When using this dataset please use the following citation and pay attention to the rights documented in rights.txt:    
Grant S(2020). Field Museum of Natural History (Zoology) Invertebrate Collection.  Field Museum. OCCURRENCE dataset 10.15468/6q5vuc accessed via GBIF.org on 2020-02-03.    
Creuwels J(2020). Naturalis Biodiversity Center (NL) - Mammalia.  Naturalis Biodiversity Center. OCCURRENCE dataset 10.15468/d7gugd accessed via GBIF.org on 2020-02-03.    
Schneider C(2020). Morphological review of the order Neelipleona (Collembola) through the redescription of the type species of Acanthoneelidus, Neelides and Neelus.  Plazi.org taxonomic treatments database. CHECKLIST dataset 10.11646/zootaxa.4308.1.1 accessed via GBIF.org on 2020-02-03.    
Gerken S(2020). Hemilamprops chilensis sp. nov. (Crustacea: Cumacea: Lampropidae) from the coast of Chile, with a key to the Chilean Lampropidae and remarks on the status of H. ultimaespei Zimmer, 1921 and H. lotusae Băcescu, 1969.  Plazi.org taxonomic treatments database. CHECKLIST dataset 10.11646/zootaxa.4399.3.5 accessed via GBIF.org on 2020-02-03.    
Guàrdia R(2020). CeDoc de Biodiversitat Vegetal: BCN-Bryophyta.  CeDoc of Plant Biodiversity (CeDocBIV), Univ. Barcelona. OCCURRENCE dataset 10.15470/ynlzi9 accessed via GBIF.org on 2020-02-03.    
Roberts D(2020). CHAS Malacology Collection (Arctos).  Chicago Academy of Sciences. OCCURRENCE dataset 10.15468/tk35ga accessed via GBIF.org on 2020-02-03.    
```

The citation_for_export.py module provides the way to do that. The execution method only requires an input csv file having the list of dataset keys (GBIF dataset UUIDs)
-one for each line- and the output file name that will contain the citation text itself.

### Getting started

The big two things to have in place before running the code is the Python [Requests](https://2.python-requests.org/en/master/) library and a CSV file of GBIF dataset keys.

### Usage

> import citation_for_export as ex


> res = ex.exe_citation('My_Dataset_Keys.csv', 'My_Citation_File.txt')
