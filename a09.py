##
## ==============================================
##   Keqi Wu (20775633)
##   CS 116 Winter 2019
##   Assignment 09
## ==============================================
##

import check

class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key= None
        self.message= ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        returns nothing and prints the name of the noun and description if
        noun satisfies the following condition.Oherwise, prints an error message

        Effects: print name of noun and description on the screen,otherwise
        prints error message
        
        look: World Str -> None
        '''
        find_inv=list(map(lambda s: s.name,self.player.inventory))
        find_cont=list(map(lambda k: k.name,self.player.location.contents))
        if noun=="me":
            self.player.look()
        elif noun=="here":
            self.player.location.look()
        elif noun in find_inv:
            self.player.inventory[find_inv.index(noun)].look()
        elif noun in find_cont:
            self.player.location.contents[find_cont.index(noun)].look()
        else:
            print(self.msg_look_fail)
            
    def inventory(self):
        '''
        returns None and print out inventories that the player carries. If
        there is no inventory, print error message

        Effect: prints some inventories on the screen
        
        inventory: World -> None
        '''
        if len(self.player.inventory) != 0:
            print('Inventory: {0}'.\
                  format(', '.join(map(lambda x: x.name,self.player.inventory))))
        else:
            print(self.msg_no_inventory)
            
    def take(self, noun):
        '''
        returns nothing and prints 'taken' if the item(noun) exists in the room. The
        inventory is added to player's inventory. Otherwise, print the error message

        Effects: mutate player's inventory list
                 mutate player's location contents list
                 print "taken" or error message on the screen

        take: World Str -> None
        '''
        item_list=list(map(lambda s: s.name,self.player.location.contents))
        if noun!='' and noun in item_list:
            self.player.inventory.append(self.player.location.\
                                         contents[item_list.index(noun)])
            self.player.location.contents.remove(\
                self.player.location.contents[item_list.index(noun)])
            print(self.msg_take_succ)
        else:
            print(self.msg_take_fail)
            
    def drop(self, noun):
        '''
        returns nothing and prints out 'dropped' if the item(noun) exists in player's
        inventory, otherwise prints error message

        Effects: mutate player's inventory list
                 mutate player's locaiton contents list
                 print "dropped" or error message on scree
        '''
        item_list=list(map(lambda s: s.name,self.player.inventory))
        if noun!='' and noun in item_list:
            self.player.location.contents.append(self.player.\
                                                 inventory[item_list.index(noun)])
            self.player.inventory.remove(\
                self.player.inventory[item_list.index(noun)])
            print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)
        
    def go(self, noun):
        '''
        returns nothing. It mutates player's location if exit(noun) exists
        in player's current location and the exit does not requires a key or key
        exists in player's inventory. Otherwise, print exit's message. If
        the exit does not exist in player's current location, print
        error message

        Effects: mutate player's location
                 print exit's message or error message on screen
        '''
        exit_list=list(map(lambda s: s.name,self.player.location.exits))
        if noun in exit_list and noun!='':
            exits=self.player.location.exits
            if exits[exit_list.index(noun)].key==None or\
               exits[exit_list.index(noun)].key in self.player.inventory:
                self.player.location=exits[exit_list.index(noun)].destination
                print(self.player.location.name)
                print(self.player.location.description)
                if len(self.player.location.contents) != 0:
                    print('Contents: {0}.'.format(\
                        ', '.join(map(lambda x: x.name, self.player.location.contents))))
                if len(self.player.location.exits) != 0:
                    print('Exits: {0}.'.format(\
                        ', '.join(map(lambda x: x.name, self.player.location.exits))))
            else:
                print(exits[exit_list.index(noun)].message)
        else:
            print(self.msg_go_fail)
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        '''
        opens a file called fname and change all the data in world into
        given format and write into that file

        Effect: write in a file
        
        save: World Str -> None
        '''
        exit_list=[]
        out=open(fname,'w')
        if self.player.inventory!=[]:
            for a in self.player.inventory:
                out.write('thing #{0} {1}\n{2}'.format(a.id,a.name,a.description))
        for b in self.rooms:
            if b.contents!=[]:
                for c in b.contents:
                    out.write('thing #{0} {1}\n{2}'.format(c.id,c.name,c.description))
        for d in self.rooms:
            out.write('room #{0} {1}\n{2}'.\
                      format(d.id,d.name,d.description))
            out.write('contents')
            if d.contents!=[]:
                for e in d.contents:
                    out.write(' #'+str(e.id))
            out.write('\n')
        out.write('player #{0} {1}\n{2}'.\
                  format(self.player.id,self.player.name,self.player.description))
        out.write('inventory')
        for f in self.player.inventory:
            out.write(' #'+str(f.id))
        out.write('\n'+'location #'+str(self.player.location.id))
        if False in list(map(lambda s: s.exits==[],self.rooms)):
            out.write('\n')
        for g in self.rooms:
            for h in g.exits:
                if h.key==None:
                    exit_list.append(('exit #{0} #{1} {2}'.format(g.id,h.destination.id,h.name)))
                else:
                    exit_list.append(('keyexit #{0} #{1} {2}'.format(g.id,h.destination.id,h.name)))
                    exit_list.append(('#{0} {1}'.format(h.key.id,h.message)))
        out.write('\n'.join(exit_list))
        out.write('\n')
        out.close()

## Q2
def load(fname):
    '''
    open a file called fname and read all lines in the file. Transfer all data
    into World and make it playable

    Effect: Read from a file

    load: Str -> World
    '''
    file=open(fname,'r')
    text=file.readline()
    objects={}
    rooms={}
    settings=[]
    while len(text)!=0:
        if text.startswith('thing'):
            s=text.split()
            athing=Thing(int(s[1].strip('#')))
            athing.id=int(s[1].strip('#'))
            athing.name=' '.join(s[2:])+' '*(text.count(' ')-len(s)+1)
            t=file.readline()
            athing.description=t
            objects[athing.id]=athing
        elif text.startswith('room'):
            s=text.split()
            aroom=Room(int(s[1].strip('#')))
            aroom.id=int(s[1].strip('#'))
            aroom.name=' '.join(s[2:])+' '*(text.count(' ')-len(s)+1)
            t=file.readline()
            aroom.description=t
            u=file.readline()
            if u.strip('contents')=='\n':
                aroom.contents=[]
            else:
                list_num=u.strip('contents').split()
                aroom.contents=[]
                for i in list_num:
                    aroom.contents.append(objects[int(i.strip('#'))])
            rooms[aroom.id]=aroom
            settings.append(aroom)
        elif text.startswith('player'):
            s=text.split()
            aplay=Player(int(s[1].strip('#')))
            aplay.id=int(s[1].strip('#'))
            aplay.name=' '.join(s[2:])+' '*(text.count(' ')-len(s)+1)
            t=file.readline()
            aplay.description=t
            u=file.readline()
            if u.strip('inventory')=='\n':
                aplay.inventory=[]
            else:
                list_num=u.strip('inventory').split()
                aplay.inventory=[]
                for i in list_num:
                    aplay.inventory.append(objects[int(i.strip('#'))])
            v=file.readline()
            aplay.location=rooms[int((v.split())[1].strip('#'))]
        elif text.startswith('exit'):
            s=text.split()
            aexit=Exit(' '.join(s[3:]),rooms[int(s[2].strip('#'))])
            aexit.name=' '.join(s[3:])+' '*(text.count(' ')-len(s)+1)
            aexit.destination=rooms[int(s[2].strip('#'))]
            rooms[int(s[1].strip('#'))].exits.append(aexit)
        elif text.startswith('keyexit'):
            s=text.split()
            kexit=Exit(' '.join(s[3:]),rooms[int(s[2].strip('#'))])
            kexit.name=' '.join(s[3:])+' '*(text.count(' ')-len(s)+1)
            kexit.destination=rooms[int(s[2].strip('#'))]
            t=file.readline()
            kexit.key=objects[int((t.split()[0]).strip('#'))]
            kexit.message=' '.join((t.split())[1:])
            rooms[int(s[1].strip('#'))].exits.append(kexit)
        text=file.readline()
    file.close()
    game=World(settings,aplay)
    game.rooms=settings
    game.player=aplay
    return game
            

def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)
