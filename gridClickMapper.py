def getGridLocation(x, y):
    if 140 <= x <= 260 and 100 <= y <= 220:
        return (0, 0)
    elif 270 <= x <= 390 and 100 <= y <= 220:
        return (0, 1)
    elif 400 <= x <= 520 and 100 <= y <= 220:
        return (0, 2)
    elif 140 <= x <= 260 and 230 <= y <= 350:
        return (1, 0)
    elif 270 <= x <= 390 and 230 <= y <= 350:
        return (1, 1)
    elif 400 <= x <= 520 and 230 <= y <= 350:
        return (1, 2)
    elif 140 <= x <= 260 and 360 <= y <= 480:
        return (2, 0)
    elif 270 <= x <= 390 and 360 <= y <= 480:
        return (2, 1)
    elif 400 <= x <= 520 and 360 <= y <= 480:
        return (2, 2)

    elif 730 <= x <= 820 and 410 <= y <= 445:
        return "reset"