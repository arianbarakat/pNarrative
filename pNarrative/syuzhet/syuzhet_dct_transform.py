
def syuzhet_dct_transform(x, low_pass_size, **kwargs):
    from scipy.fftpack import dct, idct

    dct_transform = dct(x,type=2)
    filtered_dct_tranform = [dct_transform[i] if i < low_pass_size else 0 for i in range(101)]
    idct_tranform = idct(filtered_dct_tranform,type=2)

    narrative_time = [i for i in range(len(idct_tranform))]

    return({"estimated_narrative": idct_tranform, "narrative_time":narrative_time})
