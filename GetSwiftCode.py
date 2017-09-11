import time
import datetime
import requests
import simplejson as json
import ast
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

#
# Step 1: Get the data from drones API and create a curated list
#
drones_req = requests.get('https://codetest.kube.getswift.co/drones')
x = ast.literal_eval(drones_req.text)
drones_list = []
for elem in x:
    temp = json.dumps(elem)
    temp = json.loads(temp)
    drones_list.append(temp)
    #print(temp);
# print generic info
print("Number of drones available: ", len(drones_list))

#
# Step 2: Get the data from packages API and create a curated list
#
packages_req = requests.get('https://codetest.kube.getswift.co/packages');
x = ast.literal_eval(packages_req.text);
packages_list = [];
for elem in x:
    temp = json.dumps(elem);
    packages_list.append(json.loads(temp));
# print generic info
print("Number of packages available: ", len(packages_list));

#
# Step 3: add distance information to the lists and sort them
#
geolocator = Nominatim()
location = geolocator.geocode("303 Collins Street, Melbourne, VIC 3000")
depo_location = (location.latitude,location.longitude)

for idx, drone_info in enumerate(drones_list):
    drone_location = (drone_info["location"]["latitude"],drone_info["location"]["longitude"])
    if len(drone_info["packages"])>0:
        curr_package_destination = drone_info["packages"][0]
        # print(curr_package_destination)
        # there will only be one package assigned to drone
        destination_location = (curr_package_destination["destination"]["latitude"],curr_package_destination["destination"]["longitude"])
    else:
        # distance drone has to travel to drop package is 0
        destination_location = drone_location
    # Below variable represents the distance to travel before reaching depo for picking up next package
    distance = great_circle(depo_location,destination_location).km + great_circle(destination_location,drone_location).km
    drone_info["distance"] = distance
    drones_list[idx] = drone_info

for idx, package_info in enumerate(packages_list):
    destination_location = (package_info["destination"]["latitude"],package_info["destination"]["longitude"])
    package_info["distance"] = great_circle(depo_location,destination_location).km
    packages_list[idx] = package_info

#
# Step 4: sort the drones_list based on the distances to be travelled
#    Sort the packages_list based on distance buffer
#

def by_dist(item):
    return item["distance"]
def by_buffer_dist(item):
    return item["buffer_dist"]
drones_list = sorted(drones_list,key=by_dist)

currenttime = time.time()
# print(currenttime)
for idx, package_info in enumerate(packages_list):
    time = (package_info["deadline"])
    timediff = time-currenttime
    package_info["timediff"] = timediff
    #buffer = distance that can be travelled - distance to be travelled
    #print(package_info["timediff"])
    #print(
    #datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    #)
    package_info["buffer_dist"] = timediff * 50 / 3600 - package_info["distance"]
    packages_list[idx] = package_info
packages_list = sorted(packages_list,key=by_buffer_dist)

#print("----------")
#print("drone distances:")
#for elem in drones_list:
#    print(elem["distance"])
#print("----------")
#print("package buffer distances:")
#for elem in packages_list:
#    print(elem["buffer_dist"])
#print("----------")

#
# Step 5: Now start assigning the packages to the drones taking time into account
#
#(drone distance + package distance)/speed < deadline - present_time
i = j = 0;
assignments = []
unassignedPackageIds = []
while True :
    print( "\n", i, ":", j )
    drone_info = drones_list[i]
    package_info = packages_list[j]
    print("Drone_distance:", drone_info["distance"])
    print("Package buffer_dist:", package_info["buffer_dist"])
    print("Package_distance:", package_info["distance"])
    print("Package_time:", package_info["timediff"])
    # if package buffer is less than drone distance it goes into unassigned
    # this tries to optimize the allocation
    if package_info["buffer_dist"] >= drone_info["distance"]:
        print("package: ", package_info["packageId"], " assigned to droneId:", drone_info["droneId"])
        assignments.append({"droneId": drone_info["droneId"], "packageId": package_info["packageId"]})
        i+=1
        j+=1
    else:
        print("\nPackage not assigned\n")
        unassignedPackageIds.append(package_info["packageId"])
        j+=1
    if i==len(drones_list):
        # end of drones that can be assigned - add rest of packages
        print("rest of packages go into unassigned bucket")
        while j< len(packages_list):
            package_info = packages_list[j]
            unassignedPackageIds.append(package_info["packageId"])
            j+=1
        break
    if j==len(packages_list):
        break # end of packages to be assigned - exit and print the results
print("assignments:", assignments)
print("unassignedPackageIds:", unassignedPackageIds)
