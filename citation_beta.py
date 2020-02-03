import requests
from datetime import date


date_object = date.today()
today = date.today()
print(date_object, today.year)


api = "http://api.gbif.org/v1/dataset/4fa7b334-ce0d-4e88-aaae-2e0c138d049e"

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            print('is dict')
            for k, v in obj.items():
                print('in if loop')
                print(k, ':', v)
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

def contacts(api, field):
    '''
    Returns the originator name in the citation format, Lastname[one whitespace]Firstname(first letter)
    :param field:The dataset page field where the originator is.
    :param rson: json formatted text
    :return: The formatted name
    '''

    rson = requests.get(api)
    rson = rson.json()
    contacts = rson['contacts']
    # res  = extract_values(put, 'type')
    # print('TYPE is : ', res)

    for j in contacts:
        for k, v in j.items():
            print('k: ', v)
            if v == 'ORIGINATOR':
                # print('originator ', j)
                fname = j['firstName']
                lname = j['lastName']
                originator = lname+' '+fname[0]
                return originator
                break
            else:
                continue
        break

def title(api, field):
    '''
    Returns the dataset title
    :param api: call going out to GBIF api
    :param field: the title field
    :return: dataset title
    '''
    rson = requests.get(api)
    rson = rson.json()
    dataset = rson[field]
    return dataset

res = contacts(api, 'contacts')
dataset = title(api, 'title')
print(res, dataset)
