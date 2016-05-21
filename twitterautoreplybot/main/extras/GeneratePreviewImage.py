from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

from wand.image import Image
import os

class GeneratePreviewImage:

    def __init__(self):
        self.background = Image(filename = settings.BASE_DIR + '/background.jpg')
        self.logo = Image(filename = settings.BASE_DIR + '/logo.png')
        self.montageWidth = 600
        self.montageHeight = 315
        
        
    def generatePreviewImage(self, image1Url, image2Url):
        image1 = Image(filename = image1Url)
        self.resizeImage(image1, self.montageWidth / 2, self.montageHeight)
        
        image2 = Image(filename = image2Url)
        self.resizeImage(image2, self.montageWidth / 2, self.montageHeight)
        
        self.background.composite(image1, int(self.montageWidth / 4. - image1.width / 2.), int(self.montageHeight / 2. - image1.height / 2.))
        self.background.composite(image2, int(self.montageWidth / 4. - image2.width / 2.) + self.montageWidth / 2, int(self.montageHeight / 2. - image2.height / 2.))
        
        self.background.composite(self.logo, 0, 0)
        
        self.background.save(filename = settings.BASE_DIR + '/preview.jpg')
    
    def resizeImage(self, image, desiredWidth, desiredHeight):
        originWidth = image.width
        originHeight = image.height
        originRatio = originWidth / float(originHeight)
        
        finalWidth = desiredWidth
            
        finalHeight = finalWidth / originRatio
        if (finalHeight > desiredHeight):
            finalHeight = desiredHeight
            finalWidth = finalHeight * originRatio    
	
        image.resize(int(finalWidth), int(finalHeight))