"""
This module exists to reproduce the GBIF citation text file which users obtain when requesting a full DwC archive download.
This is the desired end format:
citation_string = '{originator}({year}). {dataset_title}. {version} {publisher}. {type} dataset {doi} accessed via GBIF.org on {date}.'.format(originator=originator, year= today.year, dataset_title=dataset_title, version=vers, publisher=pubtitle, type=misc['type'], doi=misc['doi'], date=misc['date'])
"""
import csv
from datetime import date
import requests

today = date.today()


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            print('is dict')
            for k, v in obj.items():
                print('in if loop')
                # print(k, ':', v)
                if isinstance(v, (dict, list)):
                    print('in dict/list loop')
                    extract(v, arr, key)
                elif k == key:
                    print('IN append str ')
                    arr.append(v)
        elif isinstance(obj, list):
            print('in list loop')
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


citation_fields = ['contacts', 'title', 'version', 'publishingOrganizationKey', 'type', 'doi']

def contacts(api, key, field):
    '''
    Returns the originator name in the citation format, Lastname[one whitespace]Firstname(first letter)
    :param field:The dataset page field where the originator is.
    :param rson: json formatted text
    :return: The formatted name
    '''
    api = api+key
    rson = requests.get(api)
    rson = rson.json()
    contacts = rson['contacts']

    for j in contacts:
        for k, v in j.items():
            # print('k: ', v)
            if v == 'ORIGINATOR':
                fname = ''
                lname = ''
                try:
                    fname = j['firstName']
                except:
                    pass
                try:
                    lname = j['lastName']
                except:
                    pass
                if lname=='' and fname=='':
                    originator = 'Anonymous'
                elif fname=='':
                    originator = lname+' '+fname
                else:
                    originator = lname + ' ' + fname[0]
                return originator
                break
            else:
                continue
        break

def title(api, key, field):
    '''
    Returns the dataset title
    :param api: call going out to GBIF api
    :param field: the title field
    :return: dataset title
    '''
    api = api+key
    rson = requests.get(api)
    rson = rson.json()
    dataset = rson[field]
    return dataset

def version(api, field):
    '''
    Returns version number if any available
    :param api:
    :param field:
    :return: number
    '''
    rson = requests.get(api)
    rson = rson.json()
    version = ''

    # try:
    version = rson['version']

    # except KeyError:
    #     pass
    # finally:
    return version

def publisher(pubkey, field):
    '''
    Returns the publisher title
    :param pubkey: from initial search, used to look up publisher using the publisher api
    :param field: title
    :return: publisher title
    '''
    pubapi = 'http://api.gbif.org/v1/organization/'
    pubapi = pubapi+pubkey
    rson = requests.get(pubapi)
    rson = rson.json()
    pubtitle = rson['title']
    return pubtitle

def dataset(key, fields):
    '''
    Returns misc values needed in the citation
    :param key: dataset key
    :param fields: type, DOI
    :return: type, DOI, date YYYY-MM-DD
    '''
    datasetapi = 'http://api.gbif.org/v1/dataset/'+key
    print(datasetapi)
    rson = requests.get(datasetapi)
    rson = rson.json()
    print(rson)
    fields = ['type', 'doi']
    dct = {'type':'', 'doi':'', 'date':today.strftime('%Y-%m-%d')}
    for j in fields:
        dct[j] = rson[j]
    return dct

def lookup_dataset(datasetkey):
    datasetapi = 'http://api.gbif.org/v1/dataset/' + datasetkey
    rson = requests.get(datasetapi)
    rson = rson.json()
    pubkey = rson['publishingOrganizationKey']
    return pubkey


def make_citation_string(datasetkey):
    api = "http://api.gbif.org/v1/dataset/"
    misc = dataset(datasetkey, '')
    originator = contacts(api, datasetkey, 'contacts')
    dataset_title = title(api, datasetkey, 'title')
    pubkey = lookup_dataset(datasetkey)
    pubtitle = publisher(pubkey, 'title')
    vers = ''
    try:
        vers = version(api, 'version')
    except:
        pass
    if not vers: vers = ''
    else:
        vers = vers+'.'


    citation_string = '{originator}({year}). {dataset_title}. {version} {publisher}. {type} dataset {doi} accessed via GBIF.org on {date}.'.format(originator=originator, year= today.year, dataset_title=dataset_title, version=vers, publisher=pubtitle, type=misc['type'], doi=misc['doi'], date=misc['date'])
    return citation_string

def read_datasetkeys(filename):
    with open(filename) as f:
        spam = csv.reader(f, delimiter='\t')
        next(spam, None)
        for line in spam:
                line = line[0].split(',')
                key = line[0]
                # print(key)
                # break
                yield key


def exe_citation(input_filename, output_filename):
    
    boiler = 'When using this dataset please use the following citation and pay attention to the rights documented in rights.txt:'

    with open(output_filename, 'w', encoding='utf8') as wrt:


        wrt.write(boiler+'\n')
        rr = read_datasetkeys(input_filename)
        for j in rr:
            ss = j
            key = ss
            cit = make_citation_string(key)
            wrt.write(cit+'\n')
            print('cit: ', cit)
        return output_filename

