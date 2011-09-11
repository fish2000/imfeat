try:
    import unittest2 as unittest
except ImportError:
    import unittest
import Image
import cv
import cv2
import imfeat
import numpy as np


def load_images(image_name):
    fn = 'test_images/%s' % image_name
    yield cv.LoadImage(fn)
    yield cv2.imread(fn)
    yield Image.open(fn)


class Test(unittest.TestCase):

    def test_name(self):
        type_channel_modes = [('opencv', 'bgr', 'uint8'), ('pil', 'rgb', 'uint8'), ('numpy', 'bgr', 'uint8'),
                              ('opencv', 'bgr', 'float32'), ('numpy', 'bgr', 'float32')]
        to_np8 = lambda x: imfeat.convert_image(x, {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'})
        to_np32 = lambda x: imfeat.convert_image(x, {'type': 'numpy', 'dtype': 'float32', 'mode': 'bgr'})
        for fn in ['lena.jpg', 'lena.pgm', 'lena.ppm']:
            for i in load_images(fn):
                image_np8 = to_np8(i)
                image_np32 = to_np32(i)
                np.testing.assert_equal(image_np8, np.array(image_np32 * 255, dtype=np.uint8))
                image_np8 = imfeat.convert_image(i, {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'})
                image_np32 = imfeat.convert_image(i, {'type': 'numpy', 'dtype': 'float32', 'mode': 'bgr'})
                for t, c, m in type_channel_modes:
                    cur_img = imfeat.convert_image(i, {'type': t, 'dtype': m, 'mode': c})
                    if t == 'opencv':
                        self.assertTrue(isinstance(cur_img, cv.iplimage))
                    elif t == 'pil':
                        self.assertTrue(Image.isImageType(cur_img))
                    else:
                        self.assertTrue(isinstance(cur_img, np.ndarray))
                    if m == 'uint8':
                        np.testing.assert_equal(image_np8, to_np8(cur_img))
                    else:
                        np.testing.assert_equal(image_np32, to_np32(cur_img))

    def test_resize(self):
        to_np8 = lambda x: imfeat.convert_image(x, {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'})
        n = 0
        for fn in ['lena.jpg', 'lena.pgm', 'lena.ppm']:
            for i in load_images(fn):
                for h, w in [(50, 50), (100, 50), (50, 100), (1000, 100), (100, 1000)]:
                    print((fn, type(i)))
                    out_arr = to_np8(imfeat.resize_image(i, h, w))
                    self.assertEqual(out_arr.shape, (h, w, 3))
                    #cv2.imwrite('resize-out-%.3d.jpg' % n, out_arr)
                    n += 1

    def test_tostring(self):
        n = 0
        for fn in ['lena.jpg', 'lena.pgm', 'lena.ppm']:
            for i in load_images(fn):
                for ext in ['jpeg', 'png']:
                    o = imfeat.image_tostring(i, ext)
                    #open('tostring-%.3d.%s' % (n, ext), 'w').write(o)
                    o = imfeat.image_tostring(imfeat.image_fromstring(imfeat.image_tostring(i, ext), {'type': 'pil', 'dtype': 'uint8', 'mode': 'rgb'}), ext)
                    #open('fromstring-%.3d.%s' % (n, ext), 'w').write(o)
                    n += 1


if __name__ == '__main__':
    unittest.main()
