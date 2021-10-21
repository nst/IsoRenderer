#!/usr/bin/env python3
# Nicolas Seriot
# 2021-10-02
# A 2D, Cairo-based isometric renderer in Python 3
# https://github.com/nst/IsoRenderer

import cairo
import numpy as np

MARGIN = 40
DW, DH = 28, 14 # diamond size
DW2, DH2 = int(DW/2), int(DH/2)

def draw_surface(c, points, color, vertices = []):
    
    c.save()

    c.set_source_rgb(*color)
    
    [c.line_to(*p) for p in points]

    c.fill()
    
    c.set_source_rgb(0,0,0)
    c.set_line_width(1)
    
    for pts in vertices:
        p1, p2 = pts
        c.move_to(*p1)
        c.line_to(*p2)
        c.stroke()
    
    c.restore()

def draw_world_box(c, shape, front=False, back=False):

    """
          5
    2         6
        3 8       <- 3 front, 8 back
    1         7 
        4
    """

    X_MAX, Y_MAX, Z_MAX = shape

    o_x = DW2 * Y_MAX
    o_y = DH2

    p1 = (0, Y_MAX*DH2)
    p2 = (0, p1[1] + DH*Z_MAX)
    p3 = (Y_MAX*DW2, DH*Z_MAX)
    p4 = (p3[0], 0)
    p5 = (X_MAX*DW2, (X_MAX+Y_MAX)*DH2 + Z_MAX*DH)
    p6 = ((X_MAX + Y_MAX) * DW2, X_MAX*DH2 + Z_MAX*DH)
    p7 = (p6[0], X_MAX*DH2)
    p8 = (p5[0], (X_MAX+Y_MAX)*DH2)
    
    c.save()

    c.set_source_rgb(0,0,0)
    c.set_line_width(1)

    if back:

        [c.line_to(*p) for p in [p5, p8]]
        c.stroke()

        [c.line_to(*p) for p in [p1, p8, p7]]
        c.stroke()

    if front:

        [c.line_to(*p) for p in [p1, p2, p5, p6, p7, p4, p1]]
        c.stroke()
    
        [c.line_to(*p) for p in [p2, p3, p6]]
        c.stroke()
    
        [c.line_to(*p) for p in [p3, p4]]
        c.stroke()
    
    c.restore()

def draw_cube(c, shape, x, y, z,
              nx = False, nx_ = False, ny = False, ny_ = False, nz = False, nz_ = False,
              nxy_=False, nxz = False, nx_z_ = False, nyz = False, ny_z_ = False,
              flat=False):
    
    X_MAX, Y_MAX, Z_MAX = shape
    
    x, y = (DW2 * (Y_MAX-1) + DW2*(x-y), DH2*(x+y))

    z_offset = DH * z
    
    c.save()

    c.translate(x, y + z_offset)

    """
      5
    2   6
      3      - DH
    1   7
      4
      | z_offset
    """
    

    p1 = (0,   DH2)
    p2 = (0,   DH2 + DH)
    p3 = (DW2, DH)
    p4 = (DW2, 0)
    p5 = (DW2, 2*DH)
    p6 = (DW,  DH2 + DH)
    p7 = (DW,  DH2)
    
    #COLOR_RIGHT = (0.5,0.5,0.5)
    #COLOR_TOP = (1,1,1)
    #COLOR_LEFT = (0,0,0)
    
    z_ratio = 0.4 + z*0.6/Z_MAX
    
    COLOR_TOP   = (1 * z_ratio,   0.5 * z_ratio, 0.5 * z_ratio)
    COLOR_LEFT  = (0.6 * z_ratio, 0,             0)
    COLOR_RIGHT = (1 * z_ratio,   0,             0)

    
    if flat:
        vertices = [(p1,p3), (p3,p7), (p7,p4), (p4,p1)]
        draw_surface(c, [], (1,1,1), vertices)
    else:
        vertices_x = []
        vertices_y = []
        vertices_z = []
        
        if (not nx and not nz) or (nx and nxz):
            vertices_z.append((p5, p6))
        if (not nx and not ny_) or (nx and nxy_):
            vertices_x.append((p6, p7))
        if (not ny and not nz) or (ny and nyz):
            vertices_z.append((p2, p5))
        if (not nz_ and not nx_) or (nz_ and nx_z_):
            vertices_y.append((p1, p4))
        if not ny and not nx_:
            vertices_y.append((p2, p1))
        if not nz_ and not ny_:
            vertices_x.append((p4, p7))
        if not nx_ and not ny_:
            v = (p3, p4)
            vertices_y.append(v)
        if not nz and not ny_:
            v = (p6, p3)
            vertices_z.append(v)
        if not nz and not nx_:
            v = (p2, p3)
            vertices_z.append(v)
        
        if not ny_:
            draw_surface(c, [p3, p6, p7, p4], COLOR_RIGHT, vertices_x)
        
        if not nx_:
            draw_surface(c, [p1, p2, p3, p4], COLOR_LEFT, vertices_y)
        
        if not nz:
            draw_surface(c, [p2, p5, p6, p3], COLOR_TOP, vertices_z)
    
    c.restore()

def visibility_matrix(m):

    X,Y,Z = m.shape

    # nothing is visible except the three visible faces of the space

    v = np.full(m.shape, False)

    for x in range(X):
        for y in range(Y):
            v[x][y][Z-1] = True

    for x in range(X):
        for z in range(Z):
            v[x][0][z] = True

    for y in range(Y):
        for z in range(Z):
            v[0][y][z] = True

    # iterate from user's standpoint
    
    for x in range(X):
        for y in range(Y):
            for z in range(Z)[::-1]:

                # if not visible
                # no need to update visibility of "back" cube
                # continue to the next cube
                if not v[x][y][z]:
                    continue

                # if m is empty
                # "back" cube becomes visible
                if not m[x][y][z]:
                    if x < (X-1) and y < (Y-1) and z > 0:
                        v[x+1][y+1][z-1] = True
        
    return v

def is_neighbour(m,x,y,z,a,b,c):

    X,Y,Z = m.shape
    
    offset_is_valid = 0 <= (x+a) < X and 0 <= (y+b) < Y and 0 <= (z+c) < Z
    if not offset_is_valid:
        return False
    
    oid = m[x,y,z]
    
    noid = m[x+a,y+b,z+c]
    
    return noid == oid

def draw_model(c, oids, draw_box=False, draw_floor_grid=False):

    X,Y,Z = oids.shape

    if draw_floor_grid:
        for x in range(X):
            for y in range(Y):        
                draw_cube(c, oids.shape, x, y, 0, flat=True)
    
    if draw_box:
        draw_world_box(c, oids.shape, back=True)
    
    v = visibility_matrix(oids)
    
    for x in range(X)[::-1]:
        for y in range(Y)[::-1]:
            for z in range(Z):
                
                if not v[x][y][z]:
                    continue

                oid = oids[x][y][z]
                if oid == 0:
                    continue
                
                nx  = is_neighbour(oids,x,y,z, 1, 0, 0)
                nx_ = is_neighbour(oids,x,y,z,-1, 0, 0)
                ny  = is_neighbour(oids,x,y,z, 0, 1, 0)
                ny_ = is_neighbour(oids,x,y,z, 0,-1, 0)
                nz  = is_neighbour(oids,x,y,z, 0, 0, 1)
                nz_ = is_neighbour(oids,x,y,z, 0, 0,-1)

                nxy_  = oids[x+1][y-1][z] if (x+1) < X  and (y-1) >= 0 else False

                nxz   = oids[x+1][y][z+1] if (x+1) < X  and (z+1) < Z  else False
                nx_z_ = oids[x-1][y][z-1] if (x-1) >= 0 and (z-1) >= 0 else False

                nyz   = oids[x][y+1][z+1] if (y+1) < Y  and (z+1) < Z  else False
                ny_z_ = oids[x][y-1][z-1] if (y-1) >= 0 and (z-1) >= 0 else False
                
                draw_cube(c,oids.shape,x,y,z,nx,nx_,ny,ny_,nz,nz_,nxy_,nxz,nx_z_,nyz,ny_z_)

    if draw_box:
        draw_world_box(c, oids.shape, front=True)

def draw_png(m, filename, draw_floor_grid=False, draw_box=False):

    X_MAX, Y_MAX, Z_MAX = m.shape

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                 (X_MAX+Y_MAX)*DW2 + MARGIN*2,
                                 (X_MAX+Y_MAX)*DH2 + Z_MAX*DH + MARGIN*2)
    c = cairo.Context(surface)
    
    cm = cairo.Matrix(yy=-1, y0=surface.get_height())
    c.transform(cm)
    
    c.translate(MARGIN, MARGIN)
    
    c.set_antialias(cairo.ANTIALIAS_NONE)
    
    #background
    c.set_source_rgb(1,1,1)
    c.paint()
    
    #pen
    c.set_source_rgb(0,0,0)
    c.set_line_width(1)

    draw_model(c, m, draw_box=draw_box, draw_floor_grid=draw_floor_grid)

    surface.write_to_png(filename)

def fill(m, x, y, z, v=1):

    x1,x2 = x
    y1,y2 = y
    z1,z2 = z

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                m[x][y][z] = v
