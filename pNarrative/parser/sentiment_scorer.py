def create_lexicon(path_to_file, delim):
    """
    Converts a text file to a dictionary formated sentiment lexicon
    """
    import os
    assert os.path.isfile(path=path_to_file)

    lexicon = {}
    with open(path_to_file, "r") as file:
        for line in file.readlines():
            token, score = line.replace("\n", "").split(delim)
            lexicon[token] = float(score)

    return lexicon



def get_sentiment_lexicon(lexicon, lang):
    """
    Get a sentiment lexicon provided by the module
    """

    import os
    import pNarrative
    existing_lexicons = {"afinn":["sv","en"]}
    filename = {"afinn":\
                    {"en":'/data/lexicons/afinn/AFINN-en-165.txt',\
                     "sv":'/data/lexicons/afinn/AFINN-sv-165.txt'}}

    assert isinstance(lexicon, str)
    assert isinstance(lang, str)
    assert lexicon in existing_lexicons.keys(), "Lexicon not supported yet. Check spelling?"
    assert lang in existing_lexicons[lexicon], "Language not supported yet. Check spelling? Remember to use ISO-country code"

    path_base = os.path.dirname(pNarrative.__file__)
    path_file = filename[lexicon][lang]
    path_full = path_base + path_file
    print(path_full)
    lexicon_dictionary = create_lexicon(path_to_file= path_full ,delim="\t")
    return lexicon_dictionary





def get_sentiment_score(tokens, lexicon):
    assert isinstance(lexicon, dict)
    scores = [lexicon.get(token, float(0)) for token in tokens]
    return sum(scores)
