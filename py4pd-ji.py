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
            if isinstance(ratio, list):
                new_ratios.append(rt2mc(ratio, fund))
            else:
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
# =============================================================================
def diamond_identities(identities):
    """
    Returns two lists of lists representing the otonality and utonality matrices of a Partch's diamond, but here you choose the identities.

    Args:
    - identities: One list of integers representing the identities of the diamond.

    Returns:
    - A list of two lists of lists of strings representing the otonality and utonality matrices of the diamond. The first list contains the otonality matrix, and the second list contains the utonality matrix.
    """

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


# =============================================================================
def rangereduce(midicents, down, up):
    """
    Returns midicents inside some midicents range.

    Args:
    - midicents: A float or list of floats representing the MIDI cent values to be reduced to the range.
    - down: An integer representing the lower bound of the range.
    - up: An integer representing the upper bound of the range.

    Returns:
    - A float or list of floats representing the MIDI cent values inside the range.
    """

    
    octaveRange = up - down
    valueToDecrease = octaveRange % 1200 
    if (valueToDecrease != 0):
        valueToDecrease = 1200
    else:
        valueToDecrease = octaveRange   


    if (octaveRange < 1200):
        pd.error("The difference between the up and down values must be at least 1200 cents")
        return

    if isinstance(midicents, list):
        new_midicents = []
        for midicent in midicents:
            while True:
                if midicent < down and midicent < up:
                    midicent = midicent + valueToDecrease
                elif midicent > up and midicent > down:
                    midicent = midicent - valueToDecrease
                else:
                    break
            new_midicents.append(midicent)
        return new_midicents
    elif isinstance(midicents, float):
        while True:
            if midicents <= down:
                midicents = midicents + valueToDecrease
            elif midicents >= up:
                midicents = midicents - valueToDecrease
            else:
                break
        return midicents 
    else:
        pd.error("rangereduce just accepts lists and floats")
        return


# =============================================================================
def modulationnotes(ji_struc1, ji_struc2, cents):
    
    noteFounded = False
    for ji_struc1_note in ji_struc1:
        for ji_struc2_note in ji_struc2:
            distance = abs(ji_struc1_note - ji_struc2_note)
            if (distance < cents):
                noteFounded = True
                pd.print(f"The note {int(ji_struc1_note)} can be modulated to {int(ji_struc2_note)} with a distance of {int(distance)} cents")
    if (noteFounded == False):
        pd.error(f"No note can be modulated with a distance of {int(cents)} cents")


# =============================================================================

def py4pdLoadObjects():

    # Utilities
    pd.add_object(rt2mc, "rt2mc", pyout=True)
    pd.add_object(octavereduce, "octavereduce", pyout=True)
    pd.add_object(rangereduce, "rangereduce", pyout=True)

    # Harry Partch
    pd.add_object(diamond, "diamond", pyout=True)
    pd.add_object(diamond_identities, "diamond-identity", pyout=True)

    # Modulation
    pd.add_object(modulationnotes, "modulationnotes")
    pd.add_object(modulationnotes, "modnotes")

                

