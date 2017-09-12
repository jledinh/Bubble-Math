import math
def distance(point1,point2):
    return math.hypot(point1[0]-point2[0],point1[1]-point2[1])
    
if __name__ == "__main__":
    print "This module distance between two tuples."
    raw_input("\n\nPress the enter key to exit.")
