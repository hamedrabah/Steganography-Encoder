"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called whenever you 
press a button. Some of these are provided for you and others you are expected to write
on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:    October 20, 2017 (Python 3 Version)
"""
import a6history
import a6image


class Editor(a6history.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the methods
    and attributes of that class.  We do that (1) to put all of the image processing
    methods in one easy-to-read place and (2) because we might want to change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods, (2)
    non-implemented non-hidden methods and (3) hidden methods.  The non-hidden methods
    each correspond to a button press in the main application.  The hidden methods are
    all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been changed 
        and which have not.  To simplify the process, we copy the current image and use
        that as a reference.  So we change the current image with setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(original.getHeight()-col-1,row))
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,original.getWidth()-row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for h in range(current.getHeight()//2):
            for col in range(current.getWidth()):
                k = current.getHeight()-1-h
                current.swapPixels(h,col,k,col)
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all color 
        from the image by setting the three color components of each pixel to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green to
        
        0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        assert isinstance(sepia, bool)
        
        current = self.getCurrent()
        if sepia  == False:
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                red = (rgb[0]*0.3)
                green =(rgb[1]*0.6)
                blue  =(rgb[2]*0.1)
                brightness=int(red+green+blue)
                rgb = (brightness,brightness,brightness) # New pixel value
                current.setFlatPixel(pos,rgb)
        #sepia
        else:
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                red = (rgb[0]*0.3)
                green =(rgb[1]*0.6)
                blue  =(rgb[2]*0.1)
                brightness=int(red+green+blue)
                rgb = (brightness,int(brightness*0.6),int(brightness*0.4)) # New pixel value
                current.setFlatPixel(pos,rgb)
        
    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8) // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        pixel=(255,0,0)
        current = self.getCurrent()
        w=current.getWidth()
        h=current.getHeight()
        self._drawHBar(0,pixel)
        self._drawHBar(h-3,pixel)
        n=(w-8)//50
        dist=(w-4)/(n+2)
        for x in range(n+3):
            self._drawVBar(int(x*dist),pixel)     
                
            
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone helps
        give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
  
        current = self.getCurrent()
        w=current.getWidth()
        h=current.getHeight()
        midx=w/2
        midy=h/2
        hfd=(0.5)*(((w**2)+(h**2))**(0.5))
        hfd2=hfd**2
        
        for x in range(h):
            for k in range(w):
                dist2=(k-midx)**2 + (x-midy)**2
                formula=1-(dist2/hfd2)
                rgb=current.getPixel(x,k)
                red = int(rgb[0]*formula)
                green =int(rgb[1]*formula)
                blue  =int(rgb[2]*formula)
                pixel = (red,green,blue) # New pixel value
                current.setPixel(x,k,pixel)

    
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row and
        column).  Average the colors of the step x step block to the right and down
        from this corner (if there are less than step rows or step columns, go to the
        edge of the image). Then assign that average to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        #asserts 
        assert isinstance(step, int)
        assert step >0

        current = self.getCurrent()
        
        w=current.getWidth()
        h=current.getHeight()
        for x in range(0,h,step):
            for y in range (0,w,step):
                self._avgRGB(current,x,y,step)
            


    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False otherwise.
        
        This method attemps to hide the given message text in the current image.  It uses
        the ASCII representation of the text's characters.  If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have enough
        pixels to store the text, this method returns False without storing the message.
        
        To indicate that there is a hidden message to be decoded, encode creates a marker
        
        A marker of a hidden message starts in the first pixel,
        it contains the following parts:
                2 special characters: }~
                a number < 1,000,000 indicating length of hidden message
                2 special characters: ~{
                
        Ex. If the hidden message is 876,557 characters long the marker is:
                }~876557~{
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        assert isinstance(text,str)
        if len(text) > 999999:
            return False
        string=str(len(text))
        character_length=len(string)
        characters_total=character_length+4+len(text)
        current=self.getCurrent()
        maximum=current.getLength()
        if characters_total > maximum:
            return False
        
        marker_start='}~'
        marker_end='~{'
        marker= marker_start+string+marker_end
        
        ASCII_code=self._text_to_ASCII(marker)+self._text_to_ASCII(text)
        
        self._ASCII_encode(ASCII_code)
        
        return True
    
    
    def _text_to_ASCII(self,text):
        """
        Returns: a list of ASCII values
                        
        This method takes text and returns a list with all the ASCII values representing
        the characters in the text. 
        
        Parameter text: the text to convert to ASCII
        Precondition: text is a string
        """
        assert isinstance(text, str)
        
        list=[]
        for x in text:
            list.append(ord(x))
            
        return list
        

    def _ASCII_encode(self,thelist):
        """
        Takes a list with ASCII values and uses the helper function _encode_pixel
        to hide each ASCII value in the current image starting at the first pixel
        
        Parameter thelist: a list with ASCII values
        Precondition: thelist is a list with valid ASCII codes.
        """
        assert self._is_ASCII(thelist)==True
        
        for x in range(len(thelist)):
            value=thelist[x]
            self._encode_pixel(x,value)
            
            
    def _is_ASCII(self,thelist):
        """
        Returns: True if every element of a list is a possible ASCII value.
        Otherwise it returns False.
        
        Takes a list of values and determines if each values is a possible
        ASCII value.
        
        Parameter thelist: a list of integers
        Precondition: thelist is a list
        """
        
        assert isinstance(thelist,list)
        
        for x in thelist:
            if not isinstance(x,int):
                return False
            if not (0<=x <=255):
                return False
            else:
                return True
            
        
    def decode(self):
        """
        Returns: The secret message stored in the current image. If no message
        is detected, it returns None
                        
        This method draws a ASCII code and converts each value to its character
        representation and returns a string of the resulting text.
        
        To detect if there is a hidden message, it transforms the image
        into a list of ASCII values uses the helper function
        _isMarker.
        """
        current=self.getCurrent()
        message_code=self._pixels_to_ASCII(current)
        if self._isMarker(message_code)==False:
            return None
        length_text=self._getLengthCode(message_code)
        charac_length=len(str(length_text))
        start=4+charac_length
        stop=start+length_text
        
        text_code=message_code[start:stop]
        
        
        return self._translate_ASCII(text_code)
    
    
    def _isMarker(self,thelist):
        """
        Returns: True if a given list contains possible ASCII values with
        a valid marker for a hidden message.
        
        A marker of a hidden message starts in the first pixel,
        it contains the following parts:
                2 special characters: }~
                a number < 1,000,000 indicating length of hidden message
                2 special characters: ~{
                
        Ex. If the hidden message is 876,557 characters long the marker is:
                }~876557~{
                
        This method uses helper function _is_ASCII to determine if the given
        list is a list with possible ASCII values. It also uses helper function
        _translate_ASCII to change the ASCII codes of the number part in the
        marker to the character representation, and finally it uses helper
        _Code_to_Int to determine if the given characters are a valid integer.
        
        Parameter thelist: A list with possible ASCII values 
        Precondition: thelist is a list
        """
        assert isinstance(thelist, list)
        if self._is_ASCII(thelist)== False:
            return False
        marker1=thelist[:2]
        if marker1!=[125,126]:
            return False
        rest=thelist[2:]
        pos=rest.index(126)+2
        if thelist[pos+1]!=123:
            return False
        between=thelist[2:pos]
        if len(between)>6:
            return False
        number=self._translate_ASCII(between)
        if self._Code_to_Int(number)==False:
            return False
        else:
            return True
        
    
    def _getLengthCode(self,thelist):
        """
        Returns: an integer
        
        Takes a list of ASCII values that start with a marker of hidden message
        returns an int representing the length of the text
        
        This method uses the helper function _Code_to_Int to obtain the integer. 
        
        Parameter thelist: the list
        Precondition: thelist is an list with valid ASCII values
        """
        assert isinstance(thelist, list)
        assert self._is_ASCII(thelist)==True
        rest=thelist[2:]
        pos=rest.index(126)
        thelist=rest[:pos]
        string=self._translate_ASCII(thelist)
        return self._Code_to_Int(string)
    
    
    def _Code_to_Int(self,string):
        """
        Returns: an integer of a string
        
        This method takes a string and returns an integer if the string is an integer,
        otherwise returns false
        
        Parameter string: the string
        Precondition: string is an string
        """
        assert isinstance(string, str)
        try:
            return int(string)
        except ValueError:
            return False        
        
        
    def _pixels_to_ASCII(self,image):
        """
        Takes image and returns list with hidden numbers in each pixel.
        
        This method uses helper fucntion _decode_pixel to obtain
        possible ASCII codes in each pixel.
        
        Parameter image: the image to obtain hidden values
        Precondition: image is an image object
        """
        assert isinstance(image,a6image.Image)
        
        length=image.getLength()
        list=[]
        for x in range(length):
            list.append(self._decode_pixel(x))
        
        return list
    
    def _translate_ASCII(self,code):
        """
        Takes list of ASCII values returns a string of text
        
        This method draws a ASCII code and converts each value to its character
        representationa and returns a string of the resulting text. 
        
        Parameter code: the ASCII values to convert to characters
        Precondition: code is a list that consists of ASCII values which are 3 digit ints
        """
        assert isinstance(code,list)
        assert self._is_ASCII(code)==True
        
        string=''
        for x in code:
            string=string+chr(x)
            
        return string
            
                
    
    # HELPER FUNCTIONS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the current
        image. This means that the bar includes the pixels row, row+1, and row+2.
        The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        assert isinstance(row, int)
        assert isinstance(pixel, tuple)
        
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)
            
    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given col.
        
        This method draws a vertical 4-pixel-wide bar at the given col of the current
        image. This means that the bar includes the pixels col, col+1, col+2, and col+3.
        The bar uses the color given by the pixel value.
        
        Parameter col: The start of the col to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+3 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        assert isinstance(col, int)
        assert isinstance(pixel, tuple)
        
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row, col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)
    
    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        assert isinstance(pos, int)
        
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def _encode_pixel(self, pos,ASCII):
        """
        Sets pixel at position pos to be a pixel that hides an ASCCI value.
        
        This function assumes that the ASCCI value is a 3-digit number
        that will be encoded in the last digit of each of the rgb values
        (e.g. red, green and blue).
        
        Note: RGB values cannot be greater than 255. Therefore if a value whose
        last digit makes the value be > 255 will be reduced by 10.
        Example:
                original RGB (199,254,247)
                ASCII: 165
                RGB with code: (191,246,245)
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        
        Parameter ASCII: an ASCII value
        Precondition: ASCII is an int with 0 <= ASCII <=255
        """
        assert isinstance(ASCII,int)
        assert isinstance(pos, int)
        assert 0<= ASCII
        assert ASCII <= 255
        
        a=ASCII//100
        b=(ASCII//10)%10
        c=ASCII%10
        current = self.getCurrent()
        rgb=current.getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        
        red=(red//10)*10+(a)
        if red>255:
            red=red-10
        
        green=(green//10)*10+(b)
        if green>255:
            green=green-10
        
        blue=(blue//10)*10+(c)
        if blue>255:
            blue=blue-10
        
        pixel=(red,green,blue)
        
        current.setFlatPixel(pos,pixel)

    def _avgRGB(self, current,x,y,step):
        """
        The average of each color in an list of pixels
        
        Averaging is exactly what it sounds like. You sum up all the red values
        and divide them by the number of pixels.
        You do the same for the green and blue values.
        
        Parameter current: the current image object
        Precondition: current is a valid image object

        Parameter x: the row position of the first pixel to be modified
        Precondition: x is an int
        
        Parameter y: the column position of the first pixel to be modified
        Precondition: y is an int
        
        Parameter step: the amount of pixels to the right and down to be modified
        Precondition: step is an int
        
        """
        assert isinstance(current,a6image.Image)
        assert isinstance(x,int)
        assert isinstance(y,int)
        assert isinstance(step,int)
        
        red = 0
        green = 0
        blue = 0
        w=current.getWidth()
        h=current.getHeight()
        countk=0
        for k in range(x,x+step):
            try:
                for j in range(y,y+step):
                    try:
                        pixel=current.getPixel(k,j)
                        red = red + pixel[0]
                        green = green + pixel[1]
                        blue = blue + pixel[2]
                        countk+=1
                    except AssertionError:
                        green=green
            except AssertionError:
                green=green
        
        print(red,green,blue,countk)
        avgRed=int(red/(countk))
        avgGreen=int(green/(countk))
        avgBlue=int(blue/(countk))
        pixel=(avgRed,avgGreen,avgBlue)
        
        for k in range(x,x+step):
            try:
                for j in range(y,y+step):
                    try:
                        if k==0 and j==0:
                            print(pixel)
                        current.setPixel(k,j,pixel)
                    except AssertionError:
                        None
            except AssertionError:
                None
                
        
        
        