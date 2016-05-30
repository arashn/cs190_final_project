
import math
from PIL import Image
import play_note

'''Function to determine final note Frequency and Duration'''
def processNotes(note_info):
    notes = []
    note = []
    #print note_info
    for n in note_info:
        #print n
        if(n[3] == "stem"):
            if(n[2] == "filled"):
                note.append(4)
            else:
                note.append(2)
        else:
            note.append(1)
        if(n[1] == "center"):
            if(n[0] == 1):
                note.append(784)
            elif(n[0] == 2):
                note.append(659.3)
            elif(n[0] == 3):
                note.append(523.3)
            elif(n[0] == 4):
                note.append(440)
            elif(n[0] == 5):
                note.append(349.2)
            elif(n[0] == 6):
                note.append(293.7)
            elif(n[0] == 7):
                note.append(246.9)
        else:
            if(n[0] == 1):
                note.append(698.5)
            elif(n[0] == 2):
                note.append(587.3)
            elif(n[0] == 3):
                note.append(493.9)
            elif(n[0] == 4):
                note.append(392)
            elif(n[0] == 5):
                note.append(329.6)
            elif(n[0] == 6):
                note.append(261.6)
            elif(n[0] == 7):
                note.append(220)
        #print(note)
        notes.append(note)
        #print notes
        note = []


    return notes

'''Function to determine where the note is on the bars and find if filled or hollow
'''
def getLocationandFill(whitebars, pix, note_middles, threshold, stems):
    note_info = []

    #find location and if filled
    middle_index = 0
    for m in note_middles:
        bar_num= 0
        for b in whitebars:
            bar_num = bar_num + 1
            found_mid = 0
            is_filled = "filled"
            for i in range(b[0],b[1]):
                c = pix[m,i][0]
                if(c < threshold):
                    found_mid = 1
                elif(found_mid == 1 and c > threshold):
                    is_filled = "empty"
                else:
                    pass
            if(found_mid == 1):
                if pix[m,b[1]][0] < threshold and pix[m,b[0]][0] < threshold:
                    note_info.append([bar_num, "center", is_filled, stems[middle_index]])
                    print str(bar_num) + " center : " + is_filled
                else:
                    note_info.append([bar_num, "line", is_filled,  stems[middle_index]])
                    print str(bar_num) + " line : " + is_filled
                break
        middle_index = middle_index + 1


    return note_info

'''Function that scans the white bars from right to left and finds saves each encounter with a black pixel.'''
def sweepRight(whitebars, im, threshold):

    a = im.size[0]-1 #will represent the x coordinate
    on_note = 0 #boolean for if we have seen a note
    current_note = [] #stores current information about the note
    list_of_notes_right = [] #hold all notes
    while(a > -1):#search each whitespace line

        points = []
        for b in whitebars:

            for n in range(b[0],b[1]):
                c = pix[a,n][0]
                if(c < threshold):
                    points.append(c)

        if(len(points) > 0):

            current_note.append(a)
            current_note.append(points)
            list_of_notes_right.append(current_note)
            current_note = []
            a = a - (largest_bar_height*2)
        else:
            pass


    	a = a - 1

    return list_of_notes_right


'''Function that scans the white bars from left to right and finds saves each encounter with a black pixel.'''
def sweepLeft(whitebars, im, threshold):

    a = 0 #will represent the x coordinate
    on_note = 0 #boolean for if we have seen a note
    current_note = [] #stores current information about the note
    list_of_notes_left = [] #hold all notes
    while(a < im.size[0]):#search each whitespace line

        points = []
        for b in whitebars:
            #print(b)
            for n in range(b[0],b[1]):
                c = pix[a,n][0]
                if(c < threshold):
                    #print(c)
                    points.append(c)
        if(len(points) > 0):
            current_note.append(a)
            current_note.append(points)
            list_of_notes_left.append(current_note)
            current_note = []
            a = a + (largest_bar_height*2)
        else:
            pass

    	a = a + 1


    return list_of_notes_left



#------------------------------Start of program ---------------------------------------#

im = Image.open("notes22.png") #Can be many different formats.
pix = im.load()
print "THE SIZE IS: "
print im.size #width and hight of the image
x = 0 # x coordinate
y = 0 # y coordinate
threshold = 200

#---------------------Find first left most black pixel --------------------------------#

#Search for first occurence of a non-white pixel
found = 0
while( found == 0):
	y = 0
	while( y < im.size[1]):
		c = pix[x,y][0]
		if(c < threshold):
		  found = 1
		  break
		y = y + 1
	x = x + 1

#--------------------------- Find lines and white bars -----------------------------------------------#

on_line = 0 #boolean value to indicate if we are on a line
y = 0   #reset y value to 0
current = [] #list of coordinates of current line
list_of_lines = [] #list of all lines
prev_last = -1 #used to keep track of the end coordinate of the previous line
whitebars = [] #keeps track of white bar information
largest_bar_height = 0 #used to determine the of a note in note in pixels

while(y < im.size[1]):
    c = pix[x,y][0]
    if(c < threshold and on_line == 0):
        on_line = 1
    	current.append(y)
    	if(prev_last > -1):
            bar_start = prev_last + 1
            bar_end = y - 1
            bar_length = bar_end - bar_start
            whitebars.append([bar_start, bar_end, bar_length])
            if(bar_length > largest_bar_height):
                largest_bar_height = bar_length
    elif(c < threshold and on_line == 1):
		current.append(y)
    elif(c > threshold and on_line == 1):
		on_line = 0
		list_of_lines.append(current)
		prev_last = y-1
		#print current
		current = []
    else:
		pass
    y = y + 1



#adds 2 invisible bars above to below first and last lines
first_line = list_of_lines[0]
f_start = (first_line[0]-1-largest_bar_height)
f_end = (first_line[0]-1)
whitebars.insert(0,[f_start,f_end, largest_bar_height])
'''if(f_start > 0):
    f2_end= f_start - len(first_line)
    f2_start = f2_end - largest_bar_height
    if(f2_start < 0):
        f2_start = 0
    whitebars.insert(0,[f2_start,f2_end, largest_bar_height])'''
last_line = list_of_lines[len(list_of_lines)-1]
l_end = (last_line[len(last_line)-1]+largest_bar_height)
#if the end invisible bar is greater than height of the image
if(l_end  > im.size[1]-1):
    l_end = im.size[1]-1
whitebars.append([(last_line[len(last_line)-1]+1), l_end, largest_bar_height])
'''if(l_end < im.size[1]-1):
    l2_start = l_end + len(last_line)
    l2_end = l2_start + largest_bar_height
    if(l2_end  > im.size[1]-1):
        l2_end = im.size[1]-1
    whitebars.append([(last_line[len(last_line)-1]+1), l2_end, largest_bar_height])'''

print "lines are:"
print list_of_lines
print "white spaces"
print whitebars
print "largest bar height:"
print largest_bar_height

#------------------ Scan the white bars for notes ------------------------------#

#Sweep left to right
list_of_notes_left = sweepLeft(whitebars, im, threshold)

print "Number of notes"
print len(list_of_notes_left)
#print "note coordinates"
#print list_of_notes_left

#Sweep Right to left
list_of_notes_right = sweepRight(whitebars, im, threshold)


print "Number of notes"
print len(list_of_notes_right)
#print "note coordinates"


#------------------Analyze scanned data to determine note attributes ----------------------------------#

m_size = len(list_of_notes_left) #size of raw list
diff = 0
note_middles = []
stems = []

#get distances between left and right side of note
for i in range(0,m_size):
    print str(i)+" Left x: " + str(list_of_notes_left[i][0]) + " : Right x: " + str(list_of_notes_right[(m_size-i-1)][0])
    diff =  list_of_notes_right[(m_size-i-1)][0] - list_of_notes_left[i][0]
    if(diff < largest_bar_height/2): #skip black bars
        pass
    else:
        #get if note has stem
        if(len(list_of_notes_left[i][1]) != len(list_of_notes_right[(m_size-i-1)][1])):
            stems.append("stem")
        else:
            stems.append("none")
        mid = (list_of_notes_right[(m_size-i-1)][0] + list_of_notes_left[i][0])/2
        note_middles.append(mid)
print note_middles

#get the placement of the notes and if it is filled
note_info = getLocationandFill(whitebars, pix, note_middles, threshold, stems)

print "note info: "
final_output = processNotes(note_info)
print final_output

play_note.play_note(final_output)
