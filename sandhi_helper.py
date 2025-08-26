import sandhi
from indic_transliteration.sanscript import transliterate, WX, SCHEMES
from sandhi_graph import SandhiGraph


S = sandhi.Sandhi()
consonants = SCHEMES[WX]["consonants"].values()


def sandhi_all(text: str, top_n: int, input_trans: str, output_trans: str) -> list[str]:
    # Transliterate to WX to avoid a lot of conversions
    text_wx = transliterate(text, input_trans, WX).strip()
    if text_wx[-1] == ".":
        text_wx = text_wx[:-1]
    words = text_wx.split()

    results = [words[-1]]
    rem = words[:-1]

    depth = 0
    G = SandhiGraph(WX, output_trans)
    G.add_node(name=words[-1], depth=0)
    while rem:
        depth += 1
        new_results = []
        left = rem.pop()
        for right in results:
            parent = right
            res = S.sandhi(left, right, WX)
            for r in res:
                if r[2] == "varNamelana" and right[0] in consonants:
                    form = left + " " + right
                else:
                    form = r[0]
                new_results.append(form)
                G.add_node(name=form, depth=depth)
                G.add_edge((parent, form))

        new_results.sort(key=len)
        results = new_results[:top_n]

    for i, r in enumerate(results):
        r_trans = transliterate(r, WX, output_trans)
        results[i] = r_trans

    return results, G
