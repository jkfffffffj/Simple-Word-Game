###=======================================================
## Yuchen Wan (20789146)
## CS 116 Winter 2019
## Assignment 09, Problem 1
##=======================================================
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
               key(Thing)
               message(Str)           
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message =''
        
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
        '''reads in a noun,returns nothing and prints out the name and the description
        of the noun if noun is one of the matching probabilities;prints out a message
        "You don’t see that here." if the noun is not one of the matching probability. 
        
        look: Str -> None
        
        Effects:
        print the name and the description of the noun to the screen if noun is 
        one of the matching probabilities
        print "You don’t see that here."
        '''
        if noun == 'me':
            self.player.look()
        elif noun == 'here':
            self.player.location.look()
        
        else:
            item_list = {}
            for item in self.player.inventory:
                item_list[item.name] = item
            for item in self.player.location.contents:
                item_list[item.name] = item
                
            if noun in item_list.keys():
                item_list[noun].look()
            else:
                print(self.msg_look_fail) 
    
    def inventory(self):
        ''' returns nothing, prints out the things in the player's inventory in 
        a given format.
        
        inventory: World -> None
        
        Effects: 
        prints out the things in the player's inventory in a given format
        '''
        if self.player.inventory ==[]:
            print(self. msg_no_inventory)
        else:
            print('Inventory: ', end=' ')
            for item in self.player.inventory[0:-1]:
                print(item.name,end=', ')
            print(self.player.inventory[-1].name)
            
            
    def take(self, noun):
        ''' returns nothing; mutates the World by  removing the thing and append 
        the thing to the player's inventory if the noun corespounding to a thing 
        in the current room and prints 'Taken' to the screen; prints the 
        msg_take_fail to the screen if there's not such a thing in the current 
        room.
        
        take: World Str -> None
        
        Effects: 
        mutates the World by removing the thing and append the thing
        to the player's inventory if the noun corespounding to a thing 
        in the current room and prints 'Taken' to the screen;
        
        prints "You can't take that." to the screen otherwise.
        
        '''
        item_list = {}
        for item in self.player.location.contents:
            item_list[item.name] = item 

        if noun in item_list.keys():
            room_things = self.player.location.contents
            inventory = self.player.inventory
            
            room_things.remove(item_list[item.name])
            inventory.append(item_list[item.name])
            print(self.msg_take_succ)
        else:
            print(self.msg_take_fail)
            
                        
    def drop(self, noun):
        ''' returns nothing; muatates the world by removing the thing from 
        the player's inventory and appending to the current room's contents if 
        the noun correspound to a thing in the player's inventory and prints 
        'Dropped' to the screen; prints the msg_drop_fail to the screen if 
        theere's not such a thing in the player's inventory.
        
        drop: World Str -> None
        
        Effect: 
        muatates the world by removing the thing from 
        the player's inventory and appending to the current room's contents if 
        the noun correspound to a thing in the player's inventory and prints 
        'Dropped' to the screen
        
        prints the "You aren't carrying that." to the screen if 
        theere's not such a thing in the player's inventory.
        
        '''
        item_list = {}
        for item in self.player.inventory:
            item_list[item.name] = item 
        
        
        if noun in item_list.keys():
            room_things = self.player.location.contents
            inventory = self.player.inventory
            
            inventory.remove(item_list[item.name])
            room_things.append(item_list[item.name])
            print(self.msg_drop_succ)
        
        else:
            print(self.msg_drop_fail)        
    def go(self, noun):
        ''' returns nothing; mutates self.player.room field if the given noun is
        one of the exits of player's current room that doesn't need a key and 
        look at the player's new current room, print a message to the screen if 
        the given noun is not one of the exits of player's current room;mutates
        self.player.room field and look at the player's new current room if the 
        given noun is one of the exits of player's current room and player has 
        the key in the inventory, prints out the exit message if the player doesn't
        owns the key.
        
        Effcts:
        mutates self.player.room field if the given noun is
        one of the exits of player's current room
        
        print "You can't go that way." to the screen if the given noun is not one
        of the exits of player's current room; prints out the exit message if 
        the player doesn't owns the key.
        
        go: World Str -> None
        '''
        current_location = self.player.location
        loe =list(filter(lambda x: x.name==noun,current_location.exits))
        
        if not(loe == []):
            if loe[0].key == None or loe[0].key in self.player.inventory: 
                self.player.location = loe[0].destination
                loe[0].destination.look()
            
            else:
                print(loe[0].message)
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
        '''opens a file called fname, writes the data from the world itself to 
        the file in the specific assignment format.
        
        save: World Str -> None
        '''
        f = open(fname,'w')
        list_things = []
        for room in self.rooms:
            list_things.extend(room.contents)
        
        list_things.extend(self.player.inventory)
        
        for thing in list_things:
            f.write('thing #'+str(thing.id)+' '+thing.name+'\n')
            f.write(thing.description+'\n')
        
        for room in self.rooms:
            f.write ('room #'+str(room.id) +' '+ room.name + '\n')
            f.write (room.description + '\n')
            f.write('contents ')
            for thing in room.contents:
                f.write( '#'+ str(thing.id)+ ' ')
            f.write('\n')
        
        f.write( 'player ' +'#'+ str(self.player.id) + ' '+ self.player.name+'\n')
        f.write(self.player.description)
        
        f.write('\n'+'inventory ')
        for owned in self.player.inventory:
            f.write('#'+str(owned.id)+' ')
        
        f.write('\n' + 'location #'+ str(self.player.location.id)+'\n')
        
        for room in self.rooms:
            for exit in room.exits:
                if exit.key == None:
                    f.write('exit '+'#'+str(room.id)+' #'+ 
                            str(exit.destination.id)+' '+exit.name+'\n')
                else:
                    f.write('keyexit '+'#'+str(room.id)+' #'+ 
                            str(exit.destination.id)+' '+exit.name+'\n')
                    f.write('#'+str(exit.key.id)+' ' + exit.message+ '\n')
        f.close()
                  
        

## Q2
def load(fname):
    ''' opens the file called fname, reads in each line and returns a World 
    constructed from the information in the text file.
    
    Effects: Reads file called fname
    load: String -> World
    '''
    f = open(fname,'r')
    line = f.readline()
    rooms =[]
    items =[]
    
    while (line != ''):
        
        if line.split()[0] == 'thing':
            item_name = ' '.join(line.split()[2:])
            item_number = int(line.split()[1][1:])            
            current_thing = Thing(item_number)
            current_thing.name = current_thing
            current_thing.description = line
            items.append(current_thing)
        
        elif line.split()[0] == 'room':
            item_name = ' '.join(line.split()[2:])
            item_number = int(line.split()[1][1:])            
            current_room = Room(item_number)
            rooms.append(current_room)
    
            current_room.name = item_name
            crdp= f.readline()
            current_room.description = crdp
            room_contents = f.readline()
            things_num = room_contents.split()[1: ]
            current_room.contents = []
            for ids in things_num:
                (current_room.contents).append(Thing(int(ids[1:])))
            
        elif line.split()[0] == 'player':
            item_name = ' '.join(line.split()[2:])
            item_number = int(line.split()[1][1:])            
            current_player = Player(item_number)
            current_player.name = item_name
            
            cpdp= f.readline()
            current_player.description = cpdp
            
            player_inventory = f.readline()
            things_num = player_inventory.split()[1: ] 
            current_player.inventory = []
            for ids in things_num:
                current_player.inventory.append(Thing(int(ids[1:])))
            items.extend(current_player.inventory)
            
            cpl= f.readline()
            item_number = int(cpl.split()[1][1:])
            current_player.location =  Room(item_number)
            
            current_world = World(rooms,current_player)
        
        elif line.split()[0] == 'exit':
            dest = int(line.split()[2][1])
            exit_name = ''.join(line.split()[3:])
            room_num = int(line.split()[1][1:])
            current_room =Room(room_num)
            current_exit = Exit(exit_name,Room(dest))
            current_exit.name = exit_name
            current_exit.dest = Room(dest)
            current_room.exits.append(current_exit)
            Room(room_num).exits.append(Room(dest))
        
        elif line.split()[0] == 'keyexit':
            dest = int(line.split()[2][1:])
            exit_name = ''.join(line.split()[3:])
            room_num = int(line.split()[1][1:])
        
            current_room =list(filter(lambda x:x.id == room_num,rooms))[0]
            dest_room = list(filter(lambda x:x.id == dest,rooms))[0]
            current_key_exit = Exit(exit_name,dest_room)
            
               
            
            key_line =f.readline()
            key_num = int(key_line.split()[0][1:])
            current_key = list(filter(lambda x:x.id == key_num,items))[0]
            current_message =''.join( key_line.split()[1:] )
            current_key_exit.message = current_message
            current_key_exit.key = current_key             
            
            current_room.exits.append(current_key_exit)
            Room(room_num).exits.append(Room(dest))
         
        line = f.readline()   
   
    return current_world

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


   