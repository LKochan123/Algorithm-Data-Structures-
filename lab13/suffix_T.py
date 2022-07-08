# skończone

def create_all_suffix(word):
    dct, dct2, n = {}, {}, len(word)
    for i in range(n):
        dct[word[i:]] = i
        dct2[i] = word[i:]
    return dct, dct2


def sort_suffix_table(table):
    words_lst = [word for word in table.keys()]
    words_lst_sorted = sorted(words_lst, key=str.lower)
    idx_lst = []

    for word in words_lst_sorted:
        idx_lst.append(table[word])

    return idx_lst


# True - jeśli znajdzie wybrany wzorzec
# False - jeśli NIE znajdzie
def find_word_by_binary_search(word, suffix_table, reversed_HT):
    left, right = 0, len(suffix_table) - 1

    while left <= right:
        mid = (left + right) // 2
        if reversed_HT[suffix_table[mid]] == word:
            return True
        if reversed_HT[suffix_table[mid]].lower() > word.lower():
            right = mid - 1
        else:
            left = mid + 1

    return False


def main():
    banana = "banana\0"
    table, revered_table = create_all_suffix(banana)
    suffix_table = sort_suffix_table(table)
    test1, test2 = 'ana\0', 'banba\0'
    result_test1 = find_word_by_binary_search(test1, suffix_table, revered_table)
    result_test2 = find_word_by_binary_search(test2, suffix_table, revered_table)
    print(f'Słowo: {banana}')
    print(suffix_table)
    print(f'Szukany wzorzec {test1}: {result_test1}')
    print(f'Szukany wzorzec {test2}: {result_test2}')


if __name__ == '__main__':
    main()
