from sandhi_helper import sandhi_all

if __name__ == "__main__":
    input_text = "तत् लक्ष्मीवान् शुभलक्षणः"
    res = sandhi_all(input_text, 5, "devanagari", "devanagari")
    print(res)