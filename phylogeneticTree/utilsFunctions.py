import numpy as np

SAMPLE_NUM_TOTAL = 400

def hz2cents(pitchInHz, tonic=261.626):
    cents = 1200*np.log2(1.0*pitchInHz/tonic)
    return cents

def pitchtrackInterp(pitchInCents):
    x = np.linspace(0, 100, len(pitchInCents))
    xvals = np.linspace(0, 100, SAMPLE_NUM_TOTAL)
    pitchInCents_interp = np.interp(xvals, x, pitchInCents)
    return pitchInCents_interp.tolist()