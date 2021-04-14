from PIL import Image, ImageDraw
import numpy as np 
import math
import time
from copy import deepcopy
import random

# TODO: Figure out page type distributions

def create_single_panel_metadata():

    # Coords
    # Dims
    # 
    pass

def test_render(dims):

    W = 1700
    H = 2400
    print(dims)
    page = Image.new(size=(W,H), mode="L", color="white")
    draw_rect = ImageDraw.Draw(page)

    for rect in dims:
        # draw_rect.rectangle(rect, fill=None, outline="white", width=20)
        draw_rect.line(rect, fill="black", width=20)
        # draw_rect.polygon(rect, fill="red", outline="yellow")

    page.show()

def draw_n_shifted(n, topleft, topright, bottomright, bottomleft, horizontal_vertical, shifts=[]):

        # Allow each inital panel to grow to up to 75% of 100/n
        choice_max = round((100/n)*1.5)
        choice_min = round((100/n)*0.5)
        if len(shifts) < 1:
            for i in range(0, n):
                shift_choice = np.random.randint(choice_min, choice_max)
                choice_max = choice_max + ((100/n) - shift_choice)
                shifts.append(shift_choice)
        
        to_add_or_remove = (100 - sum(shifts))/len(shifts)

        normalized_shifts = []
        for shift in shifts:
            new_shift = shift + to_add_or_remove
            normalized_shifts.append(new_shift/100)

        polys = []

        horizontal_vertical = "v"
        if horizontal_vertical == "h":
            shift_level = 0.0 
            for i in range(0, n):
                if i == 0:
                    x1y1 = topleft
                    x2y2 = topright
                else:
                   shift_level += normalized_shifts[i-1]
                   x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*shift_level)
                   x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*shift_level)
                
                if i == (n-1):
                    x3y3 = bottomright
                    x4y4 = bottomleft
                else:
                    next_shift_level = shift_level + normalized_shifts[i]
                    x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*next_shift_level)
                    x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*next_shift_level)

                poly = (x1y1, x2y2, x3y3, x4y4, x1y1)
                polys.append(poly)
        
        if horizontal_vertical == "v":
            shift_level = 0.0 
            for i in range(0, n):
                if i == 0:
                    x1y1 = topleft
                    x4y4 = bottomleft 
                else:
                    shift_level += normalized_shifts[i-1]
                    x1y1 = (topleft[0] + (topright[0] - topleft[0])*shift_level, topright[1])
                    x4y4 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*shift_level, bottomright[1])

                if i == (n-1):
                    x2y2 = topright
                    x3y3 = bottomright
                else:
                    next_shift_level = shift_level + normalized_shifts[i]
                    x2y2 = (topleft[0] + (topright[0] - topleft[0])*next_shift_level, topright[1])
                    x3y3 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*next_shift_level, bottomright[1])

                poly = (x1y1, x2y2, x3y3, x4y4, x1y1)
                polys.append(poly)

        return polys

def draw_n(n, topleft, topright, bottomright, bottomleft, horizontal_vertical):

        polys = []
        
        if horizontal_vertical == "h":
            for i in range(0, n):
                if i == 0:
                    x1y1 = topleft
                    x2y2 = topright
                else:
                   x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(i/n))
                   x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(i/n))
                
                if i == (n-1):
                    x3y3 = bottomright
                    x4y4 = bottomleft
                else:
                    x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*((i+1)/n))
                    x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*((i+1)/n))

                poly = (x1y1, x2y2, x3y3, x4y4, x1y1)
                polys.append(poly)
        
        if horizontal_vertical == "v":
            for i in range(0, n):

                if i == 0:
                    x1y1 = topleft
                    x4y4 = bottomleft 
                else:
                    x1y1 = (topleft[0] + (topright[0] - topleft[0])*(i/n), topright[1])
                    x4y4 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*(i/n), bottomright[1])

                if i == (n-1):
                    x2y2 = topright
                    x3y3 = bottomright
                else:
                    x2y2 = (topleft[0] + (topright[0] - topleft[0])*((i+1)/n), topright[1])
                    x3y3 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*((i+1)/n), bottomright[1])

                poly = (x1y1, x2y2, x3y3, x4y4, x1y1)
                polys.append(poly)

        return polys

def draw_four(topleft, topright, bottomright, bottomleft, horizontal_vertical):

    if horizontal_vertical == "h":
        r1x1y1 = topleft
        r1x2y2 = topright
        r1x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])/4)
        r1x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])/4)

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])/4)
        r2x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])/4)
        r2x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(2/4))
        r2x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(2/4))

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)

        r3x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(2/4))
        r3x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(2/4))
        r3x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(3/4))
        r3x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(3/4))

        poly3 = (r3x1y1, r3x2y2, r3x3y3, r3x4y4, r3x1y1)

        r4x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(3/4))
        r4x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(3/4))
        r4x3y3 = bottomright
        r4x4y4 = bottomleft 

        poly4 = (r4x1y1, r4x2y2, r4x3y3, r4x4y4, r4x1y1)

    
    if horizontal_vertical == "v":
        r1x1y1 = topleft
        r1x2y2 = (topright[0]/4, topright[1])
        r1x3y3 = (bottomright[0]/4, bottomright[1])
        r1x4y4 = bottomleft

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (topright[0]/4, topright[1])
        r2x2y2 = (topright[0]*(2/4), topright[1])
        r2x3y3 = (bottomright[0]*(2/4), bottomright[1])
        r2x4y4 = (bottomright[0]/4, bottomright[1])

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)

        r3x1y1 = (topright[0]*(2/4), topright[1])
        r3x2y2 = (topright[0]*(3/4), topright[1])
        r3x3y3 = (bottomright[0]*(3/4), bottomright[1])
        r3x4y4 = (bottomright[0]*(2/4), bottomright[1])

        poly3 = (r3x1y1, r3x2y2, r3x3y3, r3x4y4, r3x1y1)

        r4x1y1 = (topright[0]*(3/4), topright[1])
        r4x2y2 = topright
        r4x3y3 = bottomright
        r4x4y4 = (bottomright[0]*(3/4), bottomright[1])

        poly4 = (r4x1y1, r4x2y2, r4x3y3, r4x4y4, r4x1y1)
    
    return poly1, poly2, poly3, poly4

# TODO: Add a shifting version of this
def draw_three(topleft, topright, bottomright, bottomleft, horizontal_vertical):

    if horizontal_vertical == "h":
        r1x1y1 = topleft
        r1x2y2 = topright
        r1x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])/3)
        r1x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])/3)

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])/3)
        r2x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])/3)
        r2x3y3 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(2/3))
        r2x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(2/3))

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)

        r3x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*(2/3))
        r3x2y2 = (bottomright[0], topright[1] + (bottomright[1]- topright[1])*(2/3))
        r3x3y3 = bottomright
        r3x4y4 = bottomleft 

        poly3 = (r3x1y1, r3x2y2, r3x3y3, r3x4y4, r3x1y1)

    
    if horizontal_vertical == "v":
        r1x1y1 = topleft
        r1x2y2 = (topright[0]/3, topright[1])
        r1x3y3 = (bottomright[0]/3, bottomright[1])
        r1x4y4 = bottomleft

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (topright[0]/3, topright[1])
        r2x2y2 = (topright[0]*(2/3), topright[1])
        r2x3y3 = (bottomright[0]*(2/3), bottomright[1])
        r2x4y4 = (bottomright[0]/3, bottomright[1])

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)

        r3x1y1 = (topright[0]*(2/3), topright[1])
        r3x2y2 = topright
        r3x3y3 = bottomright
        r3x4y4 = (bottomright[0]*(2/3), bottomright[1])

        poly3 = (r3x1y1, r3x2y2, r3x3y3, r3x4y4, r3x1y1)
    
    return poly1, poly2, poly3

def draw_two_shifted(topleft, topright, bottomright, bottomleft, horizontal_vertical, shift=None):

    if shift is None:
        shift_min = 25
        shift_max = 75
        shift = np.random.randint(shift_min, shift_max)
        shift = shift/100

    if horizontal_vertical == "h":
        r1x1y1 = topleft
        r1x2y2 = topright
        r1x3y3 = (bottomright[0], topright[1] + (bottomright[1] - topright[1])*shift)
        r1x4y4 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*shift)

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (bottomleft[0], topleft[1] + (bottomleft[1] - topleft[1])*shift)
        r2x2y2 = (bottomright[0], topright[1] + (bottomright[1] - topright[1])*shift)
        r2x3y3 = bottomright
        r2x4y4 = bottomleft

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)
    
    if horizontal_vertical == "v":
        
        r1x1y1 = topleft
        r1x2y2 = (topleft[0] + (topright[0] - topleft[0])*shift, topright[1])
        r1x3y3 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*shift, bottomright[1])
        r1x4y4 = bottomleft

        poly1 = (r1x1y1, r1x2y2, r1x3y3, r1x4y4, r1x1y1)

        r2x1y1 = (topleft[0] + (topright[0] - topleft[0])*shift, topright[1])
        r2x2y2 = topright
        r2x3y3 = bottomright
        r2x4y4 = (bottomleft[0] + (bottomright[0] - bottomleft[0])*shift, bottomright[1])

        poly2 = (r2x1y1, r2x2y2, r2x3y3, r2x4y4, r2x1y1)
   
    return poly1, poly2

def invert_for_next(current):
    if current == "h":
        return "v"
    else:
        return "h"

def choose_and_return(choices):

    # Shuffle for random picking
    random.shuffle(choices)

    # Pop one after shuffling
    choice = choices.pop(0)

    return choice, choices

def create_page_metadata():

    # Select page type
    # Select number of panels on the page
        # between 1 and 8
    # Select panel boundary type
    # Select panel boundary widths

    # Each page is a 2x4 grid

    panel_dims = []

    layout_type = "vh"

    # TODO: Rehaul this to be more standardized
    if layout_type == "v":
        max_num_panels = 4

        # Doesn't guarantee this number due to edge cases and fitting
        num_panels = np.random.randint(1, max_num_panels+1)

        panel_widths = {}
        # Randomly increase or decrease each panel by "x%"
        panel_width_default = 425
        if num_panels > 1:
            for panel in range(0, num_panels-1):

                change = np.random.randint(-50,50)
                pw = round(panel_width_default*(1 - (change/100)), -1)
                panel_widths[panel] = pw 

        # Deal with exceeding width
        total_widths = sum(panel_widths.values())
        if total_widths > 1700:
            extra_width = total_widths - 1700
            to_remove = math.ceil(extra_width/len(panel_widths))
            # divide it amongst the panels
            for panel in panel_widths:
                panel_widths[panel] = (panel_widths[panel] - to_remove)

        last_pw = 1700 - total_widths 
        if last_pw> 0:
            panel_widths[len(panel_widths)] = last_pw 

        panel_coords = []
        current_axis_location = 0        
        for panel in panel_widths:
            x1 = current_axis_location
            y1 = 0.0

            x2 = current_axis_location + panel_widths[panel]
            y2 = 2400

            current_axis_location = x2

            coord = ((x1, y1), (x2, y2))
            panel_coords.append(coord)
        
    # TODO: Rehaul this to be more standardized
    elif layout_type == "h":
        max_num_panels = 6

        num_panels = np.random.randint(1, max_num_panels+1)

        panel_heights = {}
        # Randomly increase or decrease each panel by "x%"
        panel_height_default = 600
        if num_panels > 1:
            for panel in range(0, num_panels-1):

                change = np.random.randint(-25,25)
                ph = round(panel_height_default*(1 - (change/100)), -1)
                panel_heights[panel] = ph 

        # Deal with exceeding height
        total_heights = sum(panel_heights.values())
        if total_heights > 2400:
            extra_height = total_heights - 2400
            to_remove = math.ceil(extra_height/len(panel_heights))
            # divide it amongst the panels
            for panel in panel_heights:
                panel_heights[panel] = (panel_heights[panel] - to_remove)

        last_ph = 2400 - total_heights
        if last_ph> 0:
            panel_heights[len(panel_heights)] = last_ph

        panel_coords = []
        current_axis_location = 0.0 
        for panel in panel_heights:
            x1 = 0.0 
            y1 = current_axis_location

            x2 = 1700
            y2 = current_axis_location + panel_heights[panel]

            current_axis_location = y2

            coord = ((x1, y1), (x2, y2))
            panel_coords.ppend(coord)
    
    elif layout_type == "vh":
        
        max_num_panels = 8
        # num_panels = np.random.randint(2, max_num_panels+1)
        num_panels = 5

        topleft = (0.0, 0.0)
        topright = (1700, 0.0)
        bottomleft = (0.0, 2400)
        bottomright = (1700, 2400)
        dims = [
            topleft,
            topright,
            bottomright,
            bottomleft
        ]

        if num_panels == 2:
            # Draw 2 rectangles
                # vertically or horizontally
            horizontal_vertical = np.random.choice(["h", "v"])
            p1, p2 = draw_two_shifted(*dims, horizontal_vertical)
            ret_list = [p1, p2]
            test_render(ret_list)
    
        if num_panels == 3:
            # Draw 2 rectangles
                # Vertically or Horizontally

            horizontal_vertical = np.random.choice(["h", "v"])
            p1, p2 = draw_two_shifted(*dims, horizontal_vertical)

            next_div = invert_for_next(horizontal_vertical)

            ret_list = []

            # Pick one and divide it into 2 rectangles
            choice, left_choices = choose_and_return([p1, p2])

            p3, p4 = draw_two_shifted(*choice[0:4], next_div)
            ret_list = left_choices + [p3, p4]

            test_render(ret_list)

        if num_panels == 4:

            ret_list = []
            horizontal_vertical = np.random.choice(["h", "v"])
            type_choice = np.random.choice(["eq", "uneq", "div", "trip"]) 

            # Draw two rectangles 
            if type_choice == "eq":
                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)

                # Divide each into 2 rectangles equally
                shift_min = 25
                shift_max = 75
                shift = np.random.randint(shift_min, shift_max)
                shift = shift/100 

                p3, p4 = draw_two_shifted(*p1[0:4], next_div, shift)
                p5, p6 = draw_two_shifted(*p2[0:4], next_div, shift)
                ret_list = [p3, p4, p5, p6]

            # Divide each into 2 rectangles unequally
            elif type_choice == "uneq":
                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)

                p3, p4 = draw_two_shifted(*p1[0:4], next_div)
                p5, p6 = draw_two_shifted(*p2[0:4], next_div)
                ret_list = [p3, p4, p5, p6]

            elif type_choice == "div":
                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)
                pick_one = np.random.random()
                # Pick one and divide into 2 rectangles
                choice1, left_choices1 = choose_and_return([p1, p2]) 
                p3, p4 = draw_two_shifted(*choice1[0:4], next_div)

                # Pick one of these two and divide that into 2 rectangles
                choice2, left_choices2 = choose_and_return([p3, p4])
                next_div = invert_for_next(next_div)
                p5, p6 = draw_two_shifted(*choice2[0:4], next_div)

                ret_list = left_choices1 + left_choices2 + [p5, p6]
            
            # Draw three rectangles
            elif type_choice == "trip":
                p1, p2, p3 = draw_three(*dims, horizontal_vertical)

                # Pick one and divide it into two
                choice, left_choices = choose_and_return([p1, p2, p3])
                next_div = invert_for_next(horizontal_vertical)
                p4, p5 = draw_two_shifted(*choice[0:4], next_div)

                ret_list = left_choices + [p4, p5]
                
            test_render(ret_list)
                    
        
        if num_panels == 5:

            ret_list = []
            # Draw two rectangles 
            horizontal_vertical = np.random.choice(["h", "v"])
            
            type_choice = np.random.choice(["eq", "uneq", "div", "2-(2+3)", "3-(2+2+1)", "4-(2+(3x1))"])
            type_choice = "4-(2+(3x1))"
            if type_choice == "eq" or type_choice == "uneq":

                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)

                # Pick one and divide it into two then
                choice, left_choices = choose_and_return([p1, p2])
                p3, p4 = draw_two_shifted(*choice[0:4], next_div)                    

                # Divide each into 2 rectangles equally
                if type_choice == "eq":
                    shift_min = 25
                    shift_max = 75
                    shift = np.random.randint(shift_min, shift_max) 
                    set_shift = shift/100
                else:
                    # Divide each into 2 rectangles unequally
                    set_shift = None

                next_div = invert_for_next(next_div)
                p5, p6 = draw_two_shifted(*p3[0:4], next_div, shift=set_shift)
                p7, p8 = draw_two_shifted(*p4[0:4], next_div, shift=set_shift)
                ret_list = left_choices + [p5, p6, p7, p8]


            # Draw two rectangles
            elif type_choice == "div":
                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)

                # Divide both equally
                p3, p4 = draw_two_shifted(*p1[0:4], next_div)
                p5, p6 = draw_two_shifted(*p2[0:4], next_div)

                # Pick one of all of them and divide into two
                choice, left_choices = choose_and_return([p3, p4, p5, p6])
                next_div = invert_for_next(next_div)
                p7, p8 = draw_two_shifted(*choice[0:4], horizontal_vertical=next_div, shift=0.5)

                ret_list = left_choices + [p7, p8]
        
            # Draw two rectangles
            elif type_choice == "2-(2+3)":
                
                p1, p2 = draw_two_shifted(*dims, horizontal_vertical, shift=0.5)
                next_div = invert_for_next(horizontal_vertical)

                # Pick which one gets 2 and which gets 3 
                choice, left_choices = choose_and_return([p1, p2])
                other = left_choices[0]

                # Divide one into 2
                next_div = invert_for_next(horizontal_vertical)
                p3, p4 = draw_two_shifted(*choice[0:4], next_div)

                # Divide other into 3
                p5, p6, p7 = draw_three(*other[0:4], next_div)

                ret_list = [p3, p4, p5, p6, p7]

            # Draw 3 rectangles (horizontally or vertically)
            elif type_choice == "3-(2+2+1)":

                p1, p2, p3 = draw_three(*dims, horizontal_vertical)
                next_div = invert_for_next(horizontal_vertical)

                choice1, left_choices1 = choose_and_return([p1, p2, p3])
                choice2, left_choices2 = choose_and_return(left_choices1)

                # Pick two and divide each into two
                p4, p5 = draw_two_shifted(*choice1[0:4], next_div)
                p6, p7 = draw_two_shifted(*choice2[0:4], next_div)

                ret_list = left_choices2 + [p4, p5, p6, p7]
            
            # Draw 4 rectangles vertically
            elif type_choice == "4-(2+(3x1))":
                # p1, p2, p3, p4 = draw_four(*dims, horizontal_vertical)

                # # Pick one and divide into two
                # choice, left_choices = choose_and_return([p1, p2, p3, p4])
                # next_div = invert_for_next(horizontal_vertical)
                # p5, p6 = draw_two_shifted(*choice[0:4], next_div)

                # ret_list = left_choices + [p5, p6]

                # ret_list = draw_n(4, *dims, horizontal_vertical)
                ret_list = draw_n_shifted(2, *dims, horizontal_vertical)

            test_render(ret_list) 

           

            pass

        if num_panels == 6:

            # 2 V 1 H
            # 2 H 1 V

            combo1 = dict(
                full_vertical_lines = 2,
                full_horizontal_lines = 1
            )

            combo2 = dict(
                full_vertical_lines = 1,
                full_horizontal_lines = 2
            )

            # 5 in one half
            combo3 = dict(
                full_vertical_lines = 1,
                combo_of_five = None

            )

            combo4 = dict(
                full_horizontal_lines = 1,
                combo_of_five = None
            )

            # 3 in both halves
            combo5 = dict(
                full_vertical_lines = 1,
                combo_of_three_one = None,
                combo_of_three_two = None

            )

            combo6 = dict(
                full_horizontal_lines = 1,
                combo_of_three_one = None,
                combo_of_three_two = None
            )


            # 2 in 3 parts
            combo7 = dict(
                full_vertical_lines = 3,
                half_lines = 3
            )
            combo8 = dict(
                full_horizontal_lines = 3,
                half_lines = 3
            )

            # 4 in one half 
            # 2 in another
            combo9 = dict(
                full_vertical_lines = 1,
                combo_of_four = None,
                half_line = 1

            )

            combo10 = dict(
                full_horizontal_lines = 1,
                combo_of_four = None,
                half_line = 1
            )
        if num_panels == 7:

            # Combo of 6 plus one extra half line
            pass
            
        if num_panels == 8:
            combo1 = dict(
                full_vertical_lines = 1,
                full_horizontal_lines = 3
            )

            combo2 = dict(
                full_vertical_lines = 3,
                full_horizontal_lines = 1
            )

            # Combo of 6 plus 2 extra half lines

            # 2 combos of 4
            # one combo of 2 one combo of 6
            # two combos of 3 one combo of two
            # one combo fof 5 one combo of 3


     