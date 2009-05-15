try:
    import pygame2.test.pgunittest as unittest
except:
    import pgunittest as unittest
from pygame2.base import Surface

class TestSurface (Surface):
    def __init__ (self):
        Surface.__init__ (self)
        self._height = 10
        self._width = 20
        self._size = (20, 10)
        self._pixels = "pixels"
    
    def blit (self, **kwds):
        return "blit"
    def copy (self):
        return TestSurface ()

    height = property (lambda self: self._height)
    width = property (lambda self: self._width)
    size = property (lambda self: self._size)
    pixels = property (lambda self: self._pixels)

class PartialSurface (Surface):
    def __init__ (self):
        Surface.__init__ (self)
        self._size = 10, 10

    def copy (self):
        return PartialSurface ()
    
    size = property (lambda self: self._size)

class SurfaceTest (unittest.TestCase):

    def test_pygame2_base_Surface_blit(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.blit:

        # blit (**kwds) -> object
        # 
        # Performs a blit operation on the Surface.
        # 
        # The behaviour, arguments and return value depend on the concrete
        # Surface implementation.

        sf = TestSurface ()
        sf2 = PartialSurface ()
        self.assertEquals (sf.blit (), "blit")
        self.assertRaises (NotImplementedError, sf2.blit)

    def test_pygame2_base_Surface_copy(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.copy:

        # copy () -> Surface
        #
        # Creates a copy of this Surface.

        sf = TestSurface ()
        sf2 = sf.copy()
        self.assertEquals (sf.size, sf2.size)
        
        sf = PartialSurface ()
        sf2 = sf.copy ()
        self.assertEquals (sf.size, sf2.size)

    def test_pygame2_base_Surface_height(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.height:

        # Gets the height of the Surface.
        sf = TestSurface ()
        self.assertEquals (sf.height, 10)
        
        sf = PartialSurface ()
        self.assertRaises (NotImplementedError, getattr, sf, "height")

    def test_pygame2_base_Surface_pixels(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.pixels:

        # Gets a buffer with the pixels of the Surface.
        sf = TestSurface ()
        self.assertEquals (sf.pixels, 'pixels')
        sf = PartialSurface ()
        self.assertRaises (NotImplementedError, getattr, sf, "pixels")
        
        #self.assertEquals (sf.pixels, 10)

    def test_pygame2_base_Surface_size(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.size:

        # Gets the width and height of the Surface.
        sf = TestSurface ()
        self.assertEquals (sf.size, (20, 10))
        sf = PartialSurface ()
        self.assertEquals (sf.size, (10, 10))

    def test_pygame2_base_Surface_width(self):

        # __doc__ (as of 2009-03-28) for pygame2.base.Surface.width:

        # Gets the width of the Surface.
        sf = TestSurface ()
        self.assertEquals (sf.width, 20)
        sf = PartialSurface ()
        self.assertRaises (NotImplementedError, getattr, sf, "width")

if __name__ == "__main__":
    unittest.main ()
