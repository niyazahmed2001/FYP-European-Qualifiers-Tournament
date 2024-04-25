from math import radians, cos, sin, asin, sqrt # imported for handling data
import pandas as pd
import random # for shuffling lists
import time # for performance timing
import sys # for system-level operations

def printStadium(A, B):
    dist = 1000000 # Initializes dist with a very high value, initial threshold for finding the minimum distance
    minStad = "" # a string variable intended to store the name of the stadium from team A that is closest to any stadium of team B
    for stadA in Stadiums[A]: # Iterates over each stadium associated with team A
        for stadB in Stadiums[B]: # Nested loop that iterates over each stadium associated with team B
            D = distance(Stadiums[A][stadA], Stadiums[B][stadB]) # calculates distance using the coordinates provided in the Stadiums dictionary
            if D < dist: # dist condition checks if the calculated distance D is less than the current minimum distance
                dist = D
                minStad = stadA # if D is smaller mindstad is updated to stadA
# Takes A and B tries to computate minimum distances between these points
    # Print using UTF-8 encoding
    sys.stdout.buffer.write(f"{stadA}\n".encode('utf-8'))

ForbiddenList = [("Armenia" , "Azerbaijan"),
                 ("Belarus" , "Ukraine"),
                 ("Gibraltar" , "Spain"),
                 ("Kosovo" , "Bosnia and Herzegovina"),
                 ("Kosovo" , "Serbia")]
# These teams cannot play each other
WinterList = ["Belarus", "Estonia", "Faroe Islands", "Finland", "Iceland", "Latvia", "Lithuania", "Norway"]
# Winter List part of the regulations (severe winter locations) No more than 2 in 1 group
def distance(coords1, coords2):
    """Function to find the distance between two latitude, longitude points on earth
    Args:
        coords1 (tuple): Tuple containing the latitude/longitude of point 1
        coords2 (tuple): Tuple containing the latitude/longitude of point 2
        unit (string): Value to switch unit of measure, default is Miles other option is Kilometers

    Returns:
        distance (float): Distance calculated between two points on a sphere using the haversine formula
    """
# Calculate distance between two stadium points
    lat1 = radians(coords1[0])
    long1 = radians(coords1[1])
    lat2 = radians(coords2[0])
    long2 = radians(coords2[1])

    delta_long = long2 - long1
    delta_lat = lat2 - lat1

    # Compute haversine of two points
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2
    # Compute distance by completing the formula
    c = 2 * asin(sqrt(a))
    # Select radius value for earth based on unit
    r = 6371
    return c * r
# Line 55 calculates distance between the two teams
def calcDistTeam(A, B):
    for pair in ForbiddenList:
        if A in pair and B in pair:
            #print("Forbidden Clash")
            return -1
# Line 56 - 59 will check to see if teams are in forbidden list
    dist = 1000000
    for stadA in Stadiums[A]:
        for stadB in Stadiums[B]:
            D = distance(Stadiums[A][stadA], Stadiums[B][stadB])
            dist = min(dist, D)
            #print(stadA, stadB, D)
# Line 61 - 65 will go through all stadiums of both Team A/B as some teams have more than 1 stadium, will pick stadium with the least distance    
    return dist
# https://en.wikipedia.org/wiki/Haversine_formula 
def calcDistGroup(Group):
# Calculates total travel distance for a group by evaluating all possible matchups
    winterCount = 0
    for country in Group:
        if country in WinterList:
            winterCount = winterCount + 1
# Line 72 - 75 calculates how many teams in the group have harsh winter
    if winterCount > 2: # If number of countries exceeds 2 it will return -1
        #print("Winter")
        return -1 # -1 meaning it is not possible

    dist = 0 # Initilaising distance to 0
    
    L = len(Group) # Will go over all teams 1 by 1
    for i in range(L):
        for j in range(L):
            
            if i != j: # If team 1 is at home ground it will not add to total distance
                
                D = calcDistTeam(Group[i], Group[j]) # Calculate distance travelled by all teams in group
                if D < 0: # Checking validity if distance less than 0 it is invalid
                    return D

                dist = dist + D # If valid returns distance of group added onto total distance travelled

    return dist
# Function which calculates distance by all teams in the league
def calcDistLeague(Team):

    dist = 0
# A group will have 4 countries
    i=4
    while i < len(Team): # Will go over the groups
        Group = Team[i-4:i] # Tkes 4 teams at a time - Slicing notation

        D = calcDistGroup(Group) # Calculates distance by teams within group
        if D < 0: # If distance is less than 0 then group is invalid returns -1
            return D
        # If group is valid it will add to total distance line 119 then add to total distance in league
        dist = dist + D

        i = i + 4

    Group = Team[i-4:len(Team)] # Creating sub-group from larger list of teams

    D = calcDistGroup(Group) # Specific group selected using slicing
    if D < 0: # checks if the returned distance D is less than 0
        return D # If D is negative, the function returns D and won't continue

    dist = dist + D # adds distance to current group

    return dist # returns distance

def printStadium(A, B):

    dist = 1000000
    minStad = ""
    for stadA in Stadiums[A]:
        for stadB in Stadiums[B]:
            D = distance(Stadiums[A][stadA], Stadiums[B][stadB])

            if D < dist:
                dist = D
                minStad = stadA

    print(stadA.encode("utf-8"), end = "")

def printGroup(Group):

    L = len(Group)
    for i in range(L):
        for j in range(L):            
            if i != j:
                print(Group[i], "will play against", Group[j], "at", end = " ")
# printGroup Function: Inside this function, for each pair of teams in the group, 
# the printStadium function is called which calculates and prints the shortest distance between stadiums for a match.
                printStadium(Group[i], Group[j])

                print(" stadium in", Group[i])


def printTeams(Team, name):

    i=4
    ind = 1
    while i < len(Team):
        Group = Team[i-4:i]
        
        print("Group", name+str(ind), "consists of", end = " ")
        for count in Group[:-1]:
            print(count, end = ", ")
        print(Group[-1])
        printGroup(Group)
        
        i = i + 4
        ind = ind + 1

    Group = Team[i-4:len(Team)]
 # https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-pandas-dataframe   
    print("Group", name+str(ind), "consists of", end = " ")
    for count in Group[:-1]:
        print(count, end = ", ")
    print(Group[-1])
    printGroup(Group)
# This function iterates over groups of teams and prints each group. 
# It calls the printGroup function to handle the details of each match within a group.

def generate_groups(league, name): # random shuffling and the hill-climbing optimization
# Function to generate groups
    Team = league["Teams"][:]
## Makes local copy of teams in the league
    dist = 1000000
    bestTeam = []

    t1 = time.time() # Measures time for start of optimsation and end
    for i in range(10000): # 10000 iterations for which the loop will run
        random.shuffle(Team)
        D = calcDistLeague(Team)
# Shuffles teams randomly, randomised tournament, optimising and randomising. Randomly shuffles then calculates distance of all teams in league
        if D < 0: # Validates teams to continue
            continue
# Distance returns -1 if group isnt valid with restrictions e.g Russia cant play Ukraine. Line 190 optimastion for teams with smaller distance
        if D < dist: # If distance is closer it continues with that team
            dist = D
            bestTeam = Team[:]
            print("Iteration:", i, "Distance:",dist)
# Above is hill climbing algorithm, iteration 10000, there is no better team, searches 10000 times. Can modify.            
    t2 = time.time()
# Line 192 if new team has smaller than distance than team before it is classed as best team. Line 194 will assign that team as best team
    print("Time Taken for optimizing League", name, "was", int(t2-t1), "seconds") # Calculated by subtracting start time and end time of optimisation
    print("Optimized Groups for League", name, "are:")
    printTeams(bestTeam[:], name)
    print()
    print()
# https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-pandas-dataframe
    league["Teams"] = bestTeam[:]

def getStadium(A, B):

    dist = 1000000
    minStad = ""
    for stadA in Stadiums[A]:
        for stadB in Stadiums[B]:
            D = distance(Stadiums[A][stadA], Stadiums[B][stadB])

            if D < dist:
                dist = D
                minStad = stadA
# This function calculates the minimum distance between any two stadiums (one from each team's available stadiums) 
# prints the name of the stadium of the first team.
    return minStad, dist
# Writegroup function for all teams in group, will go over all matches and outputs on a CSV file
def writeGroup(Group, f):
    L = len(Group)
    for i in range(L):
        for j in range(L):            
            if i != j:

                stadium, dist = getStadium(Group[i], Group[j])
# Will write eg: Team1, team2, Staidum Name, Dist...
                f.write(Group[i])
                f.write(",")
                f.write(Group[j])
                f.write(",")
                f.write(stadium)
                f.write(",")
                f.write(str(dist/1000.0)) #Divide by 1000 to get distance in KM
                f.write("\n")
# Used f.write method to a csv file, team 1, team 2...    
def writeTeams(Team, f):
    i=4 # initilialising i to 4 segments of four.
    ind = 1
    while i < len(Team): # while loop that runs as long as i is less than the length of the Team list, ensuring that all teams are processed.
        Group = Team[i-4:i] # Go over groups in teams of 4
        writeGroup(Group, f) # Write the group
        
        i = i + 4 # Increments i by 4 to move the slicing window to the next group of four teams
        ind = ind + 1 # Increments ind by 1,tracking the number of groups processed

    Group = Team[i-4:len(Team)] # handles any remaining teams that didn't fit into a complete group of four - makes last group
    writeGroup(Group, f) # Calls the writeGroup function again to write details about this final group of teams to the file

def generate_output_csv(leagues):
    f = open("All fixtures and Stadiums.csv", 'w', encoding="utf-8") # Creates file named All fixtures...
    f.write("Team1,Team2,Stadium,Distance\n") # Headers for all columns in csv
    for league in leagues:
        writeTeams(leagues[league]["Teams"], f) # Writes teams in league
    f.close() # Close file
    
if __name__ == "__main__":

    Stadiums = {} # initilizing empty dictionary
    
    df_loc = pd.read_excel("Stadiums X Y.xlsx")
    for i in range(len(df_loc)):
        StadCount = df_loc.loc[i, "Country"].strip()
    # Loads stadium positions Line 261 into dictionary (df_loc)
        if StadCount[-1].isnumeric(): # Checkes if country has number after it
            Country = StadCount[:-1] # Removes number if there is
        else:
            Country = StadCount

        if Country not in Stadiums.keys():
            Stadiums[Country] = {}

        Name = df_loc.loc[i, "Name of Stadium"].strip()

        Stadiums[Country][Name] = (df_loc.loc[i, "Latitude"], df_loc.loc[i, "Longitude"])
# Line 275 fills dictionary, two keys: Name of country, Name of Stadium, Long / Lat of Stadium
# Line 263 - 273 processing all info of Stadiums
    # Ref: https://www.uefa.com/nationalassociations/uefarankings/country/#/yr/2024
    f = open('UEFA national team coefficient rankings.csv', 'r')
    data = f.readlines()
    f.close()
# Rankings saved within CSV file
    leagues = {}
    # Initializes an empty dictionary called leagues that will store information about different leagues.
    leagues["A"] = {} # Creates a dictionary entry for League A and initializes an empty list to store the teams that will be part of this league    
    leagues["A"]["Teams"] = []
    for i in range(16): # Iterates through the first 16 entries of the data list
        if data[i].rstrip() == "Russia": # skips Russia
            continue

        leagues["A"]["Teams"].append(data[i].rstrip()) # adds the team to League A

    print("Optimizing League A") # Print a message indicating the start of the optimization process for League A
    generate_groups(leagues["A"], "A") # Calls generate_groups function which arrages teams into groups

    
    leagues["B"] = {}    
    leagues["B"]["Teams"] = []
    for i in range(16, 32):
        if data[i].rstrip() == "Russia":
            continue
        
        leagues["B"]["Teams"].append(data[i].rstrip())

    print("Optimizing League B")
    generate_groups(leagues["B"], "B")
    
    leagues["C"] = {}    
    leagues["C"]["Teams"] = []
    for i in range(32, 48):
        if data[i].rstrip() == "Russia":
            continue
        
        leagues["C"]["Teams"].append(data[i].rstrip())

    print("Optimizing League C")
    generate_groups(leagues["C"], "C")


    leagues["D"] = {}    
    leagues["D"]["Teams"] = []
    for i in range(48, 55):
        if data[i].rstrip() == "Russia":
            continue
        
        leagues["D"]["Teams"].append(data[i].rstrip())

    print("Optimizing League D")
    generate_groups(leagues["D"], "D")

    generate_output_csv(leagues) # generate a CSV file outputting all the fixtures and stadiums, which records all matches and associated details across all leagues
# https://www.geeksforgeeks.org/indexing-and-selecting-data-with-pandas/