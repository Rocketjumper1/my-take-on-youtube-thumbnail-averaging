import numpy as np
from PIL import Image


class img_averager:
    @staticmethod
    def averager_mean(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.mean(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Mean averaging"
    @staticmethod
    def averager_median(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.median(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Median averaging"
    @staticmethod
    def averager_min(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.min(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Min averaging"
    @staticmethod
    def averager_max(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.max(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Max_averaging"
    @staticmethod
    def averager_std(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.std(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Standard Deviation averaging"
    @staticmethod
    def averager_var(images, size= (0, 0)):
        array_imgs = []
        for i in images:
            array_imgs.append(np.array(i.convert("RGB").resize(size), dtype= np.float32))
        np_img_averaged = np.var(array_imgs, axis=0)
        return Image.fromarray(np.uint8(np_img_averaged)), "Var averaging"
   