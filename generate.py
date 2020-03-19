import shutil
import re
import os
import struct
import json
import PIL
from PIL import Image
from urllib.parse import quote_plus
from itertools import cycle

targetDir = "output"

def page_name(imgName):
  pageName = os.path.splitext(imgName)[0]
  pageName = re.sub(r'\s',r'_', pageName)
  pageName = re.sub(r'[\W]+', '', pageName)
  pageName = re.sub(r'__',r'_', pageName)
  pageName = pageName.lower()
  return pageName

def main():
  # remove old files
  if (os.path.isdir(targetDir)):
    shutil.rmtree(targetDir)
    print("Target folder deleted.")
  
  # create target folder
  os.mkdir(targetDir)
  print("New target folder created.")
  
  # copy images
  shutil.copytree("images", targetDir+"/i")
  shutil.copyfile("style.css", targetDir+"/style.css")
  os.mkdir(targetDir+"/i/t")
  print("Copied images and CSS.")
  
  # read image directory and filter out non-images
  fileList = sorted(os.listdir("images"))
  imgList = []
  allowedExtensions = (".jpg", ".png", ".gif", ".bmp", ".jpeg")
  for file in fileList:
    extension = os.path.splitext(file)[1].lower() 
    if extension in allowedExtensions:
      imgList.append(file)
  #print(imgList)
      
  # generate mockup htmls
  # get next element: http://stackoverflow.com/a/2167962/1221212
  running = True
  imgCycle = cycle(imgList)
  nextImg = next(imgCycle)
  prevImage = imgList[-1]
  pageNamePrev = page_name(nextImg)
 
  while running:
    img, nextImg = nextImg, next(imgCycle)
    if imgList.index(nextImg) == 0:
      running = False
  
    imageFile = "images/"+img
    pageName = page_name(img)
    pageNameNext = page_name(nextImg)
    
    extension = os.path.splitext(img)[1].lower() 
    im = Image.open(imageFile)
    imgHeight = im.size[1] # returns (width, height) tuple
    
    imgURI = "i/"+quote_plus(img);
    htmlContent = ''
    htmlContent += '<!DOCTYPE html><html lang="en">\n'
    htmlContent += '<head>\n'
    htmlContent += '<meta charset="utf-8"><title>'+str(imgList.index(img)+1)+' - '+pageName+'</title>\n'
    htmlContent += '<link rel="stylesheet" href="style.css">\n'
    htmlContent += '</head>\n'
    htmlContent += '<body style="background:url('+imgURI+') top center no-repeat; padding: 0; margin: 0;">\n'
    htmlContent += '<div style="height:'+str(imgHeight)+'px;">\n'
    htmlContent += '<img src="'+imgURI+'" width="1" />\n'
    htmlContent += '</div>\n'
    htmlContent += '<nav><ul>\n'
    htmlContent += '<li><a href="index.html">Home</a></li>\n'
    htmlContent += '<li><a href="'+pageNameNext+'.html">Next</a></li>\n'
    htmlContent += '<li><a href="'+pageNamePrev+'.html">Previous</a></li>\n'
    htmlContent += '</ul></nav>\n'
    htmlContent += '</body>\n'
    htmlContent += '</html>\n'
    
    pageNamePrev = pageName
    
    fName = targetDir+"/"+pageName+".html"
    f = open(fName, 'w')
    f.write(htmlContent)
    f.close
    print("Generated "+fName)
  
  # generate thumbnails http://stackoverflow.com/a/273962/1221212
  thumbSize = 128, 128
  for img in imgList:
    imageFile = "images/"+img
    thumbFile = "output/i/t/"+ os.path.splitext(img)[0]
    try:
      im = Image.open(imageFile)
      im.thumbnail(thumbSize, Image.ANTIALIAS)
    except IOError:
      print("cannot create thumbnail for '%s'" % infile)
  
  # generate index
  with open('config.json') as data_file:    
    conf = json.load(data_file)
  
  htmlContent = ''
  htmlContent += '<!DOCTYPE html>\n<html lang="en">\n'
  htmlContent += '<head>\n'
  htmlContent += '<meta charset="utf-8">\n'
  htmlContent += '<title>'+conf["title"]+'</title>\n'
  htmlContent += '<link rel="stylesheet" href="style.css">\n'
  htmlContent += '</head>\n'
  htmlContent += '<body>\n'
  htmlContent += '<div id="container">\n<div class="content">\n'
  htmlContent += '<h1>'+conf["headline"]+'</h1>\n<ol>\n'
  for img in imgList:
    htmlContent += '<li><a href="'+page_name(img)+'.html">'+img+'</a></li>\n'
  htmlContent += '</ol>\n'
  htmlContent += '</div>\n'
  htmlContent += '</div>\n'
  htmlContent += '</body>\n'
  htmlContent += '</html>'
  
  fName = targetDir+"/index.html"
  print(fName)
  f = open(fName, 'w')
  f.write(htmlContent)
  f.close
  print("Generated index.html")

if __name__ == "__main__":
    main()
