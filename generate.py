import shutil
import os
import struct
import json
import PIL
import urllib2

targetDir = "output"

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
    
    from PIL import Image
    im = Image.open(imageFile)
    imgHeight = im.size[1] # returns (width, height) tuple
    
    htmlContent = '<!DOCTYPE html><html lang="en">\n<head>\n<meta charset="utf-8"><title>Mockup '+str(i)+'</title>\n</head>\n<body style="background:url(i/'+img+') top center no-repeat; padding: 0; margin: 0;">\n<div style="height:'+str(imgHeight)+'px;">\n<img src="i/'+img+'" width="1" /></div>\n</body>\n</html>\n'
    
    fName = targetDir+"/mockup"+str(i).zfill(2)+".html"
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
    fName = "mockup"+str(i).zfill(2)+".html"
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
