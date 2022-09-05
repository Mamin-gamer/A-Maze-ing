#imports to set up environment
try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hides hello message from pygame
    import pygame
    pygame.font.init()
except:
    print('No pygame installed')

#import all files of the game and test for all files presence 
try:
    import CreateDB
    import MakeGrid
    import Generate
    import Utils
    from Utils import Button
except:
    print('not all files downloaded')


from random import choice

import sqlite3 as sql


#Fonts
Font = pygame.font.SysFont('arial', 60)
SubFont = pygame.font.SysFont('arial', 30)
SmallFont = pygame.font.SysFont('arial', 17) 

#Colours
White = (255,255,255)
Black = (0,0,0)
Grey = (120, 120, 120)
LightGrey = (211, 211, 211)
Red = (255,0,20)
Green = (0,255,20)
Blue = (20,0,255)
Cyan = (112, 150, 225)
Yellow = (230, 225, 105)
LightBlue = (18, 231, 255)
Purple = (140, 10, 200)

#Main class to display window
class Window:
    FPS = 60
    def __init__(self, width = 1080, height = 720, caption = 'aMAZEing'):
        self.WIN_WIDTH = width
        self.WIN_HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption(caption)
    #refreshes window
    def display(self):
        pygame.display.update()
        pygame.display.flip()
       

#initial class for login page
class LoginPage(Window):
    start_x = 450
    #main loop that sets values and has main loop
    def on(self):
        self.LoginText = Font.render('Login', True, Black)
        self.UsernameText = SubFont.render('Username', True, Black)
        self.PasswordText = SubFont.render('Password', True, Black)

        #inputs for the login
        self.UsernameInput = Utils.InputBox(self.start_x, 250, 200, 30, validate = lambda x: Utils.check_username(x))
        self.PasswordInput = Utils.InputBox(self.start_x, 350, 200, 30, password=True, validate = lambda x: Utils.check_password(x))
        
        self.input_boxes = [self.UsernameInput, self.PasswordInput]
        #buttons for the menu
        quitbtn = Button(10, self.WIN_HEIGHT-80, 'Quit', SubFont, Black, Grey, White, command= 'return', margin = 10)
        submitbtn = Button(450, 400, 'Submit', SubFont, Grey, LightGrey, Black, command = lambda: self.submit_credentials_wrapper(), margin=10)
        forgotpwd = Button(850, 400, 'Forgot Password?', SubFont, Grey, LightGrey, Black, command = lambda: self.forgot_password_wrapper(), margin=10)
        createacc = Button(400, 600, 'Create new account', SubFont, Grey, LightGrey, Black, command = lambda: self.create_account(), margin=10)
        
        self.buttons = [quitbtn, submitbtn, forgotpwd, createacc]
        
        self.draw_all()
        #main loop
        run = True
        while run:
            self.display()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    return False

                pos = pygame.mouse.get_pos()


                self.draw_all()
                self.draw_inputs()
                
                #return can be different depending on what record outputs
                try:
                    if resume == 'wrong pwd':
                        self.blit_wrong_pwd()
                    if resume == 'no record':
                        self.blit_no_record()
                except:
                    pass
                #updates input boxes
                for box in self.input_boxes:
                    box.handle_event(event)
                #updates buttons
                for btn in self.buttons:
                    
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                        
                        #registers mouse left click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:

                                    #completes the command and must have a return
                                    resume = btn.command()
                                    #if returned parameter is not False
                                    if resume != False:
                                        #if resume is none, no update is done
                                        if resume == None:
                                            continue
                                        #if resume is True, it causes update of the screen
                                        if resume == True:
                                            self.draw_buttons()
                                            self.draw_all()
                                    else:
                                        #if resume is false, program stops running
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN) 

                

        return False  
    #procedure to display text on screen
    def draw_writings(self):
        self.WIN.blit(self.LoginText, (self.start_x, 50))
        self.WIN.blit(self.UsernameText, (self.start_x, 200))
        self.WIN.blit(self.PasswordText, (self.start_x, 300))

    #procedure to draw all buttons
    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.WIN, btn.button_colour)

    #procedure to draw all inputs
    def draw_inputs(self):
        for box in self.input_boxes:
            box.update()
            box.draw(self.WIN)

    #procedure that combines drawing text and buttons
    def draw_all(self):
        self.WIN.fill(White)
        self.draw_writings()
        self.draw_buttons()

    #wrapper for function that allows return to be possible
    def create_account(self):
        return Register().on()

    #wrapper for function for people who forgot password that allows return to be possible
    def forgot_password_wrapper(self):
        return ForgotPassword().on()

    #wrapper for funciton to submit credentials
    def submit_credentials_wrapper(self):
        return self.submit_credentials()

    #function that sunbmits credentials
    def submit_credentials(self):
        username = self.UsernameInput.text
        password = self.PasswordInput.text
        conn = sql.connect('DataBase.db') 
        #fetches username from table User
        c = conn.cursor()
        c.execute(f"""
            SELECT Username, Password
            FROM User
            WHERE Username = '{username}'
        """)
        row = c.fetchone()
        
        if row:
            name = row[0]
            pwd = row[1]
            #compares password from table to hashed one using hashlib
            if Utils.PasswordCheck().check(password, pwd):
                #makes USERNAME global to allow to use it anywhere in the code
                global USERNAME
                USERNAME = self.UsernameInput.text
                #resets input boxes to increase security of login, as text could be seen after returning to previous page
                self.UsernameInput.text = ''
                self.UsernameInput.display_text = ''
                self.PasswordInput.text = ''
                self.PasswordInput.display_text = ''
                resume = MainMenu().on()
                return resume
            else:
                #if passwords don't match, it makes input boxes empty
                self.PasswordInput.text = ''
                self.PasswordInput.display_text = ''
                return 'wrong pwd'
            

        else:
            return 'no record'

    #displays text if record is not found
    def blit_no_record(self):
        text = SubFont.render("User does't exist ", True, Red)
        self.WIN.blit(text, (700, 300))
    

    #displays text if password is wrong
    def blit_wrong_pwd(self):
        text = SubFont.render('Wrong password', True, Red)
        self.WIN.blit(text, (700, 300))

#class that deals with users who forgot their password
class ForgotPassword(Window):
    start_x = 450
    #main loop that declares variabels and contains main loop
    def on(self):
        #sets up texts
        self.RestoreText = Font.render('Restore Password', True, Black)
        self.UsernameText = SubFont.render('Username', True, Black)
        self.NameText = SubFont.render('First Name', True, Black)
        self.SurnameText = SubFont.render('Surname', True, Black)


        self.username_should_be = SubFont.render('Password Requirements:', True, Black)
        self.numofchar = SmallFont.render('At least 8 characters', True, Black)
        self.oneupper = SmallFont.render('At least 1 upper case', True, Black)
        self.onelower = SmallFont.render('At least 1 lower case', True, Black)
        self.onedigit = SmallFont.render('At least 1 digit', True, Black)
        self.onespecial = SmallFont.render('At least 1 special symbol', True, Black)
        
        #sets up input boxes
        self.UsernameInput = Utils.InputBox(self.start_x, 250, 200, 30, validate = lambda x: Utils.check_username(x))
        self.NameInput = Utils.InputBox(self.start_x, 350, 200, 30)
        self.SurnameInput = Utils.InputBox(self.start_x, 450, 200, 30)

        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, Black, Grey, White, command= 'return', margin = 10)
        submitbtn = Button(450, 600, 'Submit', SubFont, Grey, LightGrey, Black, command = lambda: self.check_input_wrapper(), margin=10)
        #places buttons in an array for iteration, which allows to get each button's function individually
        self.buttons = [returnbtn, submitbtn]
        self.input_boxes = [self.UsernameInput, self.NameInput, self.SurnameInput]

        #uses 2-step verification as needed for security reasons
        self.Password1Input = Utils.InputBox(self.start_x, 250, 200, 30, validate = lambda x: Utils.check_password(x), password=True)
        self.Password2Input = Utils.InputBox(self.start_x, 350, 200, 30, validate = lambda x: Utils.check_password(x), password=True)
        
        self.PasswordText = SubFont.render('New Password', True, Black)
        self.Password2Text = SubFont.render('Repeat New Password', True, Black)
        
        submitbtn2 = Button(450, 600, 'Submit', SubFont, Grey, LightGrey, Black, command = lambda: self.check_input2(), margin=10)

        self.buttons2 = [returnbtn, submitbtn2]
        self.input_boxes2 = [self.Password1Input, self.Password2Input]

        #first main loop that asks for username to check with table if exists
        self.draw_all()
        run = True
        while run:
            self.display()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    return False

                pos = pygame.mouse.get_pos()

                self.draw_all()
                self.draw_inputs()
                
                #displays text depending on returned value from subroutine
                try: 
                    if resume == 'username wrong':
                        self.blit_username_not_valid()
                    if resume == 'name not valid':
                        self.blit_name_not_valid()
                    if resume == 'surname not valid':
                        self.bit_surname_not_valid()
                    if resume == 'not exist':
                        self.blit_not_exist()
                except:
                    pass
                #updates boxes
                for box in self.input_boxes:
                    box.handle_event(event)
                #draws buttons
                for btn in self.buttons:
                    
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        if resume == True:
                                            self.draw_buttons()
                                            self.draw_all()
                                        if resume == 'menu':
                                            #goes to menu instead of refreshing and staying on this page
                                            return True
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False

    #procedure that combines drawing buttons and text
    def draw_all(self):
        self.WIN.fill(White)
        self.draw_buttons()
        self.draw_writings()
        
    #procedure to draw buttons
    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.WIN, btn.button_colour)
    
    #procedure to draw text
    def draw_writings(self):
        self.WIN.blit(self.RestoreText, (self.WIN_WIDTH//2- self.RestoreText.get_width()//2, 50))
        self.WIN.blit(self.UsernameText, (self.start_x, 200))
        self.WIN.blit(self.NameText, (self.start_x, 300))
        self.WIN.blit(self.SurnameText, (self.start_x, 400))

    #procedure to draw and update input boxes
    def draw_inputs(self):
        for box in self.input_boxes:
            box.update()
            box.draw(self.WIN)
    #wrapper for checking input funnction that will open another window
    def check_input_wrapper(self):
        return self.check_input1()
    #function that validates username, first name and surname and if all correct, allows to reset the password
    def check_input1(self):
        username = self.UsernameInput.text
        name = self.NameInput.text
        surname = self.SurnameInput.text
        #uses method validate_ to return Boolean of correctly inputted characters
        username_valid = Utils.validate_username(username)
        name_valid = Utils.validate_name(name)
        surname_valid = Utils.validate_name(surname)

        if not username_valid:
            return 'username wrong'

        if not name_valid:
            return 'name not valid'
        
        if not surname_valid:
            return 'surname not valid'

        #if either of validations are passed, program continues to run, otherwise text is displayed with an error stating
        
        #connects to database and checks against 3 parameters
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(f"""
            SELECT Username, FirstName, Surname
            FROM User
            WHERE Username = '{username}' AND FirstName = '{name}' AND Surname = '{surname}'
        """)
        #Its given that username is unique, therefore there can be only 1 entity, therefore fetching only 1 entry
        row = c.fetchone()

        if row:
            #setting USERNAME as global for future fetching and using
            global USERNAME
            USERNAME = row[0]
            return self.restore()
        else:
            return 'not exist'
    #if credentials are correct, allows to input new password

    #function that calls new window and allows to input new password 
    def restore(self):
        self.draw_all2()
        run = True
        while run:
            self.display()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()
                #allows input of input box to be registered and updated
                for box in self.input_boxes2:
                    box.handle_event(event)

                self.draw_all2()
                self.draw_inputs2()
                       
                try:
                    if resume == 'password1 valid':
                        self.blit_first_not_valid()
                    if resume == 'password2 valid':
                        self.blit_second_not_valid()
                    if resume == 'no match':
                        self.blit_pwd_match()

                except:
                    pass
                
                #iterated through each button to get it'c command and lets to complete it
                for btn in self.buttons2:
                    
                    if btn.is_over(pos):
                        #if cursor is over the button, it should change colour to be more interractive
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        if resume == True:
                                            self.draw_all2()
                                            return True
                                        if resume == 'menu':
                                            return 'menu'
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False 
    #procedure to draw text
    def draw_writings2(self):
        self.WIN.blit(self.RestoreText, (self.WIN_WIDTH//2- self.RestoreText.get_width()//2, 50))
        self.WIN.blit(self.PasswordText, (self.start_x, 200))
        self.WIN.blit(self.Password2Text, (self.start_x, 300))
        self.WIN.blit(self.username_should_be, (20, 150))
        self.WIN.blit(self.numofchar, (20, 250))
        self.WIN.blit(self.oneupper, (20, 300))
        self.WIN.blit(self.onelower, (20, 350))
        self.WIN.blit(self.onedigit, (20, 400))
        self.WIN.blit(self.onespecial, (20, 450))   
    #procedure to draw buttons
    def draw_buttons2(self):
        for btn in self.buttons2:
            btn.draw(self.WIN, btn.button_colour)

    #procedure to draw input boxes
    def draw_inputs2(self):
        for box in self.input_boxes2:
            box.update()
            box.draw(self.WIN)
    #procedure that combines drawing input boxes and buttons
    def draw_all2(self):
        self.WIN.fill(White)
        self.draw_writings2()
        self.draw_buttons2()

    #wrapper to call check input e.g. input new password
    def check_input2_wrapper(self):
        return self.check_input2()
    #main funciton to input passwords to be reset
    def check_input2(self):
        pwd1 = self.Password1Input.text
        pwd2 = self.Password2Input.text

        #uses Utils.validate_ method to validate password and check if they meet all criterias
        pwd1_valid = Utils.validate_password(pwd1)
        pwd2_valid = Utils.validate_password(pwd2)

        if not pwd1_valid:
            return 'password1 valid'
        if not pwd2_valid:
            return 'password2 valid'
        
        if pwd1 != pwd2:
            return 'no match'
        
        #if all criterias were met, program continues to run with no problems, otherwise returns error message 
        #explaining which password is invalid


        #connect to database and update password based on username
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        #updates User's password with encrypted version of it Using Utils.encode method 
        c.execute(f"""
                UPDATE User 
                SET Password = '{Utils.PasswordCheck().encode(pwd1)}'
                WHERE Username = '{USERNAME}'
           """)
        conn.commit()
        #return menu to come back to menu
        return 'menu'

        

###### Displaying errors ########
    def blit_first_not_valid(self):
        text = SubFont.render('Password 1 Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_second_not_valid(self):
        text = SubFont.render('Password 2 Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_pwd_match(self):
        text = SubFont.render("Passwords don't match", True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_username_not_valid(self):
        text = SubFont.render('Username Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))
    
    def blit_name_not_valid(self):
        text = SubFont.render('Name Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))
    
    def bit_surname_not_valid(self):
        text = SubFont.render('Surname Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_not_exist(self):
        text = SubFont.render("Record does't exist", True, Red)
        self.WIN.blit(text, (700, 300))

#Class to create new account
class Register(Window):
    start_x = 450

    #main loop which first asks for Username and Password to be set
    def on(self):
        #sets texts to show up
        self.RegisterText = Font.render('Register', True, Black)
        self.UsernameText = SubFont.render('Username', True, Black)
        self.PasswordText = SubFont.render('Password', True, Black)
        self.Password2Text = SubFont.render('Repeat password', True, Black)

        self.Question = Font.render('Security Questions', True, Black)
        self.FirstNameText = SubFont.render('First Name', True, Black)
        self.SurnameText = SubFont.render('Surname', True, Black)
    

        #####HELP SECTION######
        self.username_should_be = SubFont.render('Password Requirements:', True, Black)
        self.numofchar = SmallFont.render('At least 8 characters', True, Black)
        self.oneupper = SmallFont.render('At least 1 upper case', True, Black)
        self.onelower = SmallFont.render('At least 1 lower case', True, Black)
        self.onedigit = SmallFont.render('At least 1 digit', True, Black)
        self.onespecial = SmallFont.render('At least 1 special symbol', True, Black)
        

        self.UsernameInput = Utils.InputBox(self.start_x, 250, 200, 30, validate = lambda x: Utils.check_username(x))
        self.PasswordInput = Utils.InputBox(self.start_x, 350, 200, 30, password=True, validate = lambda x: Utils.check_password(x))
        self.Password2Input = Utils.InputBox(self.start_x, 450, 200, 30, password=True, validate = lambda x: Utils.check_password(x))
        
        self.FirstNameInput = Utils.InputBox(self.start_x, 250, 200, 30)
        self.SurnameInput = Utils.InputBox(self.start_x, 350, 200, 30)

        #input boxes are placed into array for iteration and individual updates 
        self.input_boxes = [self.UsernameInput, self.Password2Input, self.PasswordInput]
        self.input_boxes2 = [self.FirstNameInput, self.SurnameInput]

        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, Black, Grey, White, command= 'return', margin = 10)
        submitbtn = Button(450, 600, 'Submit', SubFont, Grey, LightGrey, Black, command = lambda: self.check_input(), margin=10)
        submitbtn2 = Button(450, 600, 'Submit', SubFont, Grey, LightGrey, Black, command = lambda: self.check_input2(), margin=10)

        #buttons are places in an array for iteration over them and individual commands
        self.buttons = [returnbtn, submitbtn]
        self.buttons2 = [returnbtn, submitbtn2]


        self.draw_all()
        #main loop to ask for username and 2 passwords
        run = True
        while run:
            self.display()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()

                self.draw_all()

                #section to display errors occured during regestering are diaplayed
                try:
                    if resume == 'username wrong':
                        self.blit_username_not_valid()
                    
                    if resume == 'username taken':
                        self.blit_username_taken()

                    if resume == 'password 1 wrong':
                        self.blit_password1_not_valid()
                    
                    if resume == 'password 2 wrong':
                        self.blit_password2_not_valid()

                    if resume == 'passwords match':
                        self.blit_passwords_match()

                except:
                    pass


                self.draw_inputs()
                #updates input boxes
                for box in self.input_boxes:
                    box.handle_event(event)


                #updates buttons
                for btn in self.buttons:
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        if resume == True:
                                            self.draw_buttons()
                                            self.draw_all()
                                            return True
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False  
    #subroutine to clear out inputs 
    def empty_fields(self, inputs):
        for inp in inputs:
            inp.text = ''
            inp.display_text = ''
    
##### Display text, buttons and Input boxes######
    def blit_username_not_valid(self):
        text = SubFont.render('Username Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))
    
    def blit_password1_not_valid(self):
        text = SubFont.render('Password 1 Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_password2_not_valid(self):
        text = SubFont.render('Password 2 Not Valid', True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_passwords_match(self):
        text = SubFont.render("Passwords don't match", True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_username_taken(self):
        text = SubFont.render("Username already taken", True, Red)
        self.WIN.blit(text, (700, 300))

    def blit_first_not_valid(self):
        text = SubFont.render("First name not valid", True, Red)
        self.WIN.blit(text, (700, 300))
    
    def blit_surname_not_valid(self):
        text = SubFont.render("Surname not valid", True, Red)
        self.WIN.blit(text, (700, 300))
    
    def draw_writings2(self):
        self.WIN.blit(self.Question, (self.WIN_WIDTH//2- self.Question.get_width()//2, 50))
        self.WIN.blit(self.FirstNameText, (self.start_x, 200))
        self.WIN.blit(self.SurnameText, (self.start_x, 300))
       
    #method to draw buttons1
    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.WIN, btn.button_colour)
    #method to draw buttons2
    def draw_buttons2(self):
        for btn in self.buttons2:
            btn.draw(self.WIN, btn.button_colour)
    #method to draw inputs1
    def draw_inputs(self):
        for box in self.input_boxes:
            box.update()
            box.draw(self.WIN)
    #method to draw inputs2
    def draw_inputs2(self):
        for box in self.input_boxes2:
            box.update()
            box.draw(self.WIN)
    #method to draw everything1
    def draw_all(self):
        self.WIN.fill(White)
        self.draw_writings()
        self.draw_buttons()
    #method to draw everything2
    def draw_all2(self):
        self.WIN.fill(White)
        self.draw_writings2()
        self.draw_buttons2()
    #wrapper method to call next functon in case every check is passed
    def check_input(self):
        return self.check_input1()
#function to validates username and checks agaist database
    def check_input1(self):
        username = self.UsernameInput.text
        password = self.PasswordInput.text
        password2 = self.Password2Input.text

        #validats username and passwords using Utils.validate_ methods
        username_valid = Utils.validate_username(username)
        pwd_valid = Utils.validate_password(password)
        pwd_valid2 = Utils.validate_password(password2)

        if not username_valid:
            return 'username wrong'
        if not pwd_valid:
            return 'password 1 wrong'

        if not pwd_valid2:
            return 'password 2 wrong'

        if password != password2:
            return "passwords match"
        #connects to database and fetches username
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(f"""
            SELECT Username
            FROM User
            WHERE Username = '{username}'
        """)
        row = c.fetchone()
        #if username is in databse, then returns error as usernames are unique
        if row:
            return 'username taken'

        self.USERNAME = username
        resume = self.submit()
        return resume 

    #asks user to input his first name and surname for easier password reset
    def submit(self):
        self.draw_all2()
        run = True
        while run:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break
                self.draw_all2()
                
                pos = pygame.mouse.get_pos()

                for box in self.input_boxes2:
                    box.handle_event(event)
                #error handling         
                try:
                    if resume == 'first not valid':
                        self.blit_first_not_valid()
                    if resume == 'second not valid':
                        self.blit_surname_not_valid()

                except:
                    pass

                self.draw_inputs2()

                for btn in self.buttons2:
                    self.display()
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        if resume == True:
                                            self.draw_all2()
                                            return True
                                        
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False 

    def check_input2(self):
        return self.check_input3()
    #function to inserts value in a table Users after validating them
    def check_input3(self):
        first_name = self.FirstNameInput.text
        surname = self.SurnameInput.text

        #uses Utils.valivate_ methods to validate first and last name
        #BUG: doesnt allow names with spaces e.g. St Clair or Al Jorani
        first_name_valid = Utils.validate_name(first_name)
        surname_valid = Utils.validate_name(surname)

        if not first_name_valid:
            return 'first not valid'
        if not surname_valid:
            return 'second not valid'

        #connects to a database and inserts into table Users
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute("""
            INSERT INTO User (Username, FirstName, Surname, Password)
                            VALUES(?,?,?,?)""", (self.USERNAME, first_name, surname, Utils.PasswordCheck().encode(self.PasswordInput.text)))
        
        conn.commit()

        global USERNAME
        USERNAME = self.UsernameInput.text
        #empties fields and connects to main menu
        self.empty_fields(self.input_boxes)
        self.empty_fields(self.input_boxes2)
        return True
        
    #requirements for password to be
    def draw_writings(self):
        self.WIN.blit(self.RegisterText, (self.WIN_WIDTH//2- self.RegisterText.get_width()//2, 50))
        self.WIN.blit(self.UsernameText, (self.start_x, 200))
        self.WIN.blit(self.PasswordText, (self.start_x, 300))
        self.WIN.blit(self.Password2Text, (self.start_x, 400))
        self.WIN.blit(self.username_should_be, (20, 150))
        self.WIN.blit(self.numofchar, (20, 250))
        self.WIN.blit(self.oneupper, (20, 300))
        self.WIN.blit(self.onelower, (20, 350))
        self.WIN.blit(self.onedigit, (20, 400))
        self.WIN.blit(self.onespecial, (20, 450))


        
        
#main class where In-built levels, Worshop and Sandbox can be called
class MainMenu(Window):
    start_x = 450
    def on(self):

        self.MainMenuText = Font.render('Main Menu', True, Black)
        #sets buttons that call wrappers 
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, Black, Grey, White, command= 'return', margin = 10)
        levelsbtn = Button(self.start_x, 250, 'Levels', SubFont, Grey, LightGrey, Black, command = lambda: self.call_levels(), margin=10)
        workshopbtn = Button(self.start_x, 350, 'Workshop', SubFont, Grey, LightGrey, Black, command = lambda: self.call_workshop(), margin=10)
        sandboxbtn = Button(self.start_x, 450, 'Sandbox', SubFont, Grey, LightGrey, Black, command = lambda: self.sandbox_wrapper(), margin = 10)
        credits = Button(self.start_x, 600, 'Credits', Font, White, White, Black, command=lambda: self.credits_wrapper())
        
        #buttons are placed in an array for iteration over them to allow to fetch individual's funciton for them and update
        self.buttons = [returnbtn, levelsbtn, sandboxbtn, credits, workshopbtn]

        
        self.draw()
        #main loop cheking button behaviour and calls its functions
        run = True  
        while run:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()

                for btn in self.buttons:
                    self.display()
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        self.draw()
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False 
    #wrappers to call next function, without them nothing would be returned and it would be problematic to uodate the screen
    def call_levels(self):
        return Levels().on()

    def call_workshop(self):
        return Workshop().on()

    def sandbox_wrapper(self):
        return Sandbox().on()

    def credits_wrapper(self):
        return Credits().on()


##### Drawing section ######
    def draw(self):
        self.WIN.fill(White)
        self.draw_buttons()
        self.draw_writings()

    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.WIN, btn.button_colour)
        self.display()

    def draw_writings(self):
        self.WIN.blit(self.MainMenuText, (self.WIN_WIDTH//2- self.MainMenuText.get_width()//2, 50))

 


#Credits class that was implemented to show function to deal with multi-line text
class Credits(Window):
    def on(self):
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, Black, Grey, White, command= 'return', margin = 10)
        self.buttons = [returnbtn]
        
        #main loop to refresh text
        run = True
        while run:
            self.display()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()

                self.blit_writings()
    
                for btn in self.buttons:
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command == 'return':
                                    return True
                                else:
                                    resume = btn.command()
                                    if resume != False:
                                        if resume == None:
                                            continue
                                        if resume == True:
                                            self.draw_buttons()
                                            self.blit_writings()
                                            return True
                                    else:
                                        run = False
                                        break
                        
                    else:
                        btn.default(self.WIN)
        
        return False  
        
    def blit_writings(self):
        self.WIN.fill(White)
        #text can be modified and displayed on the screen with set parameters
        text = "Made by Dmitrii Ponomarev\n\nFull credited by me and my mates DN and I(HA-HA)"
        Utils.blit_text(self.WIN, text, pos = (50, 50), font = Font, max_width = 800)
        


#class node that is responsible for solving mazes
class Node:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent

        #fCost is the total cost of the node
        #hCost is distance between current node and end's node
        #gCost is distance between current node and end's node
        #length is total distance incuting cutting corners, which isn't used in this program, as diagonal moves are't allowed
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.length = 0

        

    def calc_fCost(self, end_node):
        #checking is parent exists (not start and end) and makes g cost and f cost
        if self.parent:
            a = abs(self.pos[0] - end_node.pos[0])
            b = abs(self.pos[1] - end_node.pos[1])
            #simple Pythagorean theorem used e.g. A^2 + B^2 = C^2
            self.gCost = self.parent.gCost + ((self.pos[0]-self.parent.pos[0])**2 + (self.pos[1]-self.parent.pos[1])**2 )**0.5
            self.length = ((self.pos[0]-self.parent.pos[0])**2 + (self.pos[1]-self.parent.pos[1])**2 )**0.5
            self.hCost = a+b

            self.fCost = self.gCost + self.hCost
    
    #allows to compare node's coordinates
    def __eq__(self, others):
        if self.pos == others.pos:
            return True
        else:
            return False

#class solving to show process of solving the grid
class Solving(Window):
    def __init__(self, level):
        #inherits __init__ method from Window to allow the use of display and WINDOW_WIDTH and HEIGHG
        super().__init__()
        self.moves = 0
        #sets up a trail as a stack as a path
        self.trail = Utils.Stack()
        
        self.grid = level.grid
        self.start_pos = level.start
        self.end_pos = level.end
        #sets start and end nodes 
        self.start_node = Node(self.start_pos, None)
        self.end_node = Node(self.end_pos, None)

        #sets constants (CAPITALS) for easier identification, as there is no constants in Python
        self.WIDTH = level.WIDTH
        self.HEIGHT = level.HEIGHT
        self.node_pos = self.start_pos

        self.start = True
        #starts stack by pushing start node at the very beginning
        self.trail.push(self.start_node)
    
    ######### moding node procedures ############ 
    def move_left(self, parent):

        if self.check_boundaries(0, -1):
            #if in boundary, sets node's position to a wall
            if self.grid[self.node_pos[0]][self.node_pos[1]-1] != '1': #wall
                self.node_pos = (self.node_pos[0], self.node_pos[1]-1)
                self.moves+=1
                #adds 1 to moves to track how many moved the player did
                node = Node((self.node_pos[0],self.node_pos[1]), parent)

                #pushed node created to the stack to allow tracking back
                self.trail.push(node)

        
    def move_right(self, parent):
        #if in boundary, sets node's position to a wall

        if self.check_boundaries(0, 1):
            if self.grid[self.node_pos[0]][self.node_pos[1]+1] != '1': #wall
                self.node_pos = (self.node_pos[0], self.node_pos[1]+1)
                self.moves+=1
                #adds 1 to moves to track how many moved the player did
                node = Node((self.node_pos[0],self.node_pos[1]), parent)

                #pushed node created to the stack to allow tracking back
                self.trail.push(node)

    def move_down(self, parent):
        #if in boundary, sets node's position to a wall
        if self.check_boundaries(1, 0):
            if self.grid[self.node_pos[0]+1][self.node_pos[1]] != '1':
                self.node_pos = (self.node_pos[0]+1, self.node_pos[1])
                self.moves+=1
                #adds 1 to moves to track how many moved the player did
                node = Node((self.node_pos[0],self.node_pos[1]), parent)
                
                #pushed node created to the stack to allow tracking back
                self.trail.push(node)

    def move_up(self, parent):
        #if in boundary, sets node's position to a wall
        if self.check_boundaries(-1, 0):
            if self.grid[self.node_pos[0]-1][self.node_pos[1]] != '1':
                self.node_pos = (self.node_pos[0]-1, self.node_pos[1])
                self.moves+=1
                #adds 1 to moves to track how many moved the player did
                node = Node((self.node_pos[0],self.node_pos[1]), parent)

                #pushed node created to the stack to allow tracking back
                self.trail.push(node)

    #function to check boundaries by adding row and column attributes to node's position to check if next node withing the allowed space
    def check_boundaries(self, row, col):
        if 0 <= self.node_pos[1] + col < self.WIDTH:
            if 0 <= self.node_pos[0] + row < self.HEIGHT:
                return True
        return False

    #function that checks if node's position is end's position
    def check_end(self):
        if self.node_pos == self.end_pos:
            self.start = False
            return True
        return False
        
    
    #function to show path by poping items from stack
    def show_path(self):
        for i in range(self.trail.size()):
            node = self.trail.pop()
            row, col = node.pos
            if self.grid[row][col] not in [1,2,3]:
                self.grid[row][col] = '4' #path number
    
    #procedure that displays text on the screen and how many moves it took to complete
    def blit_ending(self, moves):
        text = Font.render(f'Well done, it took you {moves} moves', True, Red)
        self.WIN.blit(text, (self.WIN_WIDTH//2- text.get_width()//2, 350))

# main class for All levels includint worshop and in-built levels
class AllLevels(Window):
    #sets class global variables, that can be accesses anywhere within this class
    #better to set it up like that, not in __init__ method to avoid many variables there and devide variables and constants 
    gap_x = 150
    gap_y = 200
    button_num = 5
    btn_rows = 2
    button_width = 100
    button_height = 100
    
    panel_x = 100
    panel_y = 0
    #sets constant global Font for this class
    FontNumbers = pygame.font.SysFont('arial', 80)

    #subroutine that fetches levels from table
    def fetch_levels(self, inbuilt = True):

        #connects to database and uses JOIN method to connect table Maze and Uploaded to get the creator of each maze
        #if its in-built, creator will be none and therefore sent to Workshop rather than Levels class
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute(f"""   SELECT Maze.MazeID, Maze.Base128, Maze.Inbuilt, Maze.Width,
                            Maze.Height, Maze.StartX, Maze.StartY, Maze.EndX, Maze.EndY, Uploaded.Username
                            FROM Maze
                            LEFT JOIN Uploaded
                            ON Maze.MazeID = Uploaded.MazeID
                    """)

        conn.commit()
        row = curr.fetchall()
        
        count = 0
        self.levels = []
        # _ is used to show that variable is not used anywhere, which won't affect anything
        for _, entity in enumerate(row):
            #goes through each fetched entry and assigns to a parameter to be passes to Utils.MakeGrid functon
            mazeID, base128, Inbuilt, Width, Height, StartX, StartY, EndX, EndY, MadeBy = entity
            if MadeBy:
                MadeBy = MadeBy[:5] #only first 5 letters used
                
            Start = (StartX, StartY)
            End = (EndX, EndY)
            binary = Utils.Binary128().decode(base128)
            
            #if fetched Inbuilt matches with inbuilt passed as a parameter, it will be displayed, othersise it will be skipped  
            if inbuilt == Inbuilt:
                count+=1
                lvl = Utils.MakeGrid(mazeID, binary, Height, Width, Start, End, showID=count, made_by=MadeBy)
                lvl.complete()
                self.levels.append(lvl)


    #procedure that fetches ID's to be assigned to in-built levels
    def fetch_ID(self):
        IDs = []
        for lvl in self.levels:
            IDs.append(lvl.showID)
        
        self.IDs = IDs

    #function to add tiles on the screen     
    def add_buttons(self, inbuilt = True, bunch = 0):
        copy = bunch
        btns_on = self.btn_rows*self.button_num
        start_num = bunch * btns_on
        
        #creates array of buttons with initial button of a return to set undex equal to button's ID for easier ID and understading
        self.buttons = [self.buttons[0]]
        list_ID = self.IDs[start_num: start_num + btns_on]

        start_x = x = 200
        start_y = y = 200
        
        #algorithms to add level buttons in array of buttons with its position
        adder = 0
        row = 0
        column = 0
        for adder in range(len(list_ID)):
            #iterates through length of ID fetched in a function above
            if inbuilt:
                #if levels to be displaed are inbuilt, its ID should be displayed
                btn = Button(x, y, str(list_ID[adder]), self.FontNumbers, button_colour = Grey, hover_colour = LightGrey, text_colour = Black, ID = list_ID[adder], margin = 20, height = 100, width = 100, active = False, inactive_colour=(100,100,0))
            else:
                #if levels to be displayed are made by user, first 5 letters of a name should be displayed
                name = self.levels[adder].made_by
                btn = Button(x, y, str(name), SubFont, button_colour = Grey, hover_colour = LightGrey, text_colour = Black, ID = list_ID[adder], margin = 20, height = 100, width = 100)

            #on each iteration, row is added to move position of a button
            row+=1
            #button is added to array buttons for iteration
            self.buttons.append(btn) 
            x += self.gap_x
            #if row equals to pre-set max number of buttons in a row, row is set to 0 to start a new row and y increases to move buttons down
            if row == self.button_num:
                row = 0
                x = start_x
                y+=self.gap_y
            column +=1


        #adds next and previous buttons
        #previous button is added when bunch is greater than 0, meaning that it was already on page 2
        if bunch > 0:
            prev_btn = Button(40, 400, 'Previous', SubFont, button_colour = Black, hover_colour = Grey, text_colour = LightGrey, margin = 5, width = 100, command = lambda: self.add_buttons(bunch = copy-1, inbuilt=inbuilt))
            self.buttons.append(prev_btn)

        #next button is added when number of ID in a list os greater that buttons displayed
        if len(list_ID) >= btns_on:
            next_btn = Button(self.WIN_WIDTH-150, 400, 'Next', SubFont, button_colour = Black, hover_colour = Grey, text_colour = LightGrey, margin = 5, width = 100, command = lambda: self.add_buttons(bunch = copy+1, inbuilt=inbuilt))
            self.buttons.append(next_btn)
        #fetches all solved levels from the tale and unlocks them plus unlocks the next one to be solved
        if inbuilt:
            self.get_solved()

            str_solved_IDs = list(map(str, self.solved_IDs))
            for btn in self.buttons:
                if btn.Text in str_solved_IDs:
                    btn.active = True
                
        return True #so it would refresh
        
    #functon to build a level to be able to solve it
    def build_level(self, ID, inbuilt): 
        solved = False  
        #copy here to update levels as I overwrite level when showing paths
        self.fetch_levels(inbuilt = inbuilt) 
        
        #iterates thougs levels in an array to understand which level to show
        for index, lvl in enumerate(self.levels):
            if lvl.showID == ID:
                break
        #level is fetched from the array and grid is assigned to self.grid for use in a class
        level = self.levels[index]
        self.grid = level.grid

        #starting node is made
        self.node = Solving(level)
        #level is generated with set parameters in a level class itself
        self.generate(level)
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, (Black), (Grey), (White), command= 'return', margin = 10)
        
        buttons = [returnbtn]

        #main loop to display elements
        self.Draw()
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()
                if not solved:
                    self.draw_grid(level)

                for btn in buttons:
                    self.display()

                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command:
                                    if btn.command == 'return':
                                        return True
                                    else:
                                        resume = btn.command()
                                        if resume != False:
                                            if resume == None:
                                                continue
                                            self.Draw()
                                            self.draw_grid(level)
                                        else:
                                            run = False
                                            break

                       
                        
                    else:
                        btn.default(self.WIN)  

                ########## movement or a node ############
                if self.node.start:
                    if event.type == pygame.KEYDOWN:
                        #pygame detects what key was pressed and calls specific function for it
                        if event.key == pygame.K_LEFT:
                            self.node.move_left(self.node)
                        if event.key == pygame.K_RIGHT:
                            self.node.move_right(self.node)

                        if event.key == pygame.K_UP:
                            self.node.move_up(self.node)
                        if event.key == pygame.K_DOWN:
                            self.node.move_down(self.node)
                        
                        solved = self.node.check_end()
                        if solved:
                            #if maze was solved, meaning that user reached the end node, path is shown to signify that level is complete
                            self.node.show_path()
                            self.draw_grid(level)
                            self.node.blit_ending(self.node.moves)
                            #displays text stating that level was indeed solved
                            
                            if inbuilt == True:
                                #if level is inbuilt and it was the last one available to the player, next one is unlocked
                                if ID == max(self.solved_IDs):
                                    self.get_next_level()
                                else:
                                    self.insert_level_solved(ID)
                            else:
                                self.insert_level_solved(ID)
                        

        return False

    #procedure that generates level and centers the window to it would be same gap on top and botton
    def generate(self, level):
        HEIGHT = level.HEIGHT
        WIDTH = level.WIDTH

        #measures allowed space between panel and full findow to find the center of a window
        allowed_x = self.WIN_WIDTH - self.panel_x
        allowed_y = self.WIN_HEIGHT - self.panel_y

        #sets a swuare size by selecting a mininum of width and height 
        self.square_size = min(((allowed_x//WIDTH), (allowed_y//HEIGHT)))
        self.square_size = (self.square_size, self.square_size)

        
        diff_x = allowed_x - (self.square_size[0] * WIDTH)
        diff_y = allowed_y - (self.square_size[1] * HEIGHT)

        #creates starting poing of a maze to be centered depending on a square side and panel
        self.start_x = self.panel_x + diff_x//2
        self.start_y = self.panel_y + diff_y//2

        #created ending poing depending on square sise and dimensions of a screen
        self.end_x = self.square_size[0]*WIDTH + self.start_x
        self.end_y = self.square_size[1]*HEIGHT + self.start_y

        #displayes grid generated
        self.draw_grid(level)
    #procedure that displays grid on the window
    def draw_grid(self, level):
        #assigns colours colours in a dictionary that can be fetched easily
        colours = { 'wall': (Black),
                    'empty': (White),
                    'start': (Green),
                    'end': (Red),
                    'user': (Yellow),
                    'solved': (Cyan)
                    
        }

        #goes through one by one in a grid and updates the color of each square
        for row in range(level.HEIGHT):
            for col in range(level.WIDTH):
                cell = self.grid[row][col]

                if cell == '1': # wall
                    colour = colours['wall']
                elif cell == '0': #empty
                    colour = colours['empty']
                    
                if (row,col) == (level.start):
                    self.grid[row][col] = '2' #start number
                    colour = colours['start']
                    self.start_pos = (row, col)
                elif (row,col) == (level.end):
                    self.grid[row][col] = '3' #end number
                    self.end_pos = (row, col)
                    colour = colours['end']
                
                if cell == '4': #solved number
                    colour = colours['solved']

                if (row, col) == (self.node.node_pos):
                    colour = colours['user']

                #fills a square with set size above and fill it with a colour selected in if statements above
                pygame.draw.rect(self.WIN, colour, (self.square_size[0] * col + self.start_x, self.square_size[1] * row + self.start_y, self.square_size[0], self.square_size[1]))
        #draws vertical and horiozontal lines to separate grid
        for row in range(level.HEIGHT+1):
            pygame.draw.line(self.WIN, (Grey), (self.start_x, self.square_size[1] * row + self.start_y), (self.end_x, self.square_size[1] * row + self.start_y))

        for col in range(level.WIDTH+1):
            pygame.draw.line(self.WIN, (Grey), (self.start_x + self.square_size[0] *col, self.start_y), (self.start_x + self.square_size[0] *col, self.end_y))

        # self.display()


    #procedure to display window and draw it 
    def Draw(self):
        self.WIN.fill(White)
        pygame.draw.line(self.WIN, Red, (self.panel_x, 0), (self.panel_x, self.WIN_HEIGHT))
        self.display()
    
        
#class for In-built levels
class Levels(AllLevels):
    panel_x = 100     
        
    def on(self):
        #fetches levels and IDs from database
        self.fetch_levels(inbuilt=True)
        self.fetch_ID()
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, (Black), (Grey), (White), command= 'return', margin = 10)
        self.Levels = Font.render('Levels', True, Black)
        self.buttons = [returnbtn]

        #adds level buttons to the screen and draws it
        self.add_buttons()
        self.draw()

        run = True
        while run:
            self.draw_writings()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    self.display()
                    
                    
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.active:
                                    if btn.command:
                                        if btn.command == 'return':
                                            return True
                                        else:
                                            resume = btn.command()
                                            if resume != False:
                                                if resume == None:
                                                    continue
                                                self.draw()
                                                # self.draw_grid()
                                            else:
                                                run = False
                                                break
                                    else:
                                        # if button is clicked that does't have a functon assigned, its a tile 
                                        # meaning that it has level contained 
                                        # fetches ID from the button and builds a level based on the ID
                                        ID = btn.Text
                                        resume = self.build_level(int(ID), True)
                                        if resume != False:
                                            if resume == None:
                                                continue
                                            self.draw()
                                        else:
                                            run = False
                                            break
 
                    else:
                        btn.default(self.WIN)  

        return False

    #function to fetch all solved levels from table UserMaze where Inbuilt is True
    def get_solved(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()

        c.execute(f"""SELECT Maze.MazeID
                          FROM Maze
                          LEFT JOIN UserMaze
                          ON Maze.MazeID = UserMaze.MazeID
                          Where UserMaze.Username = '{USERNAME}' AND Maze.Inbuilt = '{int(True)}'
                """)

        
        row = c.fetchall()
        self.solved_IDs = []
        
        for r in row:
            self.solved_IDs.append(int(r[0])) #adds one which were previously solved
        
        if len(self.solved_IDs) != 0:
            max_id = max(self.solved_IDs)+1 #to add next level
            self.solved_IDs.append(max_id)
            self.solved_IDs = list(set(self.solved_IDs)) #get rid of duplicates as user can solve 1 maze several times
        else:
            self.solved_IDs.append(1)

    #procedure to insert level solved into table UserMaze
    def insert_level_solved(self, ID):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute(f"""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            (str(ID), USERNAME))

        conn.commit()
    
    #procedure to insert level solved into table UserMaze and ublocks next level 
    def get_next_level(self):
        max_val = max(self.solved_IDs)
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute(f"""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            (str(max_val), USERNAME))

        conn.commit()
        self.add_buttons()

    ######### display and refresh
    def draw_writings(self):
        self.WIN.blit(self.Levels, (self.WIN_WIDTH//2- self.Levels.get_width()//2, 50))
        
    def draw(self):
        self.WIN.fill(White)
        self.display()


#class for user-made levels
class Workshop(AllLevels):
    panel_x = 100   
        
    def on(self):
        #fetches all man-made levels 
        self.fetch_levels(inbuilt=False)
        self.fetch_ID()
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, (Black), (Grey), (White), command= 'return', margin = 10)
        self.Levels = Font.render('Worshop', True, Black)
        self.buttons = [returnbtn]

        self.add_buttons(inbuilt=False)
        self.draw()

        run = True
        while run:
            self.draw_writings()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    self.display()
                    
                    
                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.active:
                                    if btn.command:
                                        if btn.command == 'return':
                                            return True
                                        else:
                                            resume = btn.command()
                                            if resume != False:
                                                if resume == None:
                                                    continue
                                                self.draw()
                                                # self.draw_grid()
                                            else:
                                                run = False
                                                break
                                    else:
                                        #builds level based on the ID fetched when the tile was clicked
                                        ID = btn.ID
                                        resume = self.build_level(int(ID), False)
                                        if resume != False:
                                            if resume == None:
                                                continue
                                            self.draw()
                                        else:
                                            run = False
                                            break
 
                    else:
                        btn.default(self.WIN)  

        return False        

    #get the names of users who uploaded the maze
    def get_names(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(f"""
            SELECT Username
            FROM Uploaded""")

        row = c.fetchall()
        names = []
        for ID in row:
            names.append(ID[0])
            
        return names
    #Fetches ID from Uploaded and inserts into UserMaze table 
    def insert_level_solved(self, ID):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()

        curr.execute(f"""SELECT MazeID FROM Uploaded WHERE UploadedID == '{ID}' """)
        ID = curr.fetchone()[0]
        
        curr.execute(f"""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            (str(ID), USERNAME))

        conn.commit()
    #######method to draw and display ##########
    def draw_writings(self):
        self.WIN.blit(self.Levels, (self.WIN_WIDTH//2- self.Levels.get_width()//2, 50))
        
    def draw(self):
        self.WIN.fill(White)
        self.display()

#class sandbox to generate random maze, upload it and solve it
class Sandbox(Window):
    panel_x = 200
    panel_y = 0
    moving = False
    editing = False
    deleting = False
    
    #getter methods
    def get_width(self):
        return self.__width_text

    def get_height(self):
        return self.__height_text

    
    def on(self):
        
        self.__width_text = SubFont.render('Width', True, Black)
        self.__height_text = SubFont.render('Height', True, Black)

        #section of code to create all buttons needed for running and make sandbox functioning
        returnbtn = Button(10, self.WIN_HEIGHT-80, 'Return', SubFont, Black, Grey, White, command = 'return', margin = 10)
        btn_empty = Button(110, self.WIN_HEIGHT-80, 'Empty', SubFont, (Black), (Grey), (White), command= lambda: self.generate(algorithm='empty'), margin = 10)
        btn_generate = Button(50, 80, 'Generate', SubFont, (Black), (Grey), (White), command = lambda: self.generate(), margin = 10 )
        btn_start = Button(50, 500, 'Start Solving', SubFont, (Black), (Grey), (White), command= lambda: self.start_solving_wrapper(), margin = 10)
        btn_upload = Button(50, 550, 'Upload', SubFont, (Black), (Grey), (White), command= lambda: self.upload_wrapper(), margin = 10)
        btn_braid = Button(50, 400, 'Braid', SubFont, (Black), (Grey), (White), command= lambda: self.braid(), margin = 10)

        self.width_input = Utils.InputBox(50, 180, 80, 30, validate=lambda x: Utils.check_numbers(x))
        self.height_input = Utils.InputBox(50, 250, 80, 30, validate=lambda x: Utils.check_numbers(x))

        self.buttons = [returnbtn, btn_generate, btn_empty, btn_start, btn_upload, btn_braid]
        self.input_boxes = [self.width_input, self.height_input]

        #sets clock for consistent solving time not dependent on GPU power
        clock = pygame.time.Clock()

        self.draw()
        run = True
        while run:

            self.display()
            clock.tick(self.FPS)
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # pygame.quit()
                    run = False
                    break

                pos = pygame.mouse.get_pos()
                
                self.draw()
                self.draw_inputs()

                try:
                    self.draw_grid()
                except:
                    pass
                #exception handling and displaying messages
                try:
                    if resume == 'boundary':
                        self.blit_boundary()
                    if resume == 'exists':
                        self.blit_exists()
                    if resume == True or resume == 'DN':
                        self.blit_success()
                    if resume == 'no path':
                        self.blit_no_path()
                        self.clicked = False
                    
                except:
                    pass
                
                    
                for box in self.input_boxes:
                    box.handle_event(event)

                for btn in self.buttons:

                    if btn.is_over(pos):
                        btn.hover(self.WIN)
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                if btn.command:
                                    if btn.command == 'return':
                                        return True
                                    else:
                                        resume = btn.command()
                                        if resume != False:
                                            if resume == None:
                                                continue
                                            if resume == True:
                                                self.display()
                                                
                                        else:
                                            run = False
                                            break

                
                        
                    else:
                        btn.default(self.WIN)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    try:
                        pos = self.get_pos_on_grid(pos) #to react on grid only
                    except:
                        pos = None

                    #left click allows to set walls on the grid and resets resume to make text disappear 
                    # and mode start and end nodes on the grid
                    if pos:
                        if pygame.mouse.get_pressed()[0]:
                            if pos: 
                                self.clicked = True
                                resume = 'dn'
                                row, column = pos

                                cell = self.grid[row][column]
                                #first checks for start/end and if cell is either, skipps next elif starement
                                if cell.is_start or cell.is_end:
                                    self.moving = True

                                elif cell.is_wall or cell.is_empty:
                                    self.editing = True

                        #right click allows to destoy walls 
                        elif pygame.mouse.get_pressed()[2]:
                            #if mouse click is right click, edting and moving set to false to disallow easing and creating walls at the same time
                            self.clicked = True
                            self.editing = False
                            self.moving = False
                            resume = 'dn'
                            if pos:
                                #if position is valid e.g. not None, 
                                #checks for boundary values and allows deleting when cells aren't on a border
                                row, column = pos
                                cell = self.grid[row][column]
                                if row != 0 and row != self.HEIGHT-1 and column != 0 and column != self.WIDTH-1:
                                    if not cell.is_start and not cell.is_end:
                                        self.deleting = True
                        
                        else:
                            self.editing = False
                            self.deleting = False
                            self.moving = False




                #resets editing and deleting and moving as soon as mouse button is up
                if event.type == pygame.MOUSEBUTTONUP:
                    self.editing = False
                    self.deleting = False
                    self.moving = False


                #if either of moving, deleting or editing are active, mouse position if fetched and casted onto grid position

                if self.moving or self.deleting or self.editing:
                    pos = pygame.mouse.get_pos()
                    position = self.get_pos_on_grid(pos)



                    if position:
                        row, column = position
                        #calls move_cell method in Grid to move start/end
                        if self.moving:
                            self.Grid.move_cells(cell, (row, column))
                        #if node is not in the border, allows to erase walls, as boundaries are compulsory
                        if row != 0 and row != self.HEIGHT-1 and column != 0 and column != self.WIDTH-1:

                            if self.editing:
                                cell = self.grid[row][column]
                                if not cell.is_start or not cell.is_end:
                                    self.grid[row][column].is_wall = True
                                    self.grid[row][column].is_empty = False

                            if self.deleting:
                                cell = self.grid[row][column]
                                if cell.is_wall or cell.is_empty:
                                    self.grid[row][column].is_wall = False
                                    self.grid[row][column].is_empty = True


                    self.draw_grid()
            

        return False 

    #gets position on the grid, as grid is not on the whole screen returs result only when mouse position
    # inbetween start and end 
    def get_pos_on_grid(self, pos):
        x,y = pos
        
        if self.start_y < y < self.end_y and self.start_x < x < self.end_x:
            Y = y - self.start_y 
            X = x - self.start_x 
            result = (Y//self.square_size[1], X //self.square_size[0])
            return result

        return None
    #wrapper to solve the maze
    def start_solving_wrapper(self):
        return self.solve()
    #wrapper to upload a maze
    def upload_wrapper(self):
        return self.upload()
        
    ########### displaying texts ########
    def blit_exists(self):
        text = Font.render("Maze already exists", True, Red)
        self.WIN.blit(text, (500, 500))

    def blit_success(self):
        text = Font.render("Great Success!!!", True, Red)
        self.WIN.blit(text, (500, 500))

    def blit_no_path(self):
        text = Font.render("No path found", True, Red)
        self.WIN.blit(text, (500, 500))

    
    #funciton to uploads the maze
    def upload(self):
        #exception handling to prevent error when no grid on the screnn
        try:
            binary, HEIGHT, WIDTH, start, end = self.Grid.export()
        except:
            return
        #convers binary into base 128 as takes less space
        Base128 = Utils.Binary128().encode(binary)

        resume = self.solve()
        if resume == 'no path':
            return 'no path'
        if resume == False:
            return False

        conn = sql.connect('DataBase.db') 
        c = conn.cursor()

        #selects ID from Maze to check if its unique.
        # 2 same mazes cannot exist 
        c.execute("""
            SELECT MazeID
            FROM Maze
            Where Base128 = ?           
            """, [Base128])
        row = c.fetchall()

        if row:
            return 'exists'
        #if maze is unique, allows to insert into Maze making new level
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(Base128, False, WIDTH, HEIGHT, start[0], start[1], end[0], end[1]))
        conn.commit()
        
        c.execute("""
            SELECT MazeID
            FROM Maze
            Where Base128 = ?           
            """, [Base128])

        MazeID = c.fetchone()[0]
        #inserts Username and MazeID to connect the creator of the maze to a maze itself
        c.execute("""INSERT INTO Uploaded (MazeID, Username) VALUES(?,?)""",
                            (MazeID, USERNAME))

        conn.commit()     
        return 'DN' 
        
        
    ########## Draw functions #########
    def draw(self):
        self.WIN.fill(White)
        self.draw_writings()
        pygame.draw.line(self.WIN, Red, (self.panel_x, 0), (self.panel_x, self.WIN_HEIGHT))

    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw(self.WIN, btn.button_colour)


    def draw_inputs(self):
        for box in self.input_boxes:
            box.update()
            box.draw(self.WIN)


    def draw_writings(self):
        self.WIN.blit(self.get_width(), (50, 145) )
        self.WIN.blit(self.get_height(), (50, 215) )


    #procedure that generates maze by using algorithms provided in Generate file
    def generate(self, algorithm = None):

        if self.width_input.text:
            self.width = int(self.width_input.text)
        else:
            return

        if self.height_input.text:
            self.height = int(self.height_input.text)
        else:
            return
        
        #cheks if width and height in allowed parametersm othersise generating maze can take too much time
        if self.width > 40 or self.width < 5:
            return 'boundary'
        if self.height > 40 or self.height < 5:
            return 'boundary'
        

        grid = MakeGrid.Grid()
        algo = ['backtracker', 'binarytree', 'sidewinder', 'cellular', 'pims']

        #selects algorithm by random and sets generator of a grid to be called
        if not algorithm:
            algorithm = choice(algo)

        if algorithm.lower() == 'backtracker':
            grid.generator = Generate.BackTracker(self.width, self.height)

        elif algorithm.lower() == 'binarytree':
            grid.generator = Generate.BinaryTree(self.width, self.height)
        
        elif algorithm.lower() == 'sidewinder':
            grid.generator = Generate.Sidewinder(self.width, self.height)
        
        elif algorithm.lower() == 'cellular':
            grid.generator = Generate.CellularAutomaton(self.width, self.height)
        
        elif algorithm.lower() == 'pims':
            grid.generator = Generate.Pims(self.width, self.height)
        
        elif algorithm.lower() == 'empty':
            grid.generator = Generate.EmptyGrid(self.width, self.height, clear = True)

        start = end = None
        #exception handling used to track position of start/end node, as fist time they don't exist
        try:
            start = self.Grid.get_node_pos('start')
            end = self.Grid.get_node_pos('end')
            grid.generate(start)
            grid.generate_entrance(start, end)

        except:
            grid.generate()
            grid.generate_entrance()

        self.Grid = grid
        self.grid = grid.grid

        self.HEIGHT = len(self.grid)
        self.WIDTH = len(self.grid[0])

        #centers the window and sets square size same to fit on the screen
        allowed_x = self.WIN_WIDTH-self.panel_x
        allowed_y = self.WIN_HEIGHT-self.panel_y
        
        #making length and width the same
        self.square_size = min(((allowed_x//self.WIDTH), (allowed_y//self.HEIGHT)))
        self.square_size = (self.square_size, self.square_size)
        
        
        diff_x = allowed_x - (self.square_size[0] * self.WIDTH)
        diff_y = allowed_y - (self.square_size[1] * self.HEIGHT)

        self.start_x = self.panel_x + diff_x //2
        self.start_y = self.panel_y + diff_y //2

        self.end_x = self.square_size[0]*self.WIDTH + self.start_x
        self.end_y = self.square_size[1]*self.HEIGHT + self.start_y
        
    def draw_grid(self):
        #assigns colours colours in a dictionary that can be fetched easily

        colours = { 'wall': (Black),
                    'empty': (White),
                    'start': (Green),
                    'end': (Red),
                    'child': (LightBlue),
                    'parent': (Blue),
                    'solved':(Purple),
        }
        try:
            self.grid = self.Grid.grid
        except:
            return 

        #goes through one by one in a grid and updates the color of each square
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                cell = self.grid[row][col]

                if cell.is_start:
                    colour = colours['start']
                elif cell.is_end:
                    colour = colours['end']
                elif cell.is_wall:
                    colour = colours['wall']
                elif cell.is_solved:
                    colour = colours['solved']
                elif cell.is_parent:
                    colour = colours['parent']
                elif cell.is_child:
                    colour = colours['child']

                elif cell.is_empty:
                    colour = colours['empty']
                #fills a rectangle at a set coordinates with a colour specifies above
                pygame.draw.rect(self.WIN, colour, (self.square_size[0] * col + self.start_x, self.square_size[1] * row + self.start_y, self.square_size[0], self.square_size[1]))
        
        #draws vertical and horiozontal lines to separate grid
        for row in range(self.HEIGHT+1):
            pygame.draw.line(self.WIN, Grey, (self.start_x, self.square_size[1] * row + self.start_y), (self.end_x, self.square_size[1] * row + self.start_y))

        for col in range(self.WIDTH+1):
            pygame.draw.line(self.WIN, Grey, (self.start_x + self.square_size[0] *col, self.start_y), (self.start_x + self.square_size[0] *col, self.end_y))

    #funciton to braid e.g. delete walls if dead end found
    #BUG: only deletes of initial grid, not man-made
    def braid(self, p = 1):
        try:
            self.Grid.braid(probability = p)
            self.draw_grid()
        except:
            pass

    # displays text 
    def blit_boundary(self):
        text = SubFont.render("Width and Height should be inbetween 5 and 40", True, Red)
        self.WIN.blit(text, (200, 500))

    #functon to solve the maze
    def solve(self):
        try:
            self.start_node = Node(self.Grid.get_node_pos('start'), None)
            self.end_node = Node(self.Grid.get_node_pos('end'), None)

            self.clear_grid()
            resume = self.solve_on()
            return resume
        except:
            pass
    
    #sets value of each node to False to erase clild, parent and solved colours
    def clear_grid(self):
         for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                node = self.Grid.grid[row][col]
                node.is_child = False
                node.is_parent = False
                node.is_solved = False
    #Practically a Breadth First search, same as Dijkstra's without weight
    def solve_on(self):
        #open list for found
        open_list = [self.start_node]
        closed_list = []

        solve = True

        while solve:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    solve = False
                    return False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.editing = False
                    self.deleting = False
                    self.moving = False

            #if no more discovered and end is not found, path does't exist
            if not open_list:
                solve = False
                return 'no path'

            open_list = Utils.MergeSort(open_list) # sorted from smallest to largest of gCost
            current_index = 0
            #appends new node to discovered
            current_node = open_list[current_index]
            current_node.calc_fCost(self.end_node)
            if current_node.pos == self.end_node.pos:
                solve = False
                break
            #appends children to the list
            children = self.get_children(current_node)
            open_list.pop(current_index)
            closed_list.append(current_node)

            #goes through each child and checks if they are in discovered already
            for child in children:
                index1 = self.check_list(open_list, child)
                index2 = self.check_list(closed_list, child)
                #if in discovered, gCost if re-calculated as could be less
                if index1:
                    if open_list[index1].gCost > child.gCost:
                        open_list.pop(index1)
                        open_list.append(child)
                #if node is in parents, poping out of it and adds to children again
                if index1 and index2:
                    if closed_list[index2].gCost > child.gCost:
                        closed_list.pop(index2)
                        open_list.append(child)

                if not index1 and not index2:
                    open_list.append(child)

            self.display_found(open_list, closed_list)

        self.display_root(current_node)
        self.display()

        return True


    def display_found(self, open_list, closed_list):
        #goes through each child and updates each node as in sets is_child to True to be displayed
        for node in open_list:
            row, column = node.pos
            if not self.Grid.grid[row][column].is_start or not self.Grid.grid[row][column].is_end:
                self.Grid.grid[row][column].is_child = True
        
        #goes through each parent and updates each node as in sets is_parent to True to be displayed
        for node in closed_list:
            row, column = node.pos
            if not self.Grid.grid[row][column].is_start or not self.Grid.grid[row][column].is_end:
                self.Grid.grid[row][column].is_parent = True

        self.draw_grid()
        self.draw_buttons()
        self.display()
    
    #functon to returns children around node passed as a parameter
    def get_children(self, node):
        row, column = node.pos
        children = []
        for y,x in [(1,0), (0,1), (0,-1), (-1,0)]:
            #exception handling as could access array's index out on range
            try:
                #checks if row+y and column+x within the boundaries
                if  0 < row+y < self.Grid.HEIGHT and 0 < column+x < self.Grid.WIDTH:
                    cell = self.Grid.grid[row+y][column+x]
                    #checks if position = end node's position
                    if (row+y, column+x) == self.end_node.pos:
                        cell = Node((row+y, column+x), node)
                        cell.calc_fCost(self.end_node)
                        children.append(cell)

                    #if cell is empty, adds to children
                    if cell.is_empty:
                        cell = Node((row+y, column+x), node)
                        cell.calc_fCost(self.end_node)

                        children.append(cell)
            except:
                pass

        return children
    #checks if object in a list, efficient as uses O(1) instead of linear search
    def check_list(self, list, object):
        try:
            return list.index(object)
        except:
            return None
            
    #displayes the shortest root found
    def display_root(self, current_node):
        length = 0
        #unconditional loop that stops only at start node
        while current_node is not None:
            y, x  = current_node.pos
            if (y,x) != self.start_node.pos:
                self.Grid.grid[y][x].is_solved = True
                
            length += current_node.length
            current_node = current_node.parent

        self.draw_grid()
        
#function to check valitity of a database and auto-populating tables of it
def run_check():
    try:
        conn = sql.connect('DataBase.db')
        curr = conn.cursor()
        # checks for table Users existance
        curr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name= 'User'""")
        if not curr.fetchone():
            CreateDB.BuildTables().create_users()
        # checks for table Maze existance
        curr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name= 'Maze'""")
        if not curr.fetchone():
            CreateDB.BuildTables().create_maze()
        # checks if number of records in table Maze is less than 15
        curr.execute("""SELECT MazeID FROM Maze""")
        if len(curr.fetchall()) < 15:
            CreateDB.BuildTables().restore_mazes()
        # checks if table UserMaze exists
        curr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name= 'UserMaze' """)
        if not curr.fetchone():
            CreateDB.BuildTables().build_maze_user()

        # checks if table Uploaded exists
        curr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name= 'Uploaded'""")
        if not curr.fetchone():
            CreateDB.BuildTables().build_uploaded()

    except:
        print('error occured while creating a database')


if __name__ == '__main__': 
    run_check()       
    c = LoginPage() 
    c.on()
    pygame.quit()

