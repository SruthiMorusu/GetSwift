## GetSwift

Drone delivery system to dispatch packages

## Analysis and Implementation:
Python is used to assign packages to the drones so that more number of packages are delivered in short time.

Get/Drones returns two types of drones one with packages assigned and the other without packages. Get/Packages returns the unassigned packages

Drones List is made based on the distance each drone has to travel to deliver the package

Packages List is made based on the distance it has to reach it's destination

Distance buffer is calculated for the packages by taking difference of distance that can be travelled by the package by the time deadline assuming drone can go 50 kms per hour and distance to reach destination

Drones List is sorted based on distance and Packages List is sorted based on distance buffer

Assigning the packages to the drones taking time into account

if package buffer is less than drone distance the package goes into unassigned or less assign the package to the drone
    # this tries to optimize the allocation

This is done to maximize the number of assignments 

## Solution 
If we need to handle dispatching thousands of jobs per second to thousands of drivers, It's better to use low level language to improve processing time.

Parallel processing can be done to process drone info and package info for huge data.
