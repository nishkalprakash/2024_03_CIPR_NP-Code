# desc: functions for performing indirect feature extraction on minutiae triplet array
# input: triplet array
# output: feature vector array

import numpy as np

def ret_arr(triplet_array):
    # return values in final_array
    final_array = []

    def calc_log_ratio(x, y):
        # Calculate the log ratio of two numbers with base 2
        return np.log2(np.abs(x / y))
    
    def calc_area(triplet):
        # Calculate the area of the triangle
        # area = |(x1-x3)(y2-y1) - (x1-x2)(y3-y1)|/2
        return 0.5 * np.abs((triplet[0][0] - triplet[2][0]) * (triplet[1][1] - triplet[0][1]) - (triplet[0][0] - triplet[1][0]) * (triplet[2][1] - triplet[0][1]))
    
    def calc_line(point):
        # calculate intercept and slope of line passing through x,y with angle theta radians
        # b = y - mx
        # return line as tuple (m,b)
        # angles are in radian
        m = np.tan(point[2])
        b = point[1] - m*point[0]
        return (m,b)
    
    def calc_edges(triplet):
        # calculate slope of edges of triangle
        # return tuple of angles
        # input is triplet of points
        # calculate tan inverse of slope of edges
        # edge 1
        m1 = (triplet[1][1] - triplet[0][1])/(triplet[1][0] - triplet[0][0])
        theta1 = np.arctan(m1)
        # edge 2
        m2 = (triplet[2][1] - triplet[1][1])/(triplet[2][0] - triplet[1][0])
        theta2 = np.arctan(m2)
        # edge 3
        m3 = (triplet[0][1] - triplet[2][1])/(triplet[0][0] - triplet[2][0])
        theta3 = np.arctan(m3)
        return (theta1, theta2, theta3)
    
    def calc_rel_angle(triplets):
        tuple = calc_edges(triplets)
        # convert negative angles to positive
        theta = []
        for i in range(len(tuple)):
            if tuple[i] < 0:
                theta.append(tuple[i] + np.pi)
            else:
                theta.append(tuple[i])
        
        for i in range(3):
            if triplets[i][2] < 0:
                triplets[i][2] = triplets[i][2] + np.pi
        # find relative angle
        rel = []
        for i in range(3):
            temp = np.pi
            for j in range(3):
                temp = min(temp, np.abs(theta[i] - triplets[j][2]))
            rel.append(temp)
        rel.sort()
        return rel

    
    def find_intercept(line1, line2):
        # find intercept of two lines
        # x = (b2 - b1)/(m1 - m2)
        # y = m1*x + b1
        x = (line2[1] - line1[1])/(line1[0] - line2[0])
        y = line1[0]*x + line1[1]
        return (x,y)
    
    def build_tuple(v1, v2, v3):
        # vi are coordinates of triangle vertices
        # generate a 3*2 array tuple of coordinates
        # build tuple from three values
        return (v1, v2, v3)
    
    def calc_area2(triplet):
        # input is triplet of lines
        # sancheck for parallel lines
        if triplet[0][0] == triplet[1][0] or triplet[0][0] == triplet[2][0] or triplet[1][0] == triplet[2][0]:
            return float('inf')
        else:
            # find intercepts
            intercept1 = find_intercept(triplet[0], triplet[1])
            intercept2 = find_intercept(triplet[0], triplet[2])
            intercept3 = find_intercept(triplet[1], triplet[2])
            # calculate area
            area = 0.5 * np.abs((intercept1[0] - intercept3[0]) * (intercept2[1] - intercept1[1]) - (intercept1[0] - intercept2[0]) * (intercept3[1] - intercept1[1]))
            return area

    
    # for each triplet in triplet_array, calculate area
    # calculate line intercepts
    # calculate area of triangle formed by line intercept
    # calculate log ratio of areas
    # triplet_array is a array of 3*3 array of triplets

    for i in range (len(triplet_array)):
        # calculate area of triangle formed by triplet
        area = calc_area(triplet_array[i])
        # calculate line intercepts
        line1 = calc_line(triplet_array[i][0])
        line2 = calc_line(triplet_array[i][1])
        line3 = calc_line(triplet_array[i][2])
        # build tuple
        triplet = build_tuple(line1, line2, line3)
        # calculate area
        area2 = calc_area2(triplet)
        print(area2, area)
        # calculate log ratio
        log_ratio = calc_log_ratio(area2, area)
        # calculate relative angle
        rel_angle = calc_rel_angle(triplet_array[i])
        # append to final_array
        final_array.append([log_ratio, rel_angle[0], rel_angle[1], rel_angle[2]])

    # sort the final_array
    final_array.sort()

    return final_array