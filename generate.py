import shutil
import os
import struct
import json

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
    
    # http://stackoverflow.com/a/7409814/1221212
    with open(imageFile, 'rb') as content_file:
      content = content_file.read()
    imgProps = get_image_info(content)
    imgHeight = imgProps[2]
    
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

# Get image size and info using pure python code
# http://markasread.net/post/17551554979/get-image-size-info-using-pure-python-code    
def get_image_info(data):
  """
  Return (content_type, width, height) for a given img file content
  no requirements
  """
  data = str(data)
  size = len(data)
  height = -1
  width = -1
  content_type = ''

  # handle GIFs
  if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
    # Check to see if content_type is correct
    content_type = 'image/gif'
    w, h = struct.unpack("<HH", data[6:10])
    width = int(w)
    height = int(h)

  # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
  # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
  # and finally the 4-byte width, height
  elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
      and (data[12:16] == 'IHDR')):
    content_type = 'image/png'
    w, h = struct.unpack(">LL", data[16:24])
    width = int(w)
    height = int(h)

  # Maybe this is for an older PNG version.
  elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
    # Check to see if we have the right content type
    content_type = 'image/png'
    w, h = struct.unpack(">LL", data[8:16])
    width = int(w)
    height = int(h)

  # handle JPEGs
  elif (size >= 2) and data.startswith('\377\330'):
    content_type = 'image/jpeg'
    jpeg = StringIO(data)
    jpeg.read(2)
    b = jpeg.read(1)
    try:
      while (b and ord(b) != 0xDA):
        while (ord(b) != 0xFF): b = jpeg.read
        while (ord(b) == 0xFF): b = jpeg.read(1)
        if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
          jpeg.read(3)
          h, w = struct.unpack(">HH", jpeg.read(4))
          break
        else:
          jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
        b = jpeg.read(1)
      width = int(w)
      height = int(h)
    except struct.error:
      pass
    except ValueError:
      pass

  return content_type, width, height

if __name__ == "__main__":
    main()
