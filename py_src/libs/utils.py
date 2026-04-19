import math

def point_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def direction_of_travel(point_start, point_end):
    direction = ''
    rise = point_end[1] - point_start[1]
    run = point_end[0] - point_start[0]

    if run < 1 and rise < 1:
        direction = 'top-left'
    elif run < 1 and rise > 1:
        direction = 'bottom-left'
    elif run > 1 and rise < 1:
        direction = 'top-right'
    elif run > 1 and rise > 1:
        direction = 'bottom-right'

    if run != 0 and abs(rise / run) < 0.3:
        if run > 1:
            direction = 'right'
        else:
            direction = 'left'

    return direction
