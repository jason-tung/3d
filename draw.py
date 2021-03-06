from display import *
from matrix import *
import math

  # ====================
  # add the points for a rectagular prism whose 
  # upper-left corner is (x, y, z) with width, 
  # height and depth dimensions.
  # ====================
def add_box( points, x, y, z, width, height, depth ):
    #add_edge(points, x, y, z, x, y, z)
    add_edge(points, x, y, z, x + width, y, z)
    add_edge(points, x, y, z, x, y, z- depth)
    add_edge(points, x, y, z, x, y - height, z)
    add_edge(points, x + width, y, z, x + width, y, z - depth)
    add_edge(points, x + width, y, z, x + width, y - height, z)
    add_edge(points, x + width, y, z - depth, x, y, z - depth)
    add_edge(points, x + width, y, z - depth, x + width, y - height, z - depth)
    add_edge(points, x, y - height, z, x, y - height, z - depth)
    add_edge(points, x, y, z - depth, x, y - height, z - depth)
    add_edge(points, x, y - height, z - depth, x + width, y - height, z - depth)
    add_edge(points, x + width, y - height, z - depth, x + width, y - height, z)
    add_edge(points, x + width, y - height, z, x, y - height, z)
    

  # ====================
  # Generates all the points along the surface
  # of a sphere with center (cx, cy, cz) and
  # radius r.
  # Returns a matrix of those points
  # ====================
def generate_sphere( points, cx, cy, cz, r, step ):
    nmat = []
    for phi in range(30):
        phi = phi * 2 * math.pi/30
        for theta in range(30):
            theta = theta * 2 * math.pi / 30
            x = r*math.cos(theta) + cx
            y = r*math.sin(theta)*math.cos(phi) + cy
            z = r*math.sin(theta)*math.sin(phi) + cz
            add_point(nmat, x, y, z)
    return nmat

  # ====================
  # adds all the points for a sphere with center 
  # (cx, cy, cz) and radius r to points
  # should call generate_sphere to create the
  # necessary points
  # ====================
def add_sphere( points, cx, cy, cz, r, step ):
    nmat = generate_sphere( points, cx, cy, cz, r, step )
    for x in nmat:
        add_edge(points, x[0], x[1], x[2], x[0] +1, x[1] +1, x[2]+1)


  # ====================
  # Generates all the points along the surface
  # of a torus with center (cx, cy, cz) and
  # radii r0 and r1.
  # Returns a matrix of those points
  # ====================
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    nmat = []
    for phi in range(30):
        phi = phi * 2 * math.pi/30
        for theta in range(30):
            theta = theta * 2 * math.pi / 30
            x = math.cos(phi) * (r0 * math.cos(theta) + r1) + cx
            y = r0 * math.sin(theta) + cy
            z = -math.sin(phi) * (r0 * math.cos(theta) + r1) + cz
            add_point(nmat, x, y, z)
    return nmat

  # ====================
  # adds all the points for a torus with center
  # (cx, cy, cz) and radii r0, r1 to points
  # should call generate_torus to create the
  # necessary points
  # ====================
def add_torus( points, cx, cy, cz, r0, r1, step ):
    nmat = generate_torus(points, cx, cy, cz, r0, r1, step)
    for x in nmat:
        add_edge(points, x[0], x[1], x[2], x[0] + 1, x[1] + 1, x[2] + 1)



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    stepper = step
    xc = generate_curve_coefs(x0,x1,x2,x3, curve_type)
    yc = generate_curve_coefs(y0,y1,y2,y3, curve_type)
    while stepper <= step + 1:
        nx0 = 0
        ny0 = 0
        nx1 = 0
        ny1 = 0
        for x in range(4):
            nx0 += xc[0][x] * stepper**(3-x)
            ny0 += yc[0][x] * stepper**(3-x)
            nx1 += xc[0][x] * (stepper-step)**(3-x)
            ny1 += yc[0][x] * (stepper-step)**(3-x)
        add_edge(points, nx0, ny0, 0, nx1, ny1, 0)
        stepper+=step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
