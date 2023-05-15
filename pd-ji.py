import pd
import math
from typing import Union, List


def midicent2freq(midicent: float) -> float:
    """
    Converts a value in MIDI cents to its corresponding frequency in Hertz.

    Args:
    - midicent: A float representing the MIDI cent value to be converted to frequency.

    Returns:
    - A float representing the frequency in Hertz corresponding to the input MIDI cent value.
    """
    return 440 * (2 ** ((midicent - 6900) / 1200))


# =============================================================================
def freq2midicent(freq: float) -> float:
    """
    Converts a frequency in Hertz to its corresponding value in MIDI cents.

    Args:
    - freq: A float representing the frequency in Hertz to be converted to MIDI cents.

    Returns:
    - A float representing the MIDI cent value corresponding to the input frequency.
    """
    return 1200 * math.log2(freq / 440) + 6900


# =============================================================================
def rt2mc(ratios, fund):
    """
    Converts a ratio or list of ratios to their corresponding values in MIDI cents.

    Args:
    - ratios: A string, integer, float, or list of strings, integers, or floats representing ratios to be converted to MIDI cents.
    - fund: An optional float representing the fundamental frequency in Hertz. Defaults to 6000.

    Returns:
    - A float or list of floats representing the MIDI cent values corresponding to the input ratios.
    """
    if fund is None:
        fund = 6000
    if isinstance(ratios, str):
        num, den = ratios.split("/")
        return freq2midicent((int(num) / int(den)) * midicent2freq(fund))
    elif isinstance(ratios, list):
        new_ratios = []
        for ratio in ratios:
            num, den = ratio.split("/")
            new_ratios.append(freq2midicent((int(num) / int(den)) * midicent2freq(fund)))
        return new_ratios
    elif isinstance(ratios, int):
        return freq2midicent(ratios * midicent2freq(fund))
    elif isinstance(ratios, float):
        return freq2midicent(ratios * midicent2freq(fund))
    else:
        pd.error("rt2mc just accepts strings, lists, ints and floats")


# =============================================================================
def diamond(limit):
    """
    Returns two lists of lists representing the otonality and utonality matrices of a Partch's diamond.

    Args:
    - limit: An integer representing the maximum odd number to include in the diamond.

    Returns:
    - A list of two lists of lists of strings representing the otonality and utonality matrices of the diamond. The first list contains the otonality matrix, and the second list contains the utonality matrix.
    """

    identities = range(1, limit + 1, 2)
    otonal = []
    utonal = []
    for i in identities:
        otonality = []
        utonality = []
        for j in identities:
            otonality.append(f"{j}/{i}")
            utonality.append(f"{i}/{j}")
        otonal.append(otonality)
        utonal.append(utonality)
    return [otonal, utonal]


# =============================================================================
def octavereduce(ratios, octave):
    if octave is None:
        octave = 2
    octaveRange = math.log2(octave)
    if isinstance(ratios, str):
        num, den = ratios.split("/")
        num = int(num)
        den = int(den)
        ratioValue = int(num) / int(den)
        if ratioValue >= 1 and ratioValue <= (2 ** octaveRange):
            return f"{num}/{den}"

        elif ratioValue < 1:
            num = num * 2
            ratios = f"{num}/{den}"
            return octavereduce(ratios, octave)
        
        elif ratioValue > (2 ** octaveRange):
            den = den * 2
            ratios = f"{num}/{den}"
            return octavereduce(ratios, octave)
        else:
            pd.error("Something went wrong")
        
    elif isinstance(ratios, list):
        new_ratios = []
        for ratio in ratios:
            new_ratios.append(octavereduce(ratio, octave))
        return new_ratios
        
    else:
        pd.error("octavereduce just accepts strings and floats")








def py4pdLoadObjects():
    pd.addobject(midicent2freq, "mc2f", pyout=True)
    pd.addobject(freq2midicent, "f2mc", pyout=True)
    pd.addobject(diamond, "diamond", pyout=True)
    pd.addobject(rt2mc, "rt2mc", pyout=True)
    pd.addobject(octavereduce, "octavereduce", pyout=True)

                

