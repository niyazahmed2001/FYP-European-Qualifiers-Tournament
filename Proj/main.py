import pandas as pd
import math
# https://en.wikipedia.org/wiki/Haversine_formula 
def Haversine(lat1, long1, lat2, long2):
    r = 6335.43e3

    lat1 = lat1*math.pi/180
    long1 = long1*math.pi/180

    lat2 = lat2*math.pi/180
    long2 = long2*math.pi/180
# Line 7 - 8 & 10 - 11 Takes Lat/Long Team 1 (start position) and Lat/Long Team 2 (destination)
    t1 = math.sin(0.5*(lat2-lat1))*math.sin(0.5*(lat2-lat1))
    t2 = math.sin(0.5*(long2-long1))*math.sin(0.5*(long2-long1))

    sq = t1 + math.cos(lat1)*math.cos(lat2)*t2
    sq = max(0, sq)

    root = math.sqrt(sq)

    arcS = math.asin(root)

    dist = 2*r*arcS

    return dist
# Line 4 - 25 Haversine Distance Formula
df_matches = pd.read_excel('All fixtures and Stadiums.xlsx') # Excel file for all fixtures
df_loc = pd.read_excel('Stadiums X Y.xlsx') # Excel file for stadiums X Y points
# Line 27 & 28 Loading excel files by using Pandas. Pandas read excel files as a dataframe
loc_dict = {} # loc_dict – made a dictionary for location, the dictionary has all teams long/lat
loc_dict["Team 1 Latitude"] = []
loc_dict["Team 1 Longitude"] = []
loc_dict["Team 2 Latitude"] = []
loc_dict["Team 2 Longitude"] = []
loc_dict["Distance"] = []

total_distance = 0 # initialised total distance to 0 – this is the total distance travelled by all the teams

for i in range(len(df_matches)): # wrote a for loop which goes over all the matches one by one, will start from first column of excel file. It will get team 1 and then team 2 location.

    team1 = df_matches.loc[i, "Team1"].strip()
    team2 = df_matches.loc[i, "Team2"].strip()
# “Team1” “Team2” are headers of the column in the excel files
    team1Lat = None
    team1Long = None
    team2Lat = None
    team2Long = None
# Initialisation in python you initialise it to be null     
    for j in range(len(df_loc)):

        if df_loc.loc[j, "Country"].strip() == team1:
            team1Lat = df_loc.loc[j, "Latitude"] 
            team1Long = df_loc.loc[j, "Longitude"]
# Will go to location dataframe and see if you can find team1 then read lat/long
        if df_loc.loc[j, "Country"].strip() == team2:
            team2Lat = df_loc.loc[j, "Latitude"] 
            team2Long = df_loc.loc[j, "Longitude"]
# Will go to location dataframe and see if you can find team2 then read lat/long
# Initiliased all points to be 0 then it searched in location dataframes both team 1 and 2 long/lat.
    if team1Lat is None or team2Lat is None or team1Long is None or team2Long is None:
        print("Record Corrupt", team1Lat, team2Lat, team1Long, team2Long, team1, team2)
    else:
        loc_dict["Team 1 Latitude"].append(team1Lat)
        loc_dict["Team 1 Longitude"].append(team1Long)
        loc_dict["Team 2 Latitude"].append(team2Lat)
        loc_dict["Team 2 Longitude"].append(team2Long)
# Line 61 Exception or Error handling – if you’re not able to find the team within the excel it will say “record corrupt”
# Now initialising from the dictionary line 30. You’ll have team 1 and 2 lat/long. Initialise to avoid errors.
        dist = 2*Haversine(team1Lat, team1Long, team2Lat, team2Long) # Times haversine distance by 2 as team is travelling once there and once back
        total_distance += dist # So add the distance on line 69 to the total distance

        loc_dict["Distance"].append(dist) # Assigning it to location dictionary
# Note: Initialising it on line 30 then adding info of country on line 63
new_data_frame = pd.DataFrame(loc_dict)
# Now assigned a temporary dataframe, made a panda dataframe from the location dictionary
# You can convert a dictionary to a panda dataframe
# Panda is a library made for analysing data

df_matches = pd.concat((df_matches,new_data_frame),axis=1) # pd.concat concatenates the new information creates new temporary dataframe (df_matches: Team1, Team2, Distance)
# Now have the table of matches and will add new information like team 1 and 2 long/lat and distance
# Line 63 Adding more columns to the dataframe (Team1 Lat, Team1 Long, Team2 Lat, Team2 Long, Distance)
loc_dict = {}
loc_dict["Total Distance"] = []
for j in range(len(df_loc)):
    loc_dict["Total Distance"].append(0)
# Line 82 Creates a dictionary and total distance will be intialised to 0. This dictionary will hold the total distance covered by all the countries.
for i in range(len(df_matches)): # Will go over all the matches one by one

    team1 = df_matches.loc[i, "Team1"].strip() # Identifying team 1

    for j in range(len(df_loc)):
        if df_loc.loc[j, "Country"].strip() == team1:
            loc_dict["Total Distance"][j] += df_matches.loc[i, "Distance"] # Will add the distance of team 1 

new_data_frame = pd.DataFrame(loc_dict) # Will find in loc_dict where the team is (loc_dict: Country, Distance)
df_loc = pd.concat((df_loc,new_data_frame),axis=1)
# Again made a dataframe and append it to our location dictionary
# New dataframe loc_dict will look like this: Country, Lat, Long, Distance
# 	https://realpython.com/pandas-merge-join-and-concat/
total_distance = total_distance/1000 # Convert the distance in km by /1000 the distance m to km
# Up until this point we have total distance travelled by all countries and total distance travelled by each country
dupDict = {} # Initialize an Empty Dictionary -used to store indices of the DataFrame rows (df_loc) where the country names are duplicates
for i in range(len(df_loc)):

    nameO = df_loc.loc[i, "Country"].strip()
    
    for j in range(len(df_loc)):
        nameI = df_loc.loc[j, "Country"].strip()

        if nameI[-1].isdigit(): # Removes number at end
            if nameO == nameI[:-1]:
                if i not in dupDict.keys():
                    dupDict[i] = []
    
                dupDict[i].append(j)
# Duplicate dictionary for duplicate countries eg Ukraine Ukraine 2
dropList = []
for i in dupDict:
    for j in dupDict[i]:
        df_loc.loc[i, "Total Distance"] += df_loc.loc[j, "Total Distance"] # Will add all the duplicates distance to total distance within dataframe
        dropList.append(j) # Delete all the duplicates after
# Will merge all duplicate distances and turn it into one distance
# removes the duplicate entry from dataframe
# dupdict: has all the duplicate countries

df_loc = df_loc.drop(dropList)
# New column “group” has been added. 
Groups = {}
# Ref: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-pandas-dataframe
for j, row in df_loc.iterrows(): # Will go through teams and check what group they are in. For e.g. England is group A it will add distance travelled by England and add to group A.
    grp = df_loc.loc[j, "Group"]

    if grp not in Groups: # Check if grp is a Key in Groups Dictionary
        Groups[grp] = 0 # checks whether a group identified by grp is already a key in the Groups dictionary. If not initialises to 0.

    Groups[grp] += df_loc.loc[j, "Total Distance"] # adds the total distance retrieved from the DataFrame df_loc to Total Distance in in Groups dictionary
print(f"Total Distance travelled is {total_distance:.2f} km.")

for grp in Groups: # Loops over each distance in group and divided by 1000 to get km
    dist = Groups[grp]
    dist = dist / 1000

    L = [] # Empty List will sotore with countries in that specific group
    for j, row in df_loc.iterrows(): # nested loop iterates through 'df_loc' checks if 'Group' value of each row matches the current group grp
        g = df_loc.loc[j, "Group"] # if so, adds the corresponding 'Country' value to the list L

        if g == grp:
            L.append(df_loc.loc[j, "Country"])
            
    print(f"Group {grp}, {L} travelled a distance of {dist:.2f} km.")

for j, row in df_loc.iterrows():
    dist = df_loc.loc[j, "Total Distance"]
    dist = dist / 1000

    name = df_loc.loc[j, "Country"] # prints each country distance

    print(f"{name}'s team travelled a distance of {dist:.2f} km.")
#prints out a formatted string for each group, listing the group identifier, the countries in the group, and the total distance traveled by that group in kilometers
# https://www.geeksforgeeks.org/working-with-excel-files-using-pandas/