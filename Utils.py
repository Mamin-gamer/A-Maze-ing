#This file is responsible for unilities
#functions that will be called throughout the program

import pygame
pygame.font.init()
import hashlib
import re

#Class to create Input box in pygame
class InputBox:
    COLOUR_ACTIVE = (20,40,140)
    COLOUR_INACTIVE = (100,100,100)
    INSIDE_COLOUR = (120, 120, 120)

    TEXT_COLOUR = ()
    FONT = pygame.font.Font(None, 32)
    FONTPWD = pygame.font.Font(None, 64)

    def __init__(self, x, y, width, height, text = '', padding = 5, validate = None, password = False):
        self.x = x
        self.y = y
        self.width = width
        self.width_copy = width #copy to compare width to
        self.height = height
        self.text = text
        self.colour = self.COLOUR_INACTIVE
        self.active = False
        self.changed = False
        self.validate = validate
        self.password = password
        self.display_text = ''
        self.padding = abs(padding)

        self.text_render = self.FONT.render(self.text, True, self.colour)
        self.height = max(self.text_render.get_height()+padding, self.height)

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.blit(self.text_render, self.text_render.get_rect(center = self.surface.get_rect().center))
        self.rect = pygame.Rect(self.x, self.y, self.width + self.padding, self.height + self.padding)
    
    #checks if cursor is over the surface of an input box, returns True if it is
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width + self.padding:
            if self.y < pos[1] < self.y + self.height + self.padding:
                return True
        return False

    #changes state of an input box
    #needed to grey out the input box to make it unactive
    def change_active(self, state = None):
        if state is not None:
            self.active = state
        else:
            self.active = not self.active

        if self.active:
            self.colour = self.COLOUR_ACTIVE
        else:
            self.colour = self.COLOUR_INACTIVE

    def change_text(self, string):
        self.text_render = self.FONT.render(string, True, self.colour)

    #main function of a input box where logic is done
    def handle_event(self, event):
        #checks of a type of event given as a parameter
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                #changes state of a box according to a cursor and if its clicked
                if self.is_over(event.pos):
                    self.change_active(True)
                else:
                    self.change_active(False)

        #handles typing in
        if event.type == pygame.KEYDOWN:
            
            if self.active:
                #if Enter is pressed while input box active
                if event.key == pygame.K_RETURN:
                    self.change_active(False) #doesnt return anything
                                            # as there would be submit button to fetch both input boxes text
                
                #handles delete of a text in an input box
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.display_text = self.display_text[:-1]
                
                else:
                    #unicode encoded key is passed, but it could be shift, ctrl or any other type of key
                    key = event.unicode
                    #neede a separate check of a key and the whole input as validation
                    to_check = self.text + key
                    if not re.search("[A-Za-z0-9@$!%*#?&-_ ]", key):
                        return
                        #returns False if key is not in allowed input characters
                    if not self.validate:
                        #if method validate is not set while declaring input box, 
                        # default regex check is called 
                    
                        if re.search("^[a-zA-Z0-9-_ ]{0,30}$", to_check):
                            
                            if self.password:
                                self.display_text += '*'
                                #if input box is made for a password input, '*' should be displayed instead
                                
                            else:
                                self.display_text += key
                            #to text variable checked key is added to make sure text isn't "*****" for password
                            self.text += key
                            self.changed = True
                    else:
                        #if validate method is passed in, its called and returns boolean for pass/not pass

                        if self.validate(to_check):
                            if self.password:
                                self.display_text += '*'
                            else:
                                self.display_text += key
                            self.text += key
                            self.changed = True

        self.text_render = self.FONT.render(self.display_text, True, self.colour)

    #procedure to set the width of input box
    def update(self):
        width = max(self.width_copy, self.text_render.get_width()+self.padding)
        self.width = width

    #procedure to draw input box on the screen
    def draw(self, screen):
        self.surface = pygame.Surface((self.width + self.padding, self.height + self.padding))
        self.surface.fill(self.INSIDE_COLOUR)
        self.surface.blit(self.text_render, self.text_render.get_rect(center = self.surface.get_rect().center))
        self.rect = pygame.Rect(self.x, self.y, self.width + self.padding, self.height + self.padding)
        screen.blit(self.surface, (self.x, self.y))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

#class for creating and button manipulations
class Button:
    def __init__(self, x, y, text, font, button_colour, hover_colour, text_colour, ID = None, command = None, margin = 0, width = None, height = None, active = True, inactive_colour = None, render = True): 

        self.x  = x
        self.y = y
        self.button_colour = button_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.font = font
        self.command = command
        self.margin = margin

        self.active = active
        self.inactive_colour = inactive_colour

        self.width = width
        self.height = height

        self.Text = text
        self.ID = ID
        
        self.size_up(text, self.font, self.text_colour, self.margin)

    #procedure to size button by adding margins and taking text width/height into account 
    def size_up(self, text, font, text_colour, margin = 0):

        self.text = font.render(text, 1, pygame.Color(text_colour))
        self.size = self.text.get_size()
        if self.width:
            self.width = max(self.size[0] + margin, self.width)
        else:
            self.width = self.size[0] + margin
        if self.height:
            self.height = max(self.size[1] + margin, self.height)
        else:
            self.height = self.size[1] + margin
    
    #procedure that draws the button. Also used to change color for hovering and default 
    def draw(self, screen, colour):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(colour)
        self.surface.blit(self.text, self.text.get_rect(center = self.surface.get_rect().center))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.surface, (self.x, self.y))

    def default(self, screen):
        if self.active:
            self.draw(screen, self.button_colour)
        else:
            self.draw(screen, self.inactive_colour)


    def hover(self, screen):
        if self.active:
            self.draw(screen, self.hover_colour)

    def change_text(self, text):
        self.size_up(text, self.font, self.text_colour, margin = 0)
    
    #function that returns boolean of mouse position over the button
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False



########   Regex


def validate_username(string):
#takes whole string as a parameter and checks length and inside of it
    if re.search("^[a-zA-Z0-9_-]{2,30}$", string):
        return True
    return False

def validate_name(string):
#takes whole string as a parameter and checks length and inside of it
#has to be only letters as name cannot consist of numerical values
    if re.search("^[a-zA-Z]{2,30}$", string):
        return True
    return False

def validate_password(string):
    #complex regex looks checks if sring is from 8 to 30 characters long 
    # and has at least 1 Uppercase, at least 1 ditit and at least 1 special character
    if re.search("^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#_?&-])[A-Za-z0-9@$!%*-_#?&]{8,30}$", string):
        return True
    return False

def check_username(string):
    #checks for username, must be max 30 characters long and has Upper, lower cased and numbers
    if re.search("^[a-zA-Z0-9_-]{,30}$", string):
        return True
    return False

def check_password(string):
    #checks that string is maximum 30 characters and has letters, numbers and special characters
    if re.search("^[a-zA-Z0-9@$!%*#?&-_]{,30}$", string):
        return True
    return False

def check_numbers(string):
    if re.search("^([1-9][0-9]?)$", string): #length of 2 with first digit is not 0
        return True
    return False

#class to check password in text-based form with hashed one
class PasswordCheck:
    #uses hashlob library to encode password and return hex value of it
    def encode(self, text):
        return hashlib.sha1(text.encode()).hexdigest()

    #compares encoded string to hashed value taken from database
    def check(self, text, pwd):
        if self.encode(text) == pwd:
            return True
        return False

#class used to convert maze 1s and 0s into 128 encoded.

class Binary128:
    #128 base
    #defined 64 characters in English alphabet 
    #and 64 more characters including special characters and Russian lowercase alphabet
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    add = """!"£$%^&*()¬`\|<.>/?;:'@#~[{]}абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБ"""

    charset +=add
    
    
    def encode(self, bin_string):
        # Split the string of 1s and 0s into lengths of 6.
        chunks = [bin_string[i:i+7] for i in range(0, len(bin_string), 7)]

        # Store the length of the last chunk so that we can add that as the last bit
        # of data so that we know how much to pad the last chunk when decoding.
        last_chunk_length = len(chunks[-1])
        # Convert each chunk from binary into a decimal
        decimals = [int(chunk, 2) for chunk in chunks]
        # Add the length of our last chunk to our list of decimals.
        decimals.append(last_chunk_length)
        # Produce an ascii string by using each decimal as an index of our charset.
        ascii_string = ''.join([self.charset[i] for i in decimals])

        return ascii_string

    def decode(self, ascii_string):
        # Convert each character to a decimal using its index in the charset.
        decimals = [self.charset.index(char) for char in ascii_string]
        # Take last decimal which is the final chunk length, and the second to last
        # decimal which is the final chunk, and keep them for later to be padded
        # appropriately and appended.
        last_chunk_length, last_decimal = decimals.pop(-1), decimals.pop(-1)
        # Take each decimal, convert it to a binary string (removing the 0b from the
        # beginning, and pad it to 6 digits long.
        bin_string = ''.join([bin(decimal)[2:].zfill(7) for decimal in decimals])
        # Add the last decimal converted to binary padded to the appropriate length
        bin_string += bin(last_decimal)[2:].zfill(last_chunk_length)

        return bin_string

#chass to make complete grid (1s and 0s) from binary value fetched from database
class MakeGrid:
    def __init__(self, ID, binary, Height, Width, start, end, showID = None, made_by = None):
        self.ID = ID
        self.BINARY = binary
        self.HEIGHT = Height
        self.WIDTH = Width
        self.start = start
        self.end = end
        self.area = (Height-2)*(Width-2)
        self.grid = []

        self.showID = showID
        self.made_by = made_by
    #combines following classes into 1 procedure
    def complete(self):
        self.addzeros()
        self.make_array()
        self.add_borders()

    #adds 0s to beginning of a string as first 0s in binary string are gettign deleted to help
    #to reduce size of a value in a table
    def addzeros(self):
        self.BINARY = '0'*(self.area-len(self.BINARY))+ str(self.BINARY)

    #makes multi-dimentional array out of a flat array
    #helps in a future to address rows and columns by indexing each
    def make_array(self):
        array = []
        index = 0
        for row in range(self.HEIGHT-2):
            arr = []
            for column in range(self.WIDTH-2):
                arr.append(self.BINARY[index])
                index+=1
            array.append(arr)
        self.grid = array
    
    #adds borders to array
    #as binary values are stripped in order to reduce key size
    def add_borders(self):
        #calculates how many 1s have to go in a single row
        ones = ['1'] * (len(self.grid[0])-2)
        #makes array of ones same width as grid's row - 2 to make corners
        self.grid.insert(0, ones)
        self.grid.append(ones)

        #adds 1s to first and last index of a row -> adds to columns and therefore makes vertical borders
        for row in range(len(self.grid)):
            self.grid[row].append('1')
            self.grid[row].insert(0,'1')

#procedure that allows to display long text in multiple lines using a single text input 
def blit_text(surface, text, pos = (0,0), font = None, max_width = 0, padding_left = 0, padding_right = 0, colour=pygame.Color('black')):
    #function must take 2 arguments: window itself and text, optional are: position of the text`s top left corner, pygame font, width of the text e.g. width of block in css/html
            #padding from both sides to control positions better and colour of the font
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.

    #if max_width wasn`t changed, it declares it as window`s width-padding
    if max_width == 0:
        max_width = surface.get_width() - padding_right - padding_right
    else:
        max_width = max_width - padding_left - padding_right

    #changes x-position of the pos tuple to add the paddinf up
    pos = list(pos)
    pos[0] += padding_left
    x, y = pos


    #iterates through each line in the 2D array
    for line in words:
        #iterates through each word in line
        for word in line:
            word_surface = font.render(word, 0, colour)
            word_width, word_height = word_surface.get_size()
            #checks if starting coordinate + width of the word is less than maximal width available
            # BUG: text can go off the edge because of max_width and starting position, however it won`t go off is starting positon is 0
            if x + word_width >= max_width + pos[0]:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space*2
        x = pos[0]  # Reset the x.
        y += word_height


#class for a stack (First in Last out structure) 
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
        
    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)
    
    def is_empty(self):
        return self.items == []

    def make_empty(self):
        self.items = []

    def reduce(self):
        return self.items[:-1]

#class for a Queue (First in First out structure) 
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        if not self.empty:
            return self.items.pop()
        return False

    def empty(self):
        return self.items == []

    def size(self):
        return len(self.items)


#merge sort algorithm used to sort only array of nodes in least gCost
def MergeSort(array):
    if len(array) > 1:
        mid = len(array)//2
        left = array[:mid]
        right = array[mid:]


        MergeSort(left)
        MergeSort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i].gCost < right[j].gCost:
                array[k] = left[i]
                i+=1
            else:
                array[k] = right[j]
                j+=1
            k+=1

        while i < len(left):
            array[k] = left[i]
            i+=1
            k+=1

        while j < len(right):
            array[k] = right[j]
            j+=1
            k+=1

    return array
