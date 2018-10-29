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



def get_sentiment_score(tokens, lexicon):
    assert isinstance(lexicon, dict)
    scores = [lexicon.get(token, float(0)) for token in tokens]
    return sum(scores)
