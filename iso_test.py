#!/usr/bin/env python3
# Nicolas Seriot
# 2021-10-02
# A 2D, Cairo-based isometric renderer in Python 3
# https://github.com/nst/IsoRenderer

from iso import fill, draw_model, draw_png

import cairo
import numpy as np

def m1():
    
    X_MAX, Y_MAX, Z_MAX = 12, 8, 6
    
    m = np.full((X_MAX, Y_MAX, Z_MAX), 0) # object ids

    m[0]      [0]      [0]       = 1
    m[X_MAX-1][0]      [0]       = 1
    m[X_MAX-1][Y_MAX-1][0]       = 1
    m[X_MAX-1][Y_MAX-1][Z_MAX-1] = 1
    m[X_MAX-1][0]      [Z_MAX-1] = 1
    m[0]      [Y_MAX-1][0]       = 1
    m[0]      [Y_MAX-1][Z_MAX-1] = 1
    m[0]      [0]      [Z_MAX-1] = 1
    
    return m

def m2():

    X, Y, Z = 5,5,5
    
    m = np.full((X, Y, Z), 0)

    fill(m, (0,2), (0,3), (0,2), v=1)
    fill(m, (2,4), (2,4), (2,3), v=2)

    m[3][3][4] = 3
    m[2][3][3] = 3
    m[2][3][3] = 3
    m[1][3][3] = 3
    m[1][2][3] = 3
    m[0][2][3] = 3
    m[0][2][2] = 3
    m[0][2][1] = 3
    m[0][1][1] = 3
    m[0][0][1] = 3
    m[1][0][1] = 3
    m[1][0][2] = 3
    m[2][0][2] = 3
    m[3][0][2] = 3
    m[4][0][2] = 3
    m[4][1][2] = 3
    m[4][2][2] = 3

    return m

def m3():

    X, Y, Z = 13, 13, 13
    
    m = np.full((X, Y, Z), 0) # object ids

    fill(m, (4,8), (4,8), (4,8))

    fill(m, (0,X-1), (6,6),   (6,6))
    fill(m, (6,6),   (0,Y-1), (6,6))
    fill(m, (6,6),   (6,6),   (0,Z-1))

    return m

def m4():

    X,Y,Z = 7,7,7
    
    m = np.full((X, Y, Z), 1) # object ids

    fill(m, (1,X-2), (0,Y-1), (1,Z-2), v=0)
    fill(m, (1,X-2), (1,Y-2), (0,Z-1), v=0)
    fill(m, (0,X-1), (1,Y-2), (1,Z-2), v=0)

    fill(m, (2,4), (2,4), (Z-2,Z-1), v=1)
    fill(m, (0,1), (2,4), (2,4), v=1)
    fill(m, (2,4), (0,1), (2,4), v=1)
    
    m[0][3][3] = 0
    m[3][0][3] = 0
    m[3][3][Z-1] = 0

    return m

def m5():
    
    X, Y, Z = 7, 7, 7
    
    m = np.full((X, Y, Z), 0) # object ids

    fill(m, (X-1,X-1), (0,  Y-1), (0,Z-1))
    fill(m, (0,  X-1), (0,  Y-1), (0,0))
    fill(m, (0,  X-1), (Y-1,Y-1), (0,Z-1))
    fill(m, (0,  X-1), (0,  Y-1), (0,0))
    
    fill(m, (X-2,X-2), (1,  Y-2), (1,Z-2))
    fill(m, (1,  X-2), (Y-2,Y-2), (1,Z-2))
    fill(m, (1,  X-2), (1,  Y-2), (1,1))

    fill(m, (X-3,X-3), (2,  Y-3), (2,Z-3))
    fill(m, (2,  X-3), (Y-3,Y-3), (2,Z-3))
    fill(m, (2,  X-3), (2,  Y-3), (2,2))
    
    m[3][3][3] = 1
    
    return m

def m6():

    X,Y,Z = 7,7,7
    
    m = np.full((X,Y,Z), 0)

    for x in range(0, X):
        for y in range(0, Y):
            for z in range(0, Z):
                m[x][y][z] = 0 if (x+y+z) % 2 == 0 else 1

    return m

def m7():

    X,Y,Z = 7,7,7
    
    m = np.full((X,Y,Z), 1)
    
    fill(m, (1,2), (1,2), (5,6), v=0)
    fill(m, (4,5), (1,2), (5,6), v=0)
    fill(m, (1,2), (4,5), (5,6), v=0)
    fill(m, (4,5), (4,5), (5,6), v=0)

    fill(m, (0,2), (1,2), (1,2), v=0)
    fill(m, (0,2), (1,2), (4,5), v=0)
    fill(m, (0,2), (4,5), (1,2), v=0)
    fill(m, (0,2), (4,5), (4,5), v=0)
    
    fill(m, (1,2), (0,2), (1,2), v=0)
    fill(m, (1,2), (0,2), (4,5), v=0)
    fill(m, (4,5), (0,2), (1,2), v=0)
    fill(m, (4,5), (0,2), (4,5), v=0)

    return m

def m8():

    X,Y,Z = 7,7,7
    
    m = np.full((X,Y,Z), 0)
    
    fill(m, (0,2), (0,0), (0,0), v=1)
    fill(m, (0,0), (0,2), (0,0), v=1)
    fill(m, (0,0), (0,0), (0,2), v=1)
    
    fill(m, (4,6), (0,0), (0,0), v=1)
    fill(m, (6,6), (0,2), (0,0), v=1)
    fill(m, (6,6), (0,0), (0,2), v=1)
    
    fill(m, (0,0), (4,6), (0,0), v=1)
    fill(m, (0,2), (6,6), (0,0), v=1)
    fill(m, (0,0), (6,6), (0,2), v=1)
    
    fill(m, (4,6), (0,0), (6,6), v=1)
    fill(m, (6,6), (0,2), (6,6), v=1)
    fill(m, (6,6), (0,0), (4,6), v=1)
    
    fill(m, (0,0), (4,6), (6,6), v=1)
    fill(m, (0,2), (6,6), (6,6), v=1)
    fill(m, (0,0), (6,6), (4,6), v=1)

    fill(m, (4,6), (6,6), (6,6), v=1)
    fill(m, (6,6), (4,6), (6,6), v=1)
    fill(m, (6,6), (6,6), (4,6), v=1)

    fill(m, (3,3), (1,5), (3,3), v=1)
    fill(m, (1,5), (3,3), (3,3), v=1)
    fill(m, (3,3), (3,3), (1,5), v=1)

    return m

def files_are_equal(file1, file2):

    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        contents1 = f1.read()
        contents2 = f2.read()
    return contents1 == contents2    

def draw_all():

    #X_MAX, Y_MAX, Z_MAX = m.shape

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1050, 580)
    c = cairo.Context(surface)
    
    cm = cairo.Matrix(yy=-1, y0=surface.get_height())
    c.transform(cm)

    c.set_antialias(cairo.ANTIALIAS_NONE)

    #background
    c.set_source_rgb(1,1,1)
    c.paint()
    
    #pen
    c.set_source_rgb(0,0,0)
    c.set_line_width(1)

    c.save()
    c.translate(50, 300)
    draw_model(c, m1(), draw_box=True, draw_floor_grid=True)
    c.restore()

    c.save()
    c.translate(360, 340)
    draw_model(c, m2())
    c.restore()

    c.save()
    c.translate(460, 240)
    draw_model(c, m3())
    c.restore()

    c.save()
    c.translate(800, 320)
    draw_model(c, m4())
    c.restore()

    c.save()
    c.translate(50, 50)
    draw_model(c, m5())
    c.restore()

    c.save()
    c.translate(300, 50)
    draw_model(c, m6())
    c.restore()

    c.save()
    c.translate(550, 50)
    draw_model(c, m7())
    c.restore()

    c.save()
    c.translate(800, 50)
    draw_model(c, m8())
    c.restore()
    
    surface.write_to_png("iso.png")

def main():

    draw_all()

    draw_png(m1(), "test_1.png", draw_floor_grid=True, draw_box=True)
    draw_png(m2(), "test_2.png", draw_floor_grid=False, draw_box=False)
    draw_png(m3(), "test_3.png", draw_floor_grid=False, draw_box=False)
    draw_png(m4(), "test_4.png", draw_floor_grid=False, draw_box=False)
    draw_png(m5(), "test_5.png", draw_floor_grid=False, draw_box=False)
    draw_png(m6(), "test_6.png", draw_floor_grid=False, draw_box=False)
    draw_png(m7(), "test_7.png", draw_floor_grid=False, draw_box=False)
    draw_png(m8(), "test_8.png", draw_floor_grid=False, draw_box=False)
    
    assert(files_are_equal("test_1.png", "test_1_ref.png"))
    assert(files_are_equal("test_2.png", "test_2_ref.png"))
    assert(files_are_equal("test_3.png", "test_3_ref.png"))
    assert(files_are_equal("test_4.png", "test_4_ref.png"))
    assert(files_are_equal("test_5.png", "test_5_ref.png"))
    assert(files_are_equal("test_6.png", "test_6_ref.png"))
    assert(files_are_equal("test_7.png", "test_7_ref.png"))
    assert(files_are_equal("test_8.png", "test_8_ref.png"))

if __name__ == "__main__":
    
    main()

