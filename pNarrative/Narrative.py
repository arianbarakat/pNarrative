from __future__ import absolute_import

class Narrative():


    def __init__(self, book, lower = False):
        from pNarrative.parser import parser
        self.text = book
        self.sentences = parser.text2sentence(self.text, lower = lower)
        self.sentTokens = [parser.sentence2tokens(sent) for sent in self.sentences]
        self.nrSentences = len(self.sentences)
        self.sentIdx = list(range(self.nrSentences))



    def get_sentiment_score(self, lexicon):
        from pNarrative.parser.sentiment_scorer import get_sentiment_score

        self.sentiment_scores = [get_sentiment_score(tokens=tokens, lexicon = lexicon) for tokens in self.sentTokens]

    def get_narrative_estimation(self, kernel, kernel_parameters, noise_sigma = 1, filter_zeros = True, use_normalized_x = True):
        from .gp import gp
        self.narrative_estimation = gp.GP(x = self.sentIdx,\
                                        y = self.sentiment_scores,\
                                        kernel = kernel,\
                                        noise_sigma = noise_sigma)
        self.narrative_estimation.train(kernel_parameters = kernel_parameters, filter_zeros = filter_zeros, use_normalized_x = use_normalized_x)
        self.narrative_estimation.predict()

    def plot_narrative(self, scale_narrative = True, plot_errors = True):
        import matplotlib.pyplot as plt
        from pNarrative.util.normalization import scale
        assert isinstance(scale_narrative, bool)
        assert isinstance(plot_errors, bool)

        x_grid = list(self.narrative_estimation.x_new)
        y_grid = list(self.narrative_estimation.predictions["predictive_mean"])
        y_error_upper95 = list(self.narrative_estimation.predictions["upper95"])
        y_error_lower95 = list(self.narrative_estimation.predictions["lower95"])

        if scale_narrative:
            y_error_upper95 = list(scale(y_error_upper95, (-1,1),\
                                    custom_max = max(y_grid),\
                                    custom_min = min(y_grid)))
            y_error_lower95 = list(scale(y_error_lower95, (-1,1),\
                                    custom_max = max(y_grid),\
                                    custom_min = min(y_grid)))
            y_grid = scale(y_grid, (-1,1))


        plt.plot(x_grid,y_grid, linestyle='solid')
        plt.xlim(0, 100)
        plt.ylim(min(y_grid), max(y_grid))
        if plot_errors:
            plt.fill_between(x = x_grid, y1=y_error_lower95, y2=y_error_upper95, alpha = 0.5)
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
