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
q = 3
p = 4
s = 5
#print(boxfilter(q)) 
#print(boxfilter(s))
#print(boxfilter(p)) 
 


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
print(gauss1d(a))
print(gauss1d(b))
print(gauss1d(c))
print(gauss1d(d))


def gauss2d(sigma):
  ar = gauss1d(sigma)
  #print(ar)
  ar = ar[np.newaxis]
  #print(ar)
  art = np.transpose(ar)
  #print(art)
  return signal.convolve2d(ar, art)
print(gauss1d(b))
print(gauss1d(c))

# print(gauss2d(a))
# q = np.array([[1], [2],[3]])
#a1 = np.array([1,2,3])
#a1 = a1[np.newaxis]
#print(a1)
# print(a1)
# print(np.transpose(a1))

def gaussconvolve2d(array,sigma):
  filter = gauss2d(sigma)
  #print(filter)
  return signal.convolve2d(array, filter,'same')
#print(gaussconvolve2d(a1, 1))

im = Image.open('dog.png')
im = im.convert('L')
im_array = np.asarray(im)
#print(im_array)
im2_array = gaussconvolve2d(im_array, 3)
#print(im2_array)
im2 = Image.fromarray(im2_array.astype('uint8'))
# only integer will be saved
im2.save('dog_blur.png','PNG', optimize = True)






        