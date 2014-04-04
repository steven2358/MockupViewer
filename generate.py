import shutil
import re
import os
import struct
import json
import PIL
import urllib2

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
    print "Target folder deleted."
  
  # create target folder
  os.mkdir(targetDir)  
  print "New target folder created."
  
  # copy images
  shutil.copytree("images", targetDir+"/i")
  shutil.copyfile("style.css", targetDir+"/style.css")
  print "Copied images and CSS."
  
  # read image directory
  imgList = os.listdir("images")
  #print imgList
      
  # generate mockup htmls
  i = 1;
  
  for img in imgList:
    imageFile = "images/"+img
    
    extension = os.path.splitext(img)[1].lower() 
    if extension in (".jpg", ".png"):
      
      from PIL import Image
      im = Image.open(imageFile)
      imgHeight = im.size[1] # returns (width, height) tuple
      
      imgURI = "i/"+urllib2.quote(img.encode("utf8"));
      htmlContent = '<!DOCTYPE html><html lang="en">\n<head>\n<meta charset="utf-8"><title>Mockup '+str(i)+'</title>\n</head>\n<body style="background:url('+imgURI+') top center no-repeat; padding: 0; margin: 0;">\n<div style="height:'+str(imgHeight)+'px;">\n<img src="'+imgURI+'" width="1" /></div>\n</body>\n</html>\n'
      
      fName = targetDir+"/"+page_name(img)+".html"
      f = open(fName, 'w')
      f.write(htmlContent)
      f.close    
      i += 1
      print "Generated "+fName  
  
  # generate index
  with open('config.json') as data_file:    
    conf = json.load(data_file)
  
  htmlContent = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>'+conf["title"]+'</title>\n<link rel="stylesheet" href="style.css">\n</head>\n<body>\n<div id="container">\n<div class="content">\n<h1>'+conf["headline"]+'</h1>\n<ul>\n'  
  i = 1
  for img in imgList:
    extension = os.path.splitext(img)[1].lower() 
    if extension in (".jpg", ".png"):
      fName = page_name(img)+".html"
      htmlContent += '<li><a href="'+fName+'">'+img+'</a></li>\n'
      i += 1
  htmlContent += '</ul>\n</div>\n</div>\n</body>\n</html>'
  fName = targetDir+"/index.html"
  print fName
  f = open(fName, 'w')
  f.write(htmlContent)
  f.close
  print "Generated index.html"

if __name__ == "__main__":
    main()
