"""
This module converts 3D (x, y, z) numpy arrays of data tiles (x, y) of data
in png files. These can then be read as WebGL textures.

The z dimension is deconstructed and the component x, y data is tiled as follows:
Columns, then rows, then channel (increasing through R, G, B, A). Note that
the RGBA values are unrelated to colors or alpha, they are merely data
channels.

"""

from __future__ import division
import png

def tile_array(a, maxx=256, maxy=256, maxz=4):
    """
    Flattens an x,y,z 3D array into an array of x,y tiles
    
    Tiling order is column, followed by row, followed by channel
    
    Args:
        * a (numpy array): a 3d numpy array of data
        * max<xyz> (int): the limits of the image size in pixels.
            NB that maxz is either 1 (Grayscale), 3 (RGB) or 4 (RGBA)
        
    This could be made more efficient using stride tricks
    
    """
    
    pngarray = np.zeros([maxx, maxy, maxz])
    datax, datay, dataz = a.shape
    itiles = int(maxx/datax)
    jtiles = int(maxy/datay)
    zslice = 0
    
    for z in range(maxz):
        for jtile in range(jtiles):
            for itile in range(itiles):
                _xmin = itile*datax
                _xmax = (itile+1)*datax
                _ymin = jtile*datay
                _ymax = (jtile+1)*datay
                
                pngarray[_xmin:_xmax, _ymin:_ymax, z] = a[:, :, zslice]
                if z+1 == maxz and jtile+1 == jtiles and itile+1 == itiles:
                    if zslice+1 < dataz:
                        print "Output array satuated"
                    return pngarray
                elif zslice < dataz:
                    pngarray[_xmin:_xmax, _ymin:_ymax, z] = a[:, :, zslice]
                    zslice += 1


def write_png(array, savep, height=256, width=256):
    """
    Writes a tiled array to a png image

    args:
        * array: x, y, rgba array
        * savep: output file
        * height/width: the height/width of the image.
            Must be a square number for use with WebGL
            textures. Need not be equal to each other.

    """
    
    if (height**0.5)%1 != 0.0 or (width**0.5)%1 != 0.0:
        raise ValueError("Dimensions must be square numbers i.e. sqrt(n) must be an integer")
    
    png_writer = png.Writer(height=height, width=width, alpha='RGBA')
    with open(savep, 'wb') as f:
        flat_array = array.reshape(-1, width*4) #assuming RGBA i.e. 4 channels
        png_writer.write(f, flat_array)
    

def array_to_png(data, filename, height=256, width=256):
    """ Converts a x,y,z 3D array to a tiled png image """
    tiled_array = tile_array(data, maxx=height, maxy=width, maxz=4)
    write_png(tiled_array, filename, height, width)


if __name__ == '__main__':
    print "Making example tiled png ./example.png"
    data = np.empty([128, 128, 16])
    for k in range(16):
        data[:,:,k] = k * 10

    array_to_png(data, "example.png")