#bad - NEEDS to be 3 strings to enter
def join_text_bad(text1: str, text2: str, text3: str, *, sep: str) -> str:
    return sep.join([text1, text2, text3])

#good - * can enter as many strings as you want
def join_text_good(*strings, sep: str) -> str:
    return sep.join(strings)

def main() -> None:
    print(join_text_bad('A', 'B', 'C', sep = '-'))
    print(join_text_good('A', sep = '-'))
    print(join_text_good('A', 'b', 'C', 'D', 'E', sep = '-'))
    
if __name__ == '__main__':
    main()