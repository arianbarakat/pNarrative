
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

    regex = "\W"

    tokens = re.split(regex, text)
    return [token for token in tokens if not token == '']







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
