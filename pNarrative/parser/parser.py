
def segment2sentence(text, lower = False):
    import re

    assert isinstance(text, str)
    assert isinstance(lower, bool)

    regex = r'\w(\.{3}|[^\.|\?|!])+(\.|\?|!|.$)'
    segments  = [i.group(0) for i in re.finditer(regex, text)]

    if lower:
        try:
            segments = [seg.lower() for seg in segments if not seg == '']
        except NameError:
            segments = []
    else:
        segments = [seg for seg in segments if not seg == '']
    return segments

def segment2custom(text, lower = False, **kwargs):
    import re

    assert isinstance(text, str)
    assert isinstance(lower, bool)

    regex = kwargs['pattern']
    assert isinstance(regex, str)
    segments  = re.split(regex, text)

    if lower:
        try:
            segments = [seg.lower() for seg in segments if not seg == '']
        except NameError:
            segments = []
    else:
        segments = [seg for seg in segments if not seg == '']
    return segments


def tokenize(text):# include_emoticons = False):
    import re

    assert isinstance(text, str)
    #assert isinstance(include_emoticons, bool)

    #compile_RE = lambda pat:  re.compile(pat,  re.UNICODE)
    #emoticons = get_emoticons_RE()

    #if include_emoticons:
    #    regex = "\W|^"+emoticons
    #else:
    regex = "\W"

    tokens = re.split(regex, text)
    return [token for token in tokens if not token == '']
#
#def get_emoticons_RE():
#    import re#

#    emoticons_parts = {"NormalEyes":r'[:=]',\
#                        "Wink":r'[;]',\
#                        "NoseArea":r'(|o|O|-)',\
#                        "HappyMouths":r'[D\)\]]',\
#                        "SadMouths":r'[\(\[]', \
#                        "Tongue":r'[pP]'}
#    emoticons =\
#        "("+emoticons_parts["NormalEyes"]+ "|"+emoticons_parts["Wink"]+")"\
#        +emoticons_parts["NoseArea"]+\
#        "("+emoticons_parts["Tongue"]+"|"+emoticons_parts["SadMouths"]+"|"+emoticons_parts["HappyMouths"]+")"#

#    return emoticons







if __name__ == "__main__":
    example = "This is a sentence. \
                Is this? What if we put a comma here, and another one here, would this be a sentence?\
                Probably!\
                And what if we take a pause like this... will this be a sent?\
                Lastly, we try this; and this: symbol! Then a smiley :D"
    example_empty = "   "
    [sentence2tokens(sent) for sent in text2sentence(example, lower = True)]
    [sentence2tokens(sent) for sent in text2sentence(example, lower = False)]
    [sentence2tokens(sent) for sent in text2sentence(example_empty, lower = True)]
    [sentence2tokens(sent) for sent in text2sentence(example_empty, lower = False)]
