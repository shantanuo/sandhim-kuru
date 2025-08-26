from sanskrit_parser.parser.sandhi import Sandhi
from sanskrit_parser.base.sanskrit_base import SanskritNormalizedString
from indic_transliteration.sanscript import transliterate, SLP1
from sandhi_graph import SandhiGraph
import logging

logger = logging.getLogger("sanskrit_parser.parser.sandhi")
logger.setLevel(logging.INFO)

S = Sandhi()


def sandhi_all(text: str, top_n: int, input_trans: str, output_trans: str) -> list[str]:
    # Transliterate to SLP1 to avoid a lot of conversions
    text_slp = transliterate(text, input_trans, SLP1).strip()
    if text_slp[-1] == ".":
        text_slp = text_slp[:-1]
    words = text_slp.split()

    results = [words[-1]]
    rem = words[:-1]

    depth = 0
    G = SandhiGraph(SLP1, output_trans)
    G.add_node(name=words[-1], depth=0)
    while rem:
        depth += 1
        new_results = []
        left = rem.pop()
        left = SanskritNormalizedString(left, SLP1)
        for right in results:
            parent = right
            right = SanskritNormalizedString(right, SLP1)
            res = S.join(left, right)
            res = res or [""]
            new_results.extend(res)
            for r in res:
                if r:
                    G.add_node(name=r, depth=depth)
                    G.add_edge((parent, r))
        new_results.sort(key=len)
        results = new_results[:top_n]

    for i, r in enumerate(results):
        r_trans = transliterate(r, SLP1, output_trans)
        results[i] = r_trans

    return results, G


if __name__ == "__main__":
    from indic_transliteration.sanscript import DEVANAGARI

    # print(sandhi_all("वेद्यम् पवित्रम् ओम् कारः ऋक्सामयजुः एव", 10, DEVANAGARI, "baraha"))
    # print(sandhi_all("निर्वाणम् ऋच्छति", 10, DEVANAGARI, "baraha"))
    print(
        sandhi_all("तेषाम् नित्य अभियुक्तानाम् योगक्षेमम् वहामि अहम्", 10, DEVANAGARI, "baraha")[0]
    )
