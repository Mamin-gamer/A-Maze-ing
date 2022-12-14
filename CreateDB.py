import sqlite3 as sql
#class that contains all methods to create and auto-populate tables
#some methods are not used, but were used for testing purposes
class BuildTables:
    #main method to auto-build all tables from scratch in case database isn't created
    def build(self):
        self.create_users()
        self.create_maze()
        self.build_maze_user()
        self.build_uploaded()
        self.auto_populate_users()
        
    #method to create table User if it doesn't exist, otherwise passes
    def create_users(self):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute( """  CREATE TABLE IF NOT EXISTS User 
                            (Username Text PRIMARY KEY,
                            FirstName Text NOT NULL,
                            Surname Text NOT NULL,
                            Password Text NOT NULL)
                    """)

        conn.commit()

    #method to create talbe Maze if it does't exist, otherwise passes
    def create_maze(self):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute( """  CREATE TABLE IF NOT EXISTS Maze 
                            (MazeID Integer PRIMARY KEY AUTOINCREMENT,
                            Base128 Text NOT NULL,
                            Inbuilt Bool NOT NULL,
                            Width Integer NOT NULL,
                            Height Integer NOT NULL,
                            StartX Integer NOT NULL,
                            StartY Integer NOT NULL,
                            EndX Integer NOT NULL,
                            EndY Integer NOT NULL)
                            
                    """)
        conn.commit()
    

    #method to auto-populate User table, made mostly for testing purposes, as not called anywhere because can lead to massive flaw of a program security
    def auto_populate_users(self):

        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
                  
        c.execute('''INSERT INTO User (Username, FirstName, Surname, Password)
                                VALUES("Mamin_gamer", "Dmitrii", "Ponomarev", r"40bd001563085fc35165329ea1ff5c5ecbdbbeef")''') 

        c.execute('''INSERT INTO User (Username, FirstName, Surname, Password)
                                VALUES("QWer", "Dima", "Yes", r"40bd001563085fc35165329ea1ff5c5ecbdbbeef")''')

        c.execute('''INSERT INTO User (Username, FirstName, Surname, Password)
                                VALUES("test", "Dmitrii", "Sur", r"a94a8fe5ccb19ba61c4c0873d391e987982fbbd3")''') 

        conn.commit()

    #method to insert pre-generated mazes into table Maze in order to have set 15 levels for a new user to start
    def auto_populate_mazes(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(r"""Gbb_????a/F??@%k??????(/G6??4Ifn????bi%????>uQ<#6I/jQ????Iux??@!aie""", True, 21, 21, 1, 0, 19, 20))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(r"""ieH??????O/x????/Qd??U??vi7'??Oaf7??qc:??????biB??-iulR????QbxU??ea@??U!fa????SG^ad""", True, 21, 25, 1, 0, 23, 20))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aabQ'Hc"F6}qOw'6??%k6??OGqL??'uk''??>qIl????Gub-'??ceDQ??aGae""", True, 21, 21, 1, 0, 19, 20))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""iuGo'R??vQ!??Q#uI^f_??TOeiQ??_??qic??????bkr3????La%HV??_ieO??????>aQu??????fi>L??????Irc????????^G???Q??:I/v_'??Gfj????-aqaac""", True, 25, 31, 1, 0, 29, 24))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""I/kk'6??vc!??6??ac!h????OarO????R??"Is#U??"aeFV????G"d??#6i>c`#??>eif??Q??aIqn????5cqGQ'????!kc??????"a"D_??HGaRV????aaaac""", True, 25, 31, 1, 0, 29, 24))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aaak????{/ka??V??rQbL??'??c'k-??????bG@'-??vOb9-????G>l7????caI<??_??qG!??7??fO!T??????GuI6??????^c&??????baqv??????c/b????6IbOcc""", True, 25, 31, 1,0,29,24))
        
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""avabad??V??????bQbIuP??#????-??bGeGa"??????????iaieQG??V??I{bQ>kqFQ'????5k^G>k('????????^Ofa>SR??U????c"kvG*}k'????%a'GfP??*7????(eabO:????ak#GO!a'c????aDR>"Gbk/3l??p????i"Gaio^6??o??uQui/N-??-????aaabcae""", True, 41, 31, 1,0,29,40))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""ieH??????i/x????qQc'Q??va7'??OafR??qcq??Q~biB??-ielQ??KIavU??eaw??U!fa????OGbad""",True, 21, 25, 1, 0, 23, 20))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""kebR#Hi/D??}uG&#????!kR????Iqf????/I!??????/Ik????IeH??'HI'vQ:/c??????(!iU????aaad""", True, 21, 25, 1, 0, 23, 20))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""k!GbvR#??(%QfN??'6>!O/lU??????"G"i-#????eOekk#??????QqIt??R????krce??????Uk!G>vR#????:cbf????6?ba"j????7}qc%I????7'acaiac""", True, 31, 25, 1, 0, 23, 30))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""Qfivv????????fauf???????bauR????????>ceIU??_??aG%G{????#??Grac????????Q"au??7??7Q"c/vV??-!rk^T????U?>Ifb????-??ecqk????????aiaGac""", True, 31, 25, 1, 0, 23, 30))
        
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(r"""cqa%It#-??????qceaaHQ??V#????qIbab??6????#GGeGaa????Q'??>ac%Gv16'U??Oi/iqIA'????6:qG>G:n????Q'6aqa!Gae""",True, 41, 17, 1, 0, 15, 40))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aaiaad??????????ra"ObP??????????!rariv"????O??0cfI!aU#??x????/G/cvv7????????Gba:a`??????J??%c"krN??????????aacqGae""", True, 41, 17, 1, 0, 15, 40))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""c'I^Ix'R#R??bkuI"R????7#??('QrO%??Q??????Lc/GvcV'????V?fi/GrFU????????G'GbcB??R????}/O:Q>L????6'??c:c"G#'_#????bkbi>l????????????rG>i^??????????KGrcbi7??????????rO>Oa9??????????G%i:i`??-??-??!iri>h??????????Oqk%Qc????#6??vG!kbbR????????!rcbO^??????????LO>irkQ????????>eiri'_-??????Oaaaaaac""", True, 41, 41, 1, 0, 39, 40))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""Gqcrac??_'R??^cfIrH????R??Q!ak%I^????#??????afa^O_??V??Q~ek>I%FU??6??5k%k:kk'??'U@vG"krpR????????kri%Gs????#7??uc/aqH??'????????eIbIq????#??'??Gvi%O6??U?????uI%G^xR????????c!G%O.????????}ra%IvnV??U??VkrO%Id??????????rG%i>j????????????!c%G^#????V????afk!OU??Q'???uk'O"D??'Q'??a"i"iac""", True, 41, 41, 1, 0, 39, 40))
        
        conn.commit()
    
    #method to clear and reset a counter in User table
    def clear_table_users(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(""" DELETE FROM User""")
        #resets an autoincrement of users
        c.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='User';""")

        conn.commit()
    #method to clear and reset a counter in Maze table
    def clear_table_mazes(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(""" DELETE FROM Maze""")
        #resets an autoincrement of mazes
        c.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Maze';""")
        conn.commit()
    #method to combine clearing and auto-populating of users
    def restore_users(self):
        self.clear_table_users()
        self.auto_populate_users()

    #method to combine clearing and auto-populating of maze table
    def restore_mazes(self):
        self.clear_table_mazes()
        self.auto_populate_mazes()
        
    #mehtod to create joing table to allow users to play game
    def build_maze_user(self):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute( """  CREATE TABLE IF NOT EXISTS UserMaze 
                            (UserMazeID Integer PRIMARY KEY AUTOINCREMENT,
                            Username Text  NOT NULL,
                            MazeID Text NOT NULL,
                            FOREIGN KEY (Username) REFERENCES User(Username),
                            FOREIGN KEY (MazeID) REFERENCES Maze(MazeID))
                    """)

        conn.commit()


    #method to create a joint table to allow users to upload levels into the program
    def build_uploaded(self):
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()

        curr.execute("""CREATE TABLE IF NOT EXISTS Uploaded
                        (UploadedID Integer PRIMARY KEY AUTOINCREMENT,
                        Username Text NOT NULL,
                        MazeID Text NOT NULL,
                        FOREIGN KEY (Username) REFERENCES User(Username),
                        FOREIGN KEY (MazeID) REFERENCES Maze(MazeID))
                    """)
        conn.commit()


    #method to clear table Uploaded and reset the counter
    def clear_table_uploaded(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(""" DELETE FROM Uploaded""")
        #resets an autoincrement of mazes
        c.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Uploaded';""")
        conn.commit()

    #method to auto-populate table UserMaze. Used for testing purposes
    def populate_maze_user(self):  
        conn = sql.connect("DataBase.db")   #connect or create db
        curr = conn.cursor()
        curr.execute("""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            ('1', 'test'))
        
        curr.execute("""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            ('2', 'test'))

        curr.execute("""INSERT INTO UserMaze (MazeID, Username) VALUES(?,?)""",
                            ('1', 'Mamin_gamer'))
        
        conn.commit()

    #method to clear out take UserMaze. Used for debugging and tested purposes
    def clear_table_maze_user(self):
        conn = sql.connect('DataBase.db') 
        c = conn.cursor()
        c.execute(""" DELETE FROM UserMaze""")
        #resets an autoincrement of mazes
        c.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='UserMaze';""")
        conn.commit()
        

