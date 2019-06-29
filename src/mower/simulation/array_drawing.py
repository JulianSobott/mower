import numpy as np

from mower.utils.types import Point


def example():
    data = np.zeros((10, 10))
    add_line_data((0, 4), (3, 4), 5, data, 1)
    print(data)


def trapez(y, y0, w):
    return np.clip(np.minimum(y + 1 + w / 2 - y0, -y + 1 + w / 2 + y0), 0, 1)


def add_line_data(pos1: Point, pos2: Point, thickness: int, data: np.array, data_val: int):
    # The algorithm below works fine if pos2[0] >= pos1[0] and pos2[0]-pos1[0] >= abs(pos2[1]-pos1[1]).
    # If either of these cases are violated, do some switches.
    rmin = 0
    rmax = np.inf
    if abs(pos2[0] - pos1[0]) < abs(pos2[1] - pos1[1]):
        # Switch x and y, and switch again when returning.
        pos1 = (pos1[1], pos1[0])
        pos2 = (pos2[1], pos2[0])
        return add_line_data(pos1, pos2, thickness, data, data_val)

    # At this point we know that the distance in columns (x) is greater
    # than that in rows (y). Possibly one more switch if pos1[0] > pos2[0].
    if pos1[0] > pos2[0]:
        return add_line_data(pos1, pos2, thickness, data, data_val)

    # The following is now always < 1 in abs
    try:
        slope = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
    except ZeroDivisionError:
        slope = 0.1
    # Adjust weight by the slope
    thickness *= np.sqrt(1 + np.abs(slope)) / 2

    # We write y as a function of x, because the slope is always <= 1
    # (in absolute value)
    x = np.arange(pos1[0], pos2[0] + 1, dtype=float)
    y = x * slope + (pos2[0] * pos1[1] - pos1[0] * pos2[1]) / (pos2[0] - pos1[0])

    # Now instead of 2 values for y, we have 2*np.ceil(w/2).
    # All values are 1 except the upmost and bottommost.
    thickness = np.ceil(thickness / 2)
    yy = (np.floor(y).reshape(-1, 1) + np.arange(-thickness - 1, thickness + 2).reshape(1, -1))
    xx = np.repeat(x, yy.shape[1])
    vals = trapez(yy, y.reshape(-1, 1), thickness).flatten()

    yy = yy.flatten()

    # Exclude useless parts and those outside of the interval
    # to avoid parts outside of the picture
    mask = np.logical_and.reduce((yy >= rmin, yy < rmax, vals > 0))

    data[yy[mask].astype(int), xx[mask].astype(int)] = data_val
    return


if __name__ == '__main__':
    example()