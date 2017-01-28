import os, sys
from osgeo import gdal


src_path = sys.argv[1]
write_dir = sys.argv[2]

def split_img(img_path, target_path):
  dset = gdal.Open(img_path)
  write_path = target_path + img_path.split("/")[-1].split(".")[0] + "/"
  if not os.path.exists(write_path):
    os.makedirs(write_path)  
  width = dset.RasterXSize
  height = dset.RasterYSize

  print width, 'x', height

  tilesize = 400

  for i in range(0, width, tilesize):
      for j in range(0, height, tilesize):
          w = min(i+tilesize, width) - i
          h = min(j+tilesize, height) - j
          gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " \
              +str(h)+" " + img_path + " " + write_path + "_"+str(i)+"_"+str(j)+".tif"
          os.system(gdaltranString)

image_types = (".jpg", ".png", ".JPG", ".PNG", ".JPEG", ".tif", ".tiff", ".TIFF", '.TIF')
 
image_paths = []  
for root, dirs, files in os.walk(src_path):
    image_paths.extend([os.path.join(root, f) for f in files if f.endswith(image_types)])
    
print 'number of images is', len(image_paths)

for image_path in image_paths:
  try:
    split_img(image_path, write_dir)
  except:
    print image_path, "failed"
