

def plot_narrative(object, type, **kwargs):
    assert type in ["gp", "rolling_mean", "merged", "syuzhet"], "Select a supported plot-type"

    if type == "gp":
        plot_gp(object= object, **kwargs)

    if type == "rolling_mean":
        plot_moving_avg(object=object, **kwargs)

    if type == "syuzhet":
        plot_syuzhet(object=object, **kwargs)

    if type == "merged":
        plot_merged(object=object, **kwargs)


def plot_syuzhet(object, **kwargs):
    import matplotlib.pyplot as plt
    from pNarrative.util.normalization import scale, normalizeNarrativeTime

    x_grid = normalizeNarrativeTime(object.narrative_estimation_syuzhet["narrative_time"])
    y_grid = list(object.narrative_estimation_syuzhet["estimated_narrative"])

    if "scale_narrative" in kwargs.keys():
        if kwargs["scale_narrative"]:
            y_grid = scale(y_grid, (-1,1))

    fig = plt.figure()
    plt.plot(x_grid,y_grid, linestyle='solid')
    plt.xlim(0, 100)

    if not object.text_id == None:
        fig.suptitle(object.text_id, fontsize=12)
    plt.ylabel('Sentiment Polarity')
    plt.xlabel('Narrative Time (%)')
    plt.draw()


def plot_gp(object, **kwargs):
    import matplotlib.pyplot as plt
    from pNarrative.util.normalization import scale, normalizeNarrativeTime

    x_grid = list(object.narrative_estimation.x_new)
    y_grid = list(object.narrative_estimation.predictions["predictive_mean"])
    y_error_upper95 = list(object.narrative_estimation.predictions["upper95"])
    y_error_lower95 = list(object.narrative_estimation.predictions["lower95"])

    if "scale_narrative" in kwargs.keys():
        if kwargs["scale_narrative"]:
            y_error_upper95 = list(scale(y_error_upper95, (-1,1),\
                                        custom_max = max(y_grid),\
                                        custom_min = min(y_grid)))
            y_error_lower95 = list(scale(y_error_lower95, (-1,1),\
                                        custom_max = max(y_grid),\
                                        custom_min = min(y_grid)))
            y_grid = scale(y_grid, (-1,1))

    fig = plt.figure()
    plt.plot(x_grid,y_grid, linestyle='solid')
    plt.xlim(0, 100)

    if "scale_narrative" in kwargs.keys():
        if kwargs["scale_narrative"]:
            plt.ylim(-1,1)

    if "plot_errors" in kwargs.keys():
        if kwargs["plot_errors"]:
            plt.fill_between(x = x_grid, y1=y_error_lower95, y2=y_error_upper95, alpha = 0.5)

    if not object.text_id == None:
        fig.suptitle(object.text_id, fontsize=12)
    plt.ylabel('Sentiment Polarity')
    plt.xlabel('Narrative Time (%)')
    plt.draw()



def plot_moving_avg(object, **kwargs):
    import matplotlib.pyplot as plt
    from pNarrative.util.normalization import scale, normalizeNarrativeTime
    from pNarrative.util.rolling_mean import rolling_mean
    import numpy as np

    if "wdw_size" in kwargs.keys():
        assert isinstance(kwargs["wdw_size"], int)
        wdw_size = kwargs["wdw_size"]
    else:
        wdw_size = round(len(object.narrative_estimation.x_normalized)*0.1)

    x_grid = object.narrative_estimation.x_normalized
    y_grid = rolling_mean(object.sentiment_scores, wdw= wdw_size)

    if "scale_narrative" in kwargs.keys():
        if kwargs["scale_narrative"]:
            y_grid = scale(y_grid, (-1,1), custom_max = np.nanmax(y_grid), custom_min=np.nanmin(y_grid))

    fig = plt.figure()
    plt.plot(x_grid,y_grid, linestyle='solid')
    plt.xlim(0, 100)


    if not object.text_id == None:
        fig.suptitle(object.text_id, fontsize=12)
    plt.ylabel('Sentiment Polarity')
    plt.xlabel('Narrative Time (%)')
    plt.draw()


def plot_merged(object, **kwargs):
    import matplotlib.pyplot as plt
    from pNarrative.util.normalization import scale, normalizeNarrativeTime
    from pNarrative.util.rolling_mean import rolling_mean
    import numpy as np

    #GP
    x_grid = list(object.narrative_estimation.x_new)
    y_grid = list(object.narrative_estimation.predictions["predictive_mean"])
    y_error_upper95 = list(object.narrative_estimation.predictions["upper95"])
    y_error_lower95 = list(object.narrative_estimation.predictions["lower95"])

    if "wdw_size" in kwargs.keys():
        assert isinstance(kwargs["wdw_size"], int)
        wdw_size = kwargs["wdw_size"]
    else:
        wdw_size = round(len(object.narrative_estimation.x_normalized)*0.1)

    x_grid_ma = object.narrative_estimation.x_normalized
    y_grid_ma = rolling_mean(object.sentiment_scores, wdw= wdw_size)

    # Force Scaling so  they match
    y_grid_ma = scale(y_grid_ma, (-1,1), custom_max = np.nanmax(y_grid_ma), custom_min=np.nanmin(y_grid_ma))

    y_error_upper95 = list(scale(y_error_upper95, (-1,1),\
                                custom_max = max(y_grid),\
                                custom_min = min(y_grid)))
    y_error_lower95 = list(scale(y_error_lower95, (-1,1),\
                                custom_max = max(y_grid),\
                                custom_min = min(y_grid)))
    y_grid = scale(y_grid, (-1,1))

    fig = plt.figure()
    plt.plot(x_grid,y_grid, linestyle='solid')
    plt.plot(x_grid_ma,y_grid_ma, linestyle='solid')
    plt.xlim(0, 100)
    plt.ylim(-1,1)


    if "plot_errors" in kwargs.keys():
        if kwargs["plot_errors"]:
            plt.fill_between(x = x_grid, y1=y_error_lower95, y2=y_error_upper95, alpha = 0.5)

    if not object.text_id == None:
        fig.suptitle(object.text_id, fontsize=12)
    plt.ylabel('Sentiment Polarity')
    plt.xlabel('Narrative Time (%)')
    plt.draw()




if __name__ == "__main__":
    from pNarrative import Narrative
    from pNarrative.kernels.rbf import rbf
    from pNarrative.parser.sentiment_scorer import get_sentiment_lexicon

    with open("/Users/arian.barakat/Documents/Data/books/9789100168254.txt") as f:
        book_text = f.read()

    book = Narrative.Narrative(book=book_text, id = "KJ")
    lexicon_sv_afinn = get_sentiment_lexicon("afinn", "sv")
    book.segment_text(mode = "sentence")
    book.get_sentiment_score(lexicon= lexicon_sv_afinn)
    book.get_narrative_estimation(kernel=rbf,\
                                kernel_parameters={"sigma":2, "el":15})

    plot_gp(book, scale_narrative = True, plot_errors = True)
    plot_moving_avg(book,scale_narrative=True)
    plot_narrative(book, type = "gp", scale_narrative = True, plot_errors = True)
    plot_narrative(book, type = "merged", scale_narrative = True, plot_errors = True, wdw_size=1200)
    plot_merged(book, wdw_size=1000, plot_errors = False)
