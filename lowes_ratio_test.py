import cv2


# returns 2nd highest value / highest value of corr_map
def get_ratio(corr_map, height, width):
    # get highest corr value
    _, max_val, _, max_loc = cv2.minMaxLoc(corr_map)

    # black out surrounding correlation peak, .25 the size of the template
    radius = int(min(height, width) / 4)
    cv2.circle(corr_map, max_loc, radius, 0, -1)

    # get second highest corr value
    _, max_val2, _, _ = cv2.minMaxLoc(corr_map)
    return max_val2 / max_val


