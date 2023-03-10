#import package
from __future__ import division
from PIL import Image
import numpy as np
import math
from scipy import signal



# def boxfilter(num):
# mod = num%2
#  if mod > 0
#  array = np.full((num, num), 1//num)
#  return array;
#  else:
#   raise Exception('Dimension must be odd')

def boxfilter(num):
  mod = num%2
  assert mod != 0, "Dimension must be odd."
  array = np.full((num, num), 1/num)
  return array
# a = 7
# b = 6
# print(boxfilter(a))         	
# boxfilter(b)


def getlength(sigma):
  arlength = np.ceil(sigma*6/2.)*2 + 1
  return arlength


def createarray(num):
  return np.arange((1-num)/2, (num-1)/2+1)
#print(createarray(b))

def gauss1d(sigma):
  ar1d = createarray(getlength(sigma))
  #print(ar1d)
  ar1d = ar1d * ar1d
  # ar1d = np.multipy(ar1d,ar1d)
  #print(ar1d)
  needM = -1/(2*(sigma * sigma))
  #print(needM)
  fnary = needM ** ar1d
  #print(fnary)
  fnary = np.exp(fnary)
  #print(fnary)
  fnary = roundarr(fnary)
  #print(fnary)
  return fnary

def roundarr(array):
  suma = np.sum(array)
  return array/suma
a = 0.3
b = 0.5
c = 1
d = 2
# print(gauss1d(a))
# print(gauss1d(b))
# print(gauss1d(c))
# print(gauss1d(d))


def gauss2d(sigma):
  ar = gauss1d(sigma)
  #print(ar)
  ar = ar[np.newaxis]
  #print(ar)
  art = np.transpose(ar)
  #print(art)
  return signal.convolve2d(ar, art)
# print(gauss1d(b))
# print(gauss1d(c))

# print(gauss2d(a))
# q = np.array([[1], [2],[3]])
a1 = np.array([1,2,3])
a1 = a1[np.newaxis]
#print(a1)
# print(a1)
# print(np.transpose(a1))

def gaussconvolve2d(array,sigma):
  filter = gauss2d(sigma)
  #print(filter)
  return signal.convolve2d(array, filter,'same')
#print(gaussconvolve2d(a1, 1))
im = Image.open('dog.png')
im = np.asfarray(im)
listr = im[:,:,0]
listg = im[:,:,1]
listb = im[:,:,2]
im[:,:,0] = gaussconvolve2d(listr, 3)
im[:,:,1] = gaussconvolve2d(listg, 3)
im[:,:,2] = gaussconvolve2d(listb, 3)
im2 = Image.fromarray(im.astype('uint8'))
im2.save('dog_1.png','PNG', optimize = True)

im_c = Image.open('cat.png')
im_c = np.asfarray(im_c)
listr_c = im_c[:,:,0]
listg_c = im_c[:,:,1]
listb_c = im_c[:,:,2]
im_c[:,:,0] = im_c[:,:,0] - gaussconvolve2d(listr_c, 3)+128
im_c[:,:,1] = im_c[:,:,1] - gaussconvolve2d(listg_c, 3)+128
im_c[:,:,2] = im_c[:,:,2] - gaussconvolve2d(listb_c, 3)+128
imc2 = Image.fromarray(im_c.astype('uint8'))
imc2.save('cat_2.png','PNG', optimize = True)


im_c[:,:,0] = im_c[:,:,0] - 128 + im[:,:,0]
im_c[:,:,1] = im_c[:,:,1] - 128 + im[:,:,1]
im_c[:,:,2] = im_c[:,:,2] - 128 + im[:,:,2]
lowerbound, upperbound = 0, 255
np.clip(im_c[:,:,0], lowerbound, upperbound, out = im_c[:,:, 0])
np.clip(im_c[:,:,1], lowerbound, upperbound, out = im_c[:,:, 1])
np.clip(im_c[:,:,2], lowerbound, upperbound, out = im_c[:,:, 2])
im_c_add = Image.fromarray(im_c.astype('uint8'))
im_c_add.save('cat_3.png','PNG', optimize = True)












        