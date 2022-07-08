#skończone
from math import inf


def string_compare(P, T, i, j):
    if i == 0:
        return j
    if j == 0:
        return i

    change = string_compare(P, T, i-1, j-1) + (P[i] != T[j])
    insert = string_compare(P, T, i, j-1) + 1
    delete = string_compare(P, T, i-1, j) + 1

    min_cost = min(change, insert, delete)

    return min_cost


def PD_version(P, T):

    N, M = len(P), len(T)
    D = [[0]*M for _ in range(N)]
    parent = [['X']*M for _ in range(N)]

    for i in range(M):
        D[0][i] = i
        parent[0][i] = 'I'

    for i in range(N):
        D[i][0] = i
        parent[i][0] = 'D'

    parent[0][0] = 'X'

    for i in range(1, N):
        for j in range(1, M):
            change = D[i-1][j-1] + (P[i] != T[j])
            insert = D[i][j-1] + 1
            delete = D[i-1][j] + 1
            min_cost = min(change, insert, delete)
            parent_char = 'X'

            if min_cost == insert:
                parent_char = 'I'
            if min_cost == delete:
                parent_char = 'D'
            if min_cost == change:
                if P[i] != T[j]:
                    parent_char = 'S'
                else:
                    parent_char = 'M'

            D[i][j] = min_cost
            parent[i][j] = parent_char

    return D, parent, D[-1][-1]


def find_path(parent):
    N, M = len(parent), len(parent[0])
    result = []
    act_char = parent[-1][-1]
    act_i, act_j = N-1, M-1
    final_str = ""

    while act_char != 'X':

        if act_char == 'D':
            act_i -= 1
        if act_char == 'M':
            act_i, act_j = act_i-1, act_j-1
        if act_char == 'S':
            act_i, act_j = act_i-1, act_j-1
        if act_char == 'I':
            act_j -= 1

        result.append(act_char)
        act_char = parent[act_i][act_j]

    # odwracanie listy
    result = result[::-1]
    for letter in range(len(result)):
        final_str += result[letter]

    return final_str


def matching_the_substring(P, T):
    N, M = len(P), len(T)
    D = [[0]*M for _ in range(N)]
    parent = [['X']*M for _ in range(N)]

    for i in range(N):
        D[i][0] = i
        parent[i][0] = 'D'

    parent[0][0] = 'X'

    for i in range(1, N):
        for j in range(1, M):
            change = D[i-1][j-1] + (P[i] != T[j])
            insert = D[i][j-1] + 1
            delete = D[i-1][j] + 1
            min_cost = min(change, insert, delete)
            parent_char = 'X'

            if min_cost == insert:
                parent_char = 'I'
            if min_cost == delete:
                parent_char = 'D'
            if min_cost == change:
                if P[i] != T[j]:
                    parent_char = 'S'
                else:
                    parent_char = 'M'

            D[i][j] = min_cost
            parent[i][j] = parent_char

    start_point = goal_cell(D[-1])
    return start_point - N + 2


def goal_cell(lst):
    min_el = lst[0]
    min_idx = 0

    for i in range(1, len(lst)):
        if min_el > lst[i]:
            min_el = lst[i]
            min_idx = i

    return min_idx


def longest_common_sequence(P, T):
    N, M = len(P), len(T)
    D = [[0]*M for _ in range(N)]
    parent = [['X']*M for _ in range(N)]

    for i in range(M):
        D[0][i] = i
        parent[0][i] = 'I'

    for i in range(N):
        D[i][0] = i
        parent[i][0] = 'D'

    parent[0][0] = 'X'

    for i in range(1, N):
        for j in range(1, M):
            change = -1
            if P[i] != T[j]:
                change = inf
            else:
                change = D[i-1][j-1]

            insert = D[i][j-1] + 1
            delete = D[i-1][j] + 1
            min_cost = min(change, insert, delete)
            parent_char = 'X'

            if min_cost == insert:
                parent_char = 'I'
            if min_cost == delete:
                parent_char = 'D'
            if min_cost == change:
                if P[i] != T[j]:
                    parent_char = 'S'
                else:
                    parent_char = 'M'

            D[i][j] = min_cost
            parent[i][j] = parent_char

    return D, parent


# Idea polega na takim samym przechodzeniu po tablicy parent jednak
# zwracamy uwagę tylko na literę M. Kiedy ją napotkamy to aktualny
# indeks kolumny oznacza indeks tesktu T, który musimy dodać do rozwiązania.
# Na koniec analogicznie odrawcamy listę, pakujemy w stringa i otrzymujemy naszą
# najdłuższą wspólną sekwencje.
def find_path_for_longest_common_sequence(T, parent):
    N, M = len(parent), len(parent[0])
    result = []
    act_char = parent[-1][-1]
    act_i, act_j = N-1, M-1
    final_str = ""

    while act_char != 'X':

        if act_char == 'D':
            act_i -= 1
        if act_char == 'M':
            result.append(T[act_j])
            act_i, act_j = act_i-1, act_j-1
        if act_char == 'S':
            act_i, act_j = act_i-1, act_j-1
        if act_char == 'I':
            act_j -= 1

        act_char = parent[act_i][act_j]

    # odwracanie listy
    result = result[::-1]
    for letter in range(len(result)):
        final_str += result[letter]

    return final_str


def create_P_by_sorting_T(T):
    k = sorted(T)
    result, n = '', len(T)

    for i in range(n):
        result += k[i]

    return result


def test_a():
    P = ' kot'
    T = ' pies'
    i, j = len(P)-1, len(T)-1
    print(string_compare(P, T, i, j))


def test_b():
    P = ' biały autobus'
    T = ' czarny autokar'
    _, _, result = PD_version(P, T)
    print(result)


def test_c():
    P = ' thou shalt not'
    T = ' you should not'
    _, parent, _ = PD_version(P, T)
    print(find_path(parent))


def test_d():
    P = ' ban'
    T = ' mokeyssbanana'
    print(matching_the_substring(P, T))


def test_e():
    P = ' democrat'
    T = ' republican'
    _, parent = longest_common_sequence(P, T)
    print(find_path_for_longest_common_sequence(T, parent))


def test_f():
    T = ' 243517698'
    P = create_P_by_sorting_T(T)
    _, parent = longest_common_sequence(P, T)
    print(find_path_for_longest_common_sequence(T, parent))


def main():
    test_a()
    test_b()
    test_c()
    test_d()
    test_e()
    test_f()


if __name__ == "__main__":
    main()