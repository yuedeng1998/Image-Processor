#import package
from __future__ import division
from PIL import Image
import numpy as np
import math
from scipy import signal

import pdb

def boxfilter(num):
  mod = num%2
  assert mod != 0, "Dimension must be odd."
  #if the mod is 0,then num is even, go to the assert
  array = np.full((num, num), 1/num)
  #full the array with 1/num
  return array

def getlength(sigma):
  arlength = np.ceil(sigma*6/2.)*2 + 1
  return arlength
  # helpper fn to get the length of filter array
def createarray(num):
  return np.arange((1-num)/2, (num-1)/2+1)
  # helpper fn to create the array with[...-2,-1,0,1,2...] which is the distance from center
def roundarr(array):
  suma = np.sum(array)
  return array/suma
  #helpper fn to round the final filter sum up to 1

def gauss1d(sigma):
  ar1d = createarray(getlength(sigma))
  #an array with x, distance from center
  ar1d = ar1d * ar1d
  #x^2
  needM = -1/(2*(sigma * sigma))
  #get the parameter
  fnary = needM ** ar1d
  fnary = np.exp(fnary)
  fnary = roundarr(fnary)
  return fnary

def gauss2d(sigma):
  filterA1d = gauss1d(sigma)
  #get the 1d filter
  filterA2d = filterA1d[np.newaxis]
  #get the 2d filter by extension
  filterA2d_T = np.transpose(filterA2d)
  #get the transposed 2d filter
  return signal.convolve2d(filterA2d, filterA2d_T)

def gaussconvolve2d(array,sigma):
  filter = gauss2d(sigma)
  return signal.convolve2d(array, filter,'same')

im = Image.open('dog.png')
im = im.convert('L')
#convert the image to gray-scale
im_array = np.asarray(im)
#convert the image to an array
im2_array = gaussconvolve2d(im_array, 3)
#get the image after filter
im2 = Image.fromarray(im2_array.astype('uint8'))
# only integer will be saved, so cast to [0,255] and convert the arrary back to integer
im2.save('dog_part1.png','PNG', optimize = True)

def imblur(im, sigma):
 im = np.asfarray(im)
# convert the image to a 2d array with height and width based on (x,y) and each pixel
# maintain (r,g,b)
 listr = im[:,:,0]
 listg = im[:,:,1]
 listb = im[:,:,2]
# get 2d array for each r, g,b seperately
 im[:,:,0] = gaussconvolve2d(listr, sigma)
 im[:,:,1] = gaussconvolve2d(listg, sigma)
 im[:,:,2] = gaussconvolve2d(listb, sigma)
#apply filter to rgb seperetely
 im2 = Image.fromarray(im.astype('uint8'))
 return im2

im_d = Image.open('dog.png')
im2_d = imblur(im_d,3)
im2_d.save('dog_1.png','PNG', optimize = True)
im_c = Image.open('cat.png')
def imhigh_freq(im_c, sigma): 
 im_c = np.asfarray(im_c)
 listr_c = im_c[:,:,0]
 listg_c = im_c[:,:,1]
 listb_c = im_c[:,:,2]
 im_c[:,:,0] = im_c[:,:,0] - gaussconvolve2d(listr_c, sigma)+128
 im_c[:,:,1] = im_c[:,:,1] - gaussconvolve2d(listg_c, sigma)+128
 im_c[:,:,2] = im_c[:,:,2] - gaussconvolve2d(listb_c, sigma)+128
 #apply -filter and add 128 to get the high fre array and get rid og neg value
 imc2 = Image.fromarray(im_c.astype('uint8'))
 return imc2

im_c = Image.open('cat.png')
im2_c = imhigh_freq(im_c, 3)
im2_c.save('cat_2.png','PNG', optimize = True)

def imadd_hl(im_cc, im_dd, sigma):
 im_cc = imhigh_freq(im_cc, sigma)
 im_dd = imblur(im_dd, sigma)
 im_c = np.asfarray(im_cc)
 im_d = np.asfarray(im_dd)

 #pdb.set_trace()
 #get the higfre and blur image for two images and convert to arrays
 im_c[:,:,0] = im_c[:,:,0] - 128 + im_d[:,:,0]
 im_c[:,:,1] = im_c[:,:,1] - 128 + im_d[:,:,1]
 im_c[:,:,2] = im_c[:,:,2] - 128 + im_d[:,:,2]
 #add them up
 lowerbound, upperbound = 0, 255
 np.clip(im_c[:,:,0], lowerbound, upperbound, out = im_c[:,:, 0])
 np.clip(im_c[:,:,1], lowerbound, upperbound, out = im_c[:,:, 1])
 np.clip(im_c[:,:,2], lowerbound, upperbound, out = im_c[:,:, 2])
 #clamp the array to within [0,255]
 im_c_add = Image.fromarray(im_c.astype('uint8'))
 return im_c_add

im_cd_add = imadd_hl(im_c,im_d,3)
im_cd_add.save('dog_cat_add.png','PNG', optimize = True)

im_bike = Image.open('1a_bicycle.bmp')
im_moto = Image.open('1b_motorcycle.bmp')
im_bm_add = imadd_hl(im_bike,im_moto, 2)
im_bm_add.save('11_add.png', 'PNG', optimize = True)
im_bm_add = imadd_hl(im_bike,im_moto, 3)
im_bm_add.save('12_add.png', 'PNG', optimize = True)
im_bm_add = imadd_hl(im_bike,im_moto, 4)
im_bm_add.save('13_add.png', 'PNG', optimize = True)

im_eins = Image.open('2a_einstein.bmp')
im_mari = Image.open('2b_marilyn.bmp')
im_em_add = imadd_hl(im_eins,im_mari,2)
im_em_add.save('21_add.png','PNG', optimize = True)
im_em_add = imadd_hl(im_eins,im_mari,3)
im_em_add.save('22_add.png','PNG', optimize = True)
im_em_add = imadd_hl(im_eins,im_mari,4)
im_em_add.save('23_add.png','PNG', optimize = True)

im_fish = Image.open('3a_fish.bmp')
im_subm = Image.open('3b_submarine.bmp')
im_fs_add = imadd_hl(im_fish,im_subm,2)
im_fs_add.save('31_add.png','PNG', optimize = True)
im_fs_add = imadd_hl(im_fish,im_subm,3)
im_fs_add.save('32_add.png','PNG', optimize = True)
im_fs_add = imadd_hl(im_fish,im_subm,4)
im_fs_add.save('33_add.png','PNG', optimize = True)

im_bird = Image.open('4a_bird.bmp')
im_plane = Image.open('4b_plane.bmp')
im_bp_add = imadd_hl(im_bird,im_plane,4)
im_bp_add.save('41_add.png','PNG', optimize = True)
im_bp_add = imadd_hl(im_bird,im_plane,5)
im_bp_add.save('42_add.png','PNG', optimize = True)
im_bp_add = imadd_hl(im_bird,im_plane,6)
im_bp_add.save('43_add.png','PNG', optimize = True)



