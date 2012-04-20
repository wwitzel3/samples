"""Linear Chamber Floaty Stuff

Take in a timing value and the initial position, layout, and direction
(indicated by R or L) of the chamber elements. Move those elements
through the chamber until they leave it. Show elements in the chamber
with X show empty space with '.'

>>> animate(2,'..R....')
['..X....', '....X..', '......X', '.......']

The single particle starts at the 3rd position, moves to the 5th, then
7th, and then out of the chamber.

>>> animate(3,'RR..LRL')
['XX..XXX', '.X.XX..', 'X.....X', '.......']

At time 1, there are actually 4 particles in the chamber, but two are
passing through each other at the 4th position

>>> animate(2,'LRLR.LRLR')
['XXXX.XXXX', 'X..X.X..X', '.X.X.X.X.', '.X.....X.', '.........']

At time 0 there are 8 particles. At time 1, there are still 6 particles,
but only 4 positions are occupied since particles are passing through
each other.

>>> animate(10,'RLRLRLRLRL')
['XXXXXXXXXX', '..........']

These particles are moving so fast that they all exit the chamber by
time 1.

>>> animate(1,'...')
['...']

>>> animate(1, 'LRRL.LR.LRR.R.LRRL.')
['XXXX.XX.XXX.X.XXXX.', '..XXX..X..XX.X..XX.', '.X.XX.X.X..XX.XX.XX', 'X.X.XX...X.XXXXX..X', '.X..XXX...X..XX.X..', 'X..X..XX.X.XX.XX.X.', '..X....XX..XX..XX.X', '.X.....XXXX..X..XX.', 'X.....X..XX...X..XX', '.....X..X.XX...X..X', '....X..X...XX...X..', '...X..X.....XX...X.', '..X..X.......XX...X', '.X..X.........XX...', 'X..X...........XX..', '..X.............XX.', '.X...............XX', 'X.................X', '...................']

"""

def get_left_right_elements(input, length):
    """Returns a left and right list of moving
    elements in the chamber with '.' surrounding them."""
    
    left = ['.'] * length
    right = ['.'] * length
    
    for pos,element in enumerate(input):
        if element == 'L':
            left[pos] = element
        elif element == 'R':
            right[pos] = element
    return (left, right)

def shift(speed, input, length):
    """Shifts a given input list containing a single direction
    or empty '.' given the timing amount. Replaces items that go
    out of bounds with an empty '.'
    """
    output = ['.'] * length
    
    for pos,element in enumerate(input):        
        if element == '.':
            continue
        elif element == 'L' and (pos-speed) >= 0:
            output[pos-speed] = 'L'
        elif element == 'R' and (pos+speed) < length:
            output[pos+speed] = 'R'
    return output

def merge(input1, input2, length):
    """Returns a merged 'X' string of
    a left and right movement listing.
    """
    output = ['.'] * length
    for pos,lr in enumerate(zip(input1,input2)):
        if lr[0] == 'L' or lr[1] == 'R':
            output[pos] = 'X' 
        elif lr[0] == 'R' or lr[1] == 'L':
            output[pos] = 'X'
    return output
    
def animate(speed, init):
    init = list(init)
    length = len(init)
    
    output = []
    floated_away = False
    started = False    
    
    left_elements, right_elements = get_left_right_elements(init, length)

    while(True):
        if not started:
            output.append("".join(merge(left_elements, right_elements, length)))
            started = True
        else:
            right_elements = shift(speed, right_elements, length)
            left_elements = shift(speed, left_elements, length)
            output.append("".join(merge(left_elements, right_elements, length)))
        
        # check the last element of output if it contains nothing but '.'
        # break out of the while loop
        if output[-1] == ('.' * length):
            floated_away = True
        else:
            floated_away = False
            
        if floated_away:
            break
         
    return output

if __name__ == '__main__':
    import doctest
    doctest.testmod()
