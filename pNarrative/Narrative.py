from __future__ import absolute_import

class Narrative():


    def __init__(self, book, lower = False):
        from parser.parser import text2sentence, sentence2tokens
        self.text = book
        self.sentences = text2sentence(self.text, lower = lower)
        self.sentTokens = [sentence2tokens(sent) for sent in self.sentences]
        self.nrSentences = len(self.sentences)
        self.sentIdx = list(range(self.nrSentences))



    def get_sentiment_score(self, lexicon):
        from parser.sentiment_scorer import get_sentiment_score

        self.sentiment_scores = [get_sentiment_score(tokens=tokens, lexicon = lexicon) for tokens in self.sentTokens]

    def get_narrative_estimation(self, kernel, kernel_parameters, noise_sigma = 1):
        from gp import gp
        self.narrative_estimation = gp.GP(x = self.sentIdx,y = self.sentiment_scores, kernel = kernel, noise_sigma = noise_sigma)
        self.narrative_estimation.train(kernel_parameters = kernel_parameters)
        self.narrative_estimation.predict()

    def plot_narrative(self, scale = True):
        import matplotlib.pyplot as plt
        from util import normalization
        if scale:
            y_grid = list(normalization.scale(self.narrative_estimation.predictions["predictive_mean"], (-1,1)))
        else:
            y_grid = list(self.narrative_estimation.predictions["predictive_mean"], (-1,1))

        plt.plot(list(self.narrative_estimation.x_new),y_grid, linestyle='solid')
        plt.xlim(0, 100)
        plt.ylim(min(y_grid), max(y_grid))
        plt.ylabel('Sentiment Polarity')
        plt.xlabel('Narrative Time')
        plt.show()






if __name__ == "__main__":
    import requests
    example_URL = "http://www.gutenberg.org/cache/epub/706/pg706.txt"
    r = requests.get(example_URL)
    bookObj = Narrative(r.text, lower =True)
    from parser.sentiment_scorer import create_lexicon

    lexicon = create_lexicon("/Users/arian.barakat/Documents/Code/NLP/pNarrative/pNarrative/data/lexicons/afinn/AFINN-sv-165.txt", delim="\t")


    bookObj.get_sentiment_score(lexicon=lexicon)
    from kernels.rbf import rbf
    rbf
    bookObj.get_narrative_estimation(kernel= rbf, kernel_parameters= {"el":7, "sigma":1})
    import matplotlib.pylab as plt
    bookObj.plot_narrative()
