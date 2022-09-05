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
                                Values(?,?,?,?,?,?,?,?)''',(r"""Gbb_чжa/Fъ@%k£щс(/G6а4Ifnэщbi%ям>uQ<#6I/jQазIuxА@!aie""", True, 21, 21, 1, 0, 19, 20))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(r"""ieHнщгO/xъц/QdаUеvi7'пOaf7чqc:щмьbiBБ-iulRвцQbxUюea@БU!faнщSG^ad""", True, 21, 25, 1, 0, 23, 20))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aabQ'Hc"F6}qOw'6£%k6БOGqLъ'uk''м>qIlчнGub-'дceDQцaGae""", True, 21, 21, 1, 0, 19, 20))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""iuGo'RтvQ!яQ#uI^f_вTOeiQБ_мqicярюbkr3эаLa%HVщ_ieOвям>aQuщмяfi>LнчыIrcнчА£^G?аQц:I/v_'зGfjрБ-aqaac""", True, 25, 31, 1, 0, 29, 24))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""I/kk'6фvc!ч6вac!hАаOarOнчR¬"Is#Uц"aeFVягG"dм#6i>c`#ъ>eifяQяaIqnрч5cqGQ'н¬!kcаъю"a"D_вHGaRVБмaaaac""", True, 25, 31, 1, 0, 29, 24))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aaakчс{/kaчVчrQbLъ'лc'k-яр£bG@'-юvOb9-ягG>l7БмcaI<в_фqG!ч7яfO!TАакGuI6щмк^c&БАюbaqvъщзc/bря6IbOcc""", True, 25, 31, 1,0,29,24))
        
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""avabadчVярщbQbIuPэ#эв-кbGeGa"эяряжiaieQGщVвI{bQ>kqFQ'ъу5k^G>k('рарц^Ofa>SRвUчэc"kvG*}k'рч%a'GfPс*7чм(eabO:яьak#GO!a'cъцaDR>"Gbk/3lцpаыi"Gaio^6БoцuQui/N-щ-чрaaabcae""", True, 41, 31, 1,0,29,40))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""ieHмчгi/xмцqQc'Qеva7'кOafRчqcqщQ~biBБ-ielQвKIavUцeawяU!faнчOGbad""",True, 21, 25, 1, 0, 23, 20))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""kebR#Hi/Dм}uG&#ъ£!kRвлIqfмв/I!чмт/IkчэIeHн'HI'vQ:/c£вэ(!iUБлaaad""", True, 21, 25, 1, 0, 23, 20))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""k!GbvR#ъ(%QfNА'6>!O/lUчмц"G"i-#счeOekk#АчжQqItчRщкkrceчБаUk!G>vR#рк:cbfмБ6?ba"jБя7}qc%Iнч7'acaiac""", True, 31, 25, 1, 0, 23, 30))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""Qfivvъам£faufрвр?bauRАаАА>ceIUв_аaG%G{щБ#зGracчАвыQ"auщ7щ7Q"c/vVя-!rk^TнаU?>Ifbрщ-бecqkсараaiaGac""", True, 31, 25, 1, 0, 23, 30))
        
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''',(r"""cqa%It#-чрщqceaaHQчV#рмqIbabв6щн#GGeGaaмБQ'р>ac%Gv16'UяOi/iqIA'на6:qG>G:nмчQ'6aqa!Gae""",True, 41, 17, 1, 0, 15, 40))

        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""aaiaadвэаБщra"ObPэщъуъ!rariv"рщOБ0cfI!aU#мxрф/G/cvv7аэвлGba:a`БнаJц%c"krNсщрарaacqGae""", True, 41, 17, 1, 0, 15, 40))
    
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""c'I^Ix'R#RаbkuI"Rра7#м('QrO%чQамщLc/GvcV'няV?fi/GrFUчнякG'GbcBчRБс}/O:Q>Lмч6'ъc:c"G#'_#нчbkbi>lрврчА£rG>i^анчАщKGrcbi7ясвртrO>Oa9мчъБыG%i:i`щ-ч-ц!iri>hАярчАOqk%QcяА#6вvG!kbbRщАвс!rcbO^ясвмщLO>irkQчАяр>eiri'_-ярчOaaaaaac""", True, 41, 41, 1, 0, 39, 40))
       
        c.execute('''INSERT INTO Maze (Base128, InBuilt, Width, Height, StartX, StartY, endX, EndY)
                                Values(?,?,?,?,?,?,?,?)''', (r"""Gqcracщ_'Rщ^cfIrHсяRяQ!ak%I^ББ#нщгafa^O_БVБQ~ek>I%FUч6щ5k%k:kk'с'U@vG"krpRяэаАkri%Gsвн#7щuc/aqHБ'БщАгeIbIqвэ#н'жGvi%O6яUвА?uI%G^xRчъчлc!G%O.щБщр}ra%IvnVчUаVkrO%IdамяэщrG%i>jнщнчА£!c%G^#БвVчзafk!OUБQ'Б?uk'O"Dр'Q'ьa"i"iac""", True, 41, 41, 1, 0, 39, 40))
        
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
        

