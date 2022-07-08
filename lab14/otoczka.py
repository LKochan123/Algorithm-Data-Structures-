#skończone

def choose_starting_coords(points):
    x, y = points[0]
    n = len(points)

    for point in range(n):
        xi, yi = points[point]
        if xi < x:
            x, y = xi, yi
        if xi == x and yi < y:
            x, y = xi, yi

    return x, y


def find_Q_point(Px, Py, points):
    N = len(points)

    for i in range(N):
        if i == N-1:
            return points[0]
        pX, pY = points[i]
        if Px == pX and Py == pY:
            return points[i+1]


def left_or_right_handed(p, q, r):
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r

    value = (y2 - y1)*(x3 - x2) - (y3 - y2)*(x2 - x1)

    if value > 0:
        return 'R'
    elif value < 0:
        return 'L'
    else:
        return 'W'


def check_if_q_is_between_pr(P, Q, R):
    px, py = P
    qx, qy = Q
    rx, ry = R

    # Uwzględniamy przypadki w obie strony
    if px < qx < rx or py < qy < ry:
        return True
    if rx < qx < px or ry < qy < py:
        return True
    return False


def Jarvis(points, version):
    # version -> 0: początkowa wersja, 1: ulepszona wersja
    start_point = choose_starting_coords(points)
    good_points = []
    P = start_point
    run = True

    while run:
        good_points.append(P)
        px, py = P
        Q = find_Q_point(px, py, points)
        for R in points:
            if left_or_right_handed(P, Q, R) == 'R':
                Q = R
            if version:
                if left_or_right_handed(P, Q, R) == 'W' and \
                        check_if_q_is_between_pr(P, Q, R):
                    Q = R

        P = Q
        if P == start_point:
            run = False

    return good_points


def main():
    POINTS = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    version_0 = Jarvis(POINTS, 0)
    version_1 = Jarvis(POINTS, 1)
    print(version_0)
    print(version_1)


if __name__ == "__main__":
    main()
