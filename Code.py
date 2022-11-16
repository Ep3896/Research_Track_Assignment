from __future__ import print_function

import time
from sr.robot import *


################### List of used variables ###################

R = Robot()

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

count = 0
""" integer: variable for counting the number of silver token placed """

List_golden = []
""" List: used for saving the offset of value of the the golden objects paired"""

List_silver = []
""" List: used for saving the value of the offset of the silver objects seen at the beginning of the program """

List_elements_removed = []
""" List: used for saving the value of the offset of the silver objects dropped and paired to the golden ones """

position=0
"""integer: variable for pointing the position of the List_golden"""

position_rem=0
""" integer: variable for pointing the position of the List_elements_removed"""

position_silver=0
"""integer: variable for pointing the position of the List_silver"""

max_silver_token_number=0
""" integer: variable for saving the number of silver token seen in the arena by the robot"""

grabbed= False
""" bool: variable for letting the robot know that it has a silver token grabbed"""


################### List of used functions  ###################

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    global List_silver 
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.offset not in List_elements_removed:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

def find_golden_token():
    global List_golden
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.offset not in List_golden:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
   	return dist, rot_y

def vision_all_silver():
    markers = R.see()
    global List_silver
    global List_golden
    global max_silver_token_number
    global position_silver
    for m in markers:
        if( m.info.marker_type == MARKER_TOKEN_SILVER):
            print ("Token Silver",m.info.offset, "is metres away", m.dist)
            if m.info.offset not in List_silver:
                if m.info.offset not in List_elements_removed:
                    List_silver.insert(position_silver,m.info.offset)
                    print('List Silver is', List_silver)
                    position_silver = position_silver +1
                    max_silver_token_number = max_silver_token_number +1
                    print( 'max_silver_token_number is', max_silver_token_number)                
                    print("Silver_Token_List",List_silver)
                    print("Maximum silver token number", max_silver_token_number)
        
def get_offset_silver():
    offset=1
    dist=100
    markers = R.see()
    for m in markers:
        if m.dist < dist and m.info.marker_type is MARKER_TOKEN_SILVER:
            offset=m.info.offset
            dist=m.dist
       
    return offset
                          
def get_offset_gold():
    offset=1
    dist=100
    markers=R.see()
    for m in markers:
        if m.dist < dist and m.info.marker_type is MARKER_TOKEN_GOLD:
            offset=m.info.offset
            dist=m.dist
    return offset

def avoid_obstacles_silver():
    
    d_th = 0.6
    markers = R.see()
    for m in markers:
        if m.info.marker_type is MARKER_TOKEN_SILVER and m.dist < d_th and grabbed== True and m.info.offset not in List_elements_removed:
            if 0 <=m.rot_y:
                turn(-20,1)
                drive(20,1)
                turn(+20,1)
            else:
                turn(+20,1)
                drive(20,1)
                turn(-20,1)                
            
            
################### Main script ###################

vision_all_silver()

while 1:
    
    avoid_obstacles_silver()
       
    #Check to find the values of the closest silver or golden token
    if (silver == True):
        dist, rot_y = find_silver_token()
        offset = get_offset_silver()
    else:
        dist, rot_y = find_golden_token()
        offset= get_offset_gold()
    
    
    #Which action/movement the Robot has to do based on the dist, rot_y and offset given
    if (dist ==-1):
        print("no object detected, too far")
        turn(+5,1)
        
    elif (dist <d_th and silver ==True): 
        print("I've found the silver object!")
        if R.grab():
            grabbed= not grabbed
            print("got it")
            List_silver.remove(offset) # silver token offset is removed from this list to avoid to grab it again
            List_elements_removed.insert(position_rem, offset)
            print( 'List elements removed:', List_elements_removed)
            print('List silver:', List_silver)
            silver= not silver
        else:
            print ("I'm not close enough!")

        
    elif (dist < 0.6) & (silver == False):
        print("I've found the golden object!")
        silver == True
        R.release()           
        List_golden.insert(position,offset) # golden token offset is added to the list to avoid to pair it again
        positiion = position +1
        print('List Golden is',List_golden)
            
        count = count +1
        if count ==max_silver_token_number: #if it's true , then all the tokens are paired and the program exits
            turn(45,1)
            drive(10,5)
            print("Task Completed!")
            exit()  # program quits
        print("leave it here!")
        silver = not silver
        grabbed= not grabbed
        turn(50,1)            
               
    elif -a_th<= rot_y <= a_th:
        print("Ah, that'll do.")
        drive(25, 0.5)


    elif rot_y < -a_th:
        print("Left a bit...") 
        turn(-2, 0.5)

      
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)


            
    
   
        
    
        
