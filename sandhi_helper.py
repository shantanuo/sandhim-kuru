from collections import deque
import sandhi
    
S = sandhi.Sandhi()

def sandhi_all(text: str) -> list[str]:
    words = text.split()
    q  = deque()
    q.append((words[0], tuple(words[1:])))

    results = []

    while q:
        left, right = q.popleft()
        if right:
            first_right = right[0]
            rem = right[1:]
            res = S.sandhi(left, first_right)
            for r in res:
                q.append((r[0], rem))
        else:
            results.append(left.replace("Z", "ऽ"))
            
    return results