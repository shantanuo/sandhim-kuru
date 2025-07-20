from collections import deque
import sandhi
from indic_transliteration.sanscript import transliterate, WX
    
S = sandhi.Sandhi()

def sandhi_all(text: str, top_n:int, input_trans:str, output_trans:str) -> list[str]:
    # Transliterate to WX to avoid a lot of conversions
    text_wx = transliterate(text, input_trans, WX)
    words = text_wx.split()
    q  = deque()
    q.append((words[0], tuple(words[1:])))

    results = []

    while q:
        left, right = q.popleft()
        if right:
            first_right = right[0]
            rem = right[1:]
            res = S.sandhi(left, first_right, WX)
            for r in res:
                q.append((r[0], rem))
        else:
            left = left.replace("Z", "ऽ")
            left_trans = transliterate(left, WX, output_trans)
            results.append(left_trans)
            
    return results