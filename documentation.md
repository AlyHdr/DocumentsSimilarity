# Model chosen and implementation

For a first glance the data was not so clear so a normal approach was to try to get the similarities (cosine similarity) between words of the titles
of the 1000 documents and check which two documents has the highest similarity ration.

Later then we consider the TF-IDF algorithm where we can get a bag of words and then compute the TF-IDF scores for each category (titles,abstracts,claims) , after this calculation we can get matrices and then get the average with respect to the three categories considered.
Finally we can get the two documents that ranked first against each other according to the three features we take into consideration.

Any further approaches would include context analysis and semantics like LSA algos or concept net where the words are not just compared according to the similarity between them but also the topic and the context plays a role in this ratio we can get.

But for simplicity this approach that have been followed got results where we can make sure that those documents are almost identical:

filename: ~/nano/EP2181142A1.xml 
filename: ~/nano/EP2028218A1.xml

# installation and running

## create an environement and install the necessary packages
`virtualenv my_env --distribute
source my_env/bin/activate
pip list
pip install numpy
pip install sklearn
pip list
pip install pandas`

## run script to generate dataset from xml files
`python parser.py ~/nano/ ~/DocumentsSimilarity/dataset_1000.csv`

## run script to 
`python model.py ~/DocumentsSimilarity/dataset_1000.csv`