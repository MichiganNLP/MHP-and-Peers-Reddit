
# Language Modeling

The original language model code comes from [Merity et al's 2018 code](https://github.com/salesforce/awd-lstm-lm). See their README for full details on how to run the language model. There are additional preprocessing scripts in the `data` folder that may be helpful depending on your use case.


## Added Parameters

We have added the following parameters:

`--eout entropy_file`

`--vocab vocab_file`

The `eout` option specifies the file name where the model entropies will be written.

The `vocab` option tells the model to fix the vocabulary using an existing vocabulary file.

## Getting Words and Categories by Entropy

You can use `read_entropy.py` to get the categories sorted by entropy. You can also get the words for a specific category by setting `TARGET_CAT`.

`PATH_TO_TEST_DATA` should specify the location of the file with plaintext sentences you want to use.

Note the purpose of the following four files:
`MOM_FILE` is the log of entropy scores for the MHP model run on MHP data.
`POM_FILE` is the log of entropy scores for the Peer model run on MHP data.
`MOP_FILE` is the log of entropy scores for the MHP model on Peer data.
`POP_FILE` is the log of entropy scores for the Peer model on Peer data.


## Language Model Classification

You can use `ent_as_classifier.py` to use the language model entropies for classification. It requires the same file paths as the previous section.

The `find_pred_flip_words` function also generates plots of the language model entropies over the tokens in the sentence.