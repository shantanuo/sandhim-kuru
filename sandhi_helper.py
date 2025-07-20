import sandhi
from indic_transliteration.sanscript import transliterate, WX

S = sandhi.Sandhi()


def sandhi_all(text: str, top_n: int, input_trans: str, output_trans: str) -> list[str]:
    # Transliterate to WX to avoid a lot of conversions
    text_wx = transliterate(text, input_trans, WX).strip()
    if text_wx[-1] == ".":
        text_wx = text_wx[:-1]
    words = text_wx.split()

    results = [words[0]]
    rem = words[1:]

    while rem:
        new_results = []
        right = rem.pop(0)
        for left in results:
            res = S.sandhi(left, right, WX)
            for r in res:
                new_results.append(r[0])
        new_results.sort(key=len)
        results = new_results[:top_n]

    for i, r in enumerate(results):
        # Note - Z in WX can represent avagraha for Sanskrit
        # https://en.wikipedia.org/wiki/WX_notation#Anusv%C4%81ra_and_visarga
        r = r.replace("Z", "'").replace("><", "≍")
        r_trans = transliterate(r, WX, output_trans)
        results[i] = r_trans

    return results
