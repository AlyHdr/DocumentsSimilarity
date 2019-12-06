import xml.etree.ElementTree as ET
import pandas as pd
import os
import sys


# function to parse a single xml document and get the filename,title,abstract and claims
# in one list row to be added to the data frame


def parse_file(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    title = root.find('Title')
    abstract = root.find('Abstract')
    claims = root.find('Claims')

    all_claims = ''

    if claims is not None:
        # iterate over claims and remove any other character than a letter
        for claim in claims:
            claim_text = claim.text
            claim_res = ''
            for x in claim_text:
                if x == ' ':
                    claim_res += x
                else:
                    if x.isalpha():
                        claim_res += x
            all_claims += claim_res + ' '
    title_text = ''
    if title is not None:
        title_text = title.text
    abstract_text = ''
    if abstract is not None:
        abstract_text = abstract.text
    # if any of the entries is empty then the data set will be affected but later cleaned on processing
    row = [file_name, title_text, abstract_text, all_claims]

    return row


# get all file names in the passed directory


def parse_all(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.xml' in file:
                files.append(os.path.join(r, file))
    data = []
    for f in files:
        row = parse_file(f)
        data.append(row)
    return data


def generate_data_set(directory, csv_file):
    all_data = parse_all(directory)
    df = pd.DataFrame(all_data, columns=['FileName', 'Title', 'Abstract', 'Claims'])
    df.to_csv(csv_file)
    print('Data set generated in {}'.format(csv_file))


# recieve arguments from command line full directory path of documents and csv file

if len(sys.argv) == 3:
    generate_data_set(sys.argv[1], sys.argv[2])
else:
    print('run the script like this by passing the right arguments : \n"python parser.py direcoty_path '
          'full_csv_dataset_name"')
# pub_number = root.find('PublicationNumber')
# print(pub_number.text)
#
# inventor_name = root.find('Inventor').find('Name')
# print(inventor_name.text)
#
# applicant_name = root.find('Applicant').find('Name')
# print(applicant_name.text)
#
# requested_patent = root.find('RequestedPatent')
# print(requested_patent.text)
#
# applicant_name = root.find('ApplicationElem').find('Name')
# print(applicant_name.text)
