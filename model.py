import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sys


# clean the data where some of the files doesn't contain (Abstract or Claims) so those rows should be droped


def clean_data(df):
    data = df.to_numpy()
    clean_data = []
    for row in data:
        # to check if the value is Nan compared with itself
        if row[2] != row[2] or row[3] != row[3] or row[4] != row[4]:
            print('Found empty entry !')
        else:
            clean_data.append(row[1:6])

    # create the new dataframe from the cleaned data
    df = pd.DataFrame(clean_data, columns=['FileName', 'Title', 'Abstract', 'Claims'])
    return df


def titles_similarity(filenames,df):
    titles = df['Title'].to_numpy()

    new_titles = []
    for title in titles:
        # remove every character that won't be helpful for the tf-ifd algo
        title = title.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(",", "").replace("\"",
                                                                                                                   "").strip()
        new_titles.append(title)

    # use sklearn vectorizer to get a pairwise similarity matrix between all the titles against each other
    tfidf = TfidfVectorizer().fit_transform(new_titles)
    pairwise_similarity = tfidf * tfidf.T
    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, np.nan)
    max = np.nanmax(arr[0])
    index_doc_1 = 0
    index_doc_2 = 0
    # get the maximum similarity and the index of the two documents associated with this similarity ratio
    for i in range(len(new_titles)):
        local_max = np.nanmax(arr[i])
        if local_max >= max:
            max = local_max
            index_doc_1 = i
            index_doc_2 = np.nanargmax(arr[i])

    # printing local results according to titles similarity
    print("max: {} 1: {} 2:{}".format(max, index_doc_1, index_doc_2))

    print('title_1: {} '.format(new_titles[index_doc_1]))
    print('title_2: {} '.format(new_titles[index_doc_2]))

    print('filename: {} '.format(filenames[index_doc_1]))
    print('filename: {} '.format(filenames[index_doc_2]))
    return arr


# the rest two functions do the same as above in similarity comparison with titles
def abstract_similarity(filenames,df):
    abstracts = df['Abstract'].to_numpy()

    new_abstracts = []
    count = 0
    for abstract in abstracts:
        abstract = abstract.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(",",
                                                                                                        "").replace(
            "\"", "").strip()
        new_abstracts.append(abstract)
        count += 1

    tfidf = TfidfVectorizer().fit_transform(new_abstracts)
    pairwise_similarity = tfidf * tfidf.T
    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, np.nan)
    max = np.nanmax(arr[0])
    index_doc_1 = 0
    index_doc_2 = 0
    array_length = len(new_abstracts)
    for i in range(array_length):
        local_max = np.nanmax(arr[i])
        if local_max >= max:
            max = local_max
            index_doc_1 = i
            index_doc_2 = np.nanargmax(arr[i])

    print("max: {} 1: {} 2:{}".format(max, index_doc_1, index_doc_2))

    print('abstract_1: {} '.format(new_abstracts[index_doc_1]))
    print('abstract_2: {} '.format(new_abstracts[index_doc_2]))

    print('filename: {} '.format(filenames[index_doc_1]))
    print('filename: {} '.format(filenames[index_doc_2]))
    return arr


def claims_similarity(filenames):
    claims = df['Claims'].to_numpy()

    new_claims = []
    count = 0
    for claim in claims:
        claim = claim.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(",", "").replace("\"",
                                                                                                                   "").strip()
        new_claims.append(claim)
        count += 1

    tfidf = TfidfVectorizer().fit_transform(new_claims)
    pairwise_similarity = tfidf * tfidf.T
    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, np.nan)
    max = np.nanmax(arr[0])
    index_doc_1 = 0
    index_doc_2 = 0
    array_length = len(new_claims)
    for i in range(array_length):
        local_max = np.nanmax(arr[i])
        if local_max >= max:
            max = local_max
            index_doc_1 = i
            index_doc_2 = np.nanargmax(arr[i])

    print("max: {} 1: {} 2:{}".format(max, index_doc_1, index_doc_2))

    print('claim_1: {} '.format(new_claims[index_doc_1]))
    print('claim_2: {} '.format(new_claims[index_doc_2]))

    print('filename: {} '.format(filenames[index_doc_1]))
    print('filename: {} '.format(filenames[index_doc_2]))
    return arr


# load the data from csv file already generated
if len(sys.argv) == 2:
    df = pd.read_csv(sys.argv[1])
    df = clean_data(df)
    filenames_arr = df['FileName'].to_numpy()

    # get the matrices of the three categories
    arr_titles = titles_similarity(filenames_arr, df)
    arr_abstract = abstract_similarity(filenames_arr, df)
    arr_claims = claims_similarity(filenames_arr, df)

    # sum up and get the average of those matrices
    total_similarity = (arr_titles + arr_abstract + arr_claims) / 3

    ''' 
    again get the maximum similairty on the new averaged results so we can tell how much the documents
     are similar according to the three features we extracted from them 
     '''
    index_doc_1 = 0
    index_doc_2 = 0
    max = np.nanmax(total_similarity[0])

    for i in range(len(total_similarity)):
        local_max = np.nanmax(total_similarity[i])
        if local_max >= max:
            max = local_max
            index_doc_1 = i
            index_doc_2 = np.nanargmax(total_similarity[i])

    # print the final results

    print("max: {} 1: {} 2:{}".format(max, index_doc_1, index_doc_2))
    print('filename: {} '.format(filenames_arr[index_doc_1]))
    print('filename: {} '.format(filenames_arr[index_doc_2]))
else:
    print('please enter dataset file name with full path...')
