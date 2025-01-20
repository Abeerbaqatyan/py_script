from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)



connection_string = '127.0.0.1:14551'
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)




def goto_position_target_local_ned(north, east, down):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       
        0, 0,    
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
        0b0000111111111000, #locayion speed 
        north, east, down, 
        0, 0, 0, 
        0, 0, 0, 
        0, 0)
    vehicle.send_mavlink(msg)       


while not vehicle.is_armable:
    print(' Waiting for vehicle to initialise...')
    time.sleep(1)


print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name) 
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name=='GUIDED':  
    print(" Waiting for mode change ...")
    time.sleep(1)


arm_and_takeoff(2)
time.sleep(1)

print("Set default/target airspeed to 3")
vehicle.airspeed = 200

time.sleep(1)


print("SQUARE path using SET_POSITION_TARGET_LOCAL_NED and position parameters")
DURATION = 10 #Set duration for each segment.

print("North 50m, East 0m, 10m altitude for %s seconds" % DURATION)
goto_position_target_local_ned(10,0,-10)
print("Point ROI at current location (home position)") 
time.sleep(5)

print("North 50m, East 50m, 10m altitude")
goto_position_target_local_ned(10,10,-10)
time.sleep(5)

print("Point ROI at current location")

print("North 0m, East 50m, 10m altitude")
goto_position_target_local_ned(0,10,-10)
time.sleep(5)

print("North 0m, East 0m, 10m altitude")
goto_position_target_local_ned(0,0,-10)
time.sleep(5)







