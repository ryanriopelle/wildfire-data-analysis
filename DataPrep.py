import matplotlib.pyplot as plt
from osgeo import gdal
import os, sys

class PrepTools:
    
        
    def split_img(self,img_path, target_path,tilesize):
        dset = gdal.Open(img_path)
        write_path = target_path + "/"
        width = dset.RasterXSize
        height = dset.RasterYSize
        for i in range(0, width, tilesize[0]):
            for j in range(0, height, tilesize[1]):
                w = min(i+tilesize[0], width) - i
                h = min(j+tilesize[0], height) - j
                gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", "+str(h)+" " + img_path + " " + write_path + "_"+str(i)+"_"+str(j)+".tif"
                os.system(gdaltranString)
                
    def Clip(self,SE,FileName,OutFile):
        #Input:
            # SE - Spatial Extent - [x1, y1, x2, y2]
            # Filename - name of file you wish to clip
            # OutFile - name of file you want to create
        gdal_str="gdal_translate -projwin "+str.format('{0:.13f}', SE[0])+\
            " "+str.format('{0:.13f}', SE[1])+" "+str.format('{0:.13f}', SE[2])+\
            " "+str.format('{0:.13f}', SE[3])+" "+FileName+" "+OutFile
        os.system(gdal_str)
        
    def GrabCornerCoordinates(self,FileName):
        src = gdal.Open(FileName)
        ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
        lrx = ulx + (src.RasterXSize * xres)
        lry = uly + (src.RasterYSize * yres)
        return [ulx,uly,lrx,lry]
    
    def GrabPixelSize(self,FileName):
        dataset=gdal.Open(FileName)
        geotransform = dataset.GetGeoTransform()
        if not geotransform is None:
            return [geotransform[1],geotransform[5]]
        
    def IntersectBox(self,CC1,CC2):
        # Import:  Corner Coordinates in [Upper Left Long, Upper Left Lat, Lower Right Long, Lower Right Lat]
        # Note -- Assuming coordinates are in San Diego (aka - Long and + Lat)
    
        #Upper Left:
        ulx=max(CC1[0],CC2[0])
        uly=min(CC1[1],CC2[1])
    
        #Lower Right:
        lrx=min(CC1[2],CC2[2])
        lry=max(CC1[3],CC2[3])
    
        return [ulx,uly,lrx,lry]
        
    def Check_PlotExtentions(self,boxes,SE,plotname=None):
    	#Input:
        	#boxes -- dict of corner points (aka list of list), with [Upper Left Long, Upper Left Lat, Lower Right Long, Lower Right Lat]
    	i=0
    	color1=['-k','-b','-g']
    	plt.figure(figsize=(8,6))
    	for k in boxes.keys():
        	X=[boxes[k][0],boxes[k][2],boxes[k][2],boxes[k][0],boxes[k][0]]
        	Y=[boxes[k][1],boxes[k][1],boxes[k][3],boxes[k][3],boxes[k][1]]
        	plt.plot(X,Y,color1[i],label=k,linewidth=2.0)
        	i+=1
    
    	i=0
    	color2=['--y','--r','--c','--o','--g']
    	for k in SE:
        	X=[SE[k][0],SE[k][2],SE[k][2],SE[k][0],SE[k][0]]
        	Y=[SE[k][1],SE[k][1],SE[k][3],SE[k][3],SE[k][1]]
        	plt.plot(X,Y,color2[i],label=k,linewidth=4.0) 
        	i+=1
        
    	plt.legend()
    	if plotname != None:
    		plt.savefig(plotname+'.png')