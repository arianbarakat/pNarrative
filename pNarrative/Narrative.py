from __future__ import absolute_import

class Narrative():

    """
    A python module for the extraction of sentiment and sentiment-based plot arcs from text.

    Workflow:

    1. Initialize an object (read text)
    2. Split text into segments
    3. Get segment-sentiment scores
    4. Estimate Narrative Arc/Plot
    5. Plot Narrative Arc/Plot

    Example:
        from pNarrative import Narrative
        book = Narrative.Narrative(text = book_text)
        book.segment_text(mode = "sentence", lower = True)
        book.get_sentiment_score(lexicon = sentiment_lexicon)
        from pNarrative.kernels.rbf import rbf
        book.get_narrative_estimation(kernel= rbf, kernel_parameters= {"el":20, "sigma":1})

        book.plot_narrative()
    """


    def __init__(self, book, id = None):
        self.text = book
        if not id == None:
            assert isinstance(id, str)
            self.text_id = id


    def segment_text(self, mode, lower = False, **kwargs):
        """
        Split a text into segements. Currently supports sentence and custom
        segmentation defined by a regular expression provided to the argument "pattern"

        Example:
        object.segment_text(mode="sentence", lower = False)

        OR

        object.segment_text(mode="custom", lower = False, pattern = r'\.')


        """
        from pNarrative.parser import parser
        assert isinstance(mode, str)

        segment_type = {
        "sentence":parser.segment2sentence,
        "custom": parser.segment2custom
        }

        assert mode in segment_type.keys()

        segment_func = segment_type[mode]
        self.segments = segment_func(self.text, lower = lower, **kwargs)
        self.segmentTokens = [parser.tokenize(seg) for seg in self.segments]
        self.nrSegments = len(self.segments)
        self.segmentIdx = list(range(self.nrSegments))

    def get_sentiment_score(self, lexicon):
        from pNarrative.parser.sentiment_scorer import get_sentiment_score

        self.sentiment_scores = [get_sentiment_score(tokens=tokens, lexicon = lexicon) for tokens in self.segmentTokens]

    def get_narrative_estimation(self, kernel, kernel_parameters, noise_sigma = 1, filter_zeros = True, use_normalized_x = True):
        from pNarrative.gp import gp
        self.narrative_estimation = gp.GP(x = self.segmentIdx,\
                                        y = self.sentiment_scores,\
                                        kernel = kernel,\
                                        noise_sigma = noise_sigma)
        self.narrative_estimation.train(kernel_parameters = kernel_parameters, filter_zeros = filter_zeros, use_normalized_x = use_normalized_x)
        self.narrative_estimation.predict()

    def glimpse(self, narrative_time, wdw_size):
        from pNarrative.util.find_nearest import find_nearest
        from pNarrative.util.normalization import normalizeNarrativeTime
        narrative_timeline = normalizeNarrativeTime(self.segmentIdx)

        idx = find_nearest(x = narrative_timeline, value= narrative_time)

        left_idx = idx-wdw_size
        right_idx = idx+wdw_size

        if left_idx< 0:
            left_idx = 0
        if right_idx>len(narrative_timeline):
            right_idx = len(narrative_timeline)

        if hasattr(self, "sentiment_scores"):
            for time, score, segment in zip(narrative_timeline[left_idx:right_idx],\
                                    self.sentiment_scores[left_idx:right_idx],\
                                    self.segments[left_idx:right_idx]):
                print("("+str(round(time,2))+"% | Score: "+str(score)+" ) " + str(segment))
        else:
            for time, segment in zip(narrative_timeline[left_idx:right_idx], self.segments[left_idx:right_idx]):
                print("("+str(round(time,2))+"%) " + str(segment))

    def plot_narrative(self, type, **kwargs):
        from pNarrative.plotting.plot_narrative import plot_narrative
        plot_narrative(object=self, type = type, **kwargs)
