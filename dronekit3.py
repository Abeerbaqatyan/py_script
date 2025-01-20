from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative
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

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print ("Get some vehicle attribute values:")
print (" GPS: %s" % vehicle.gps_0 )
print (" Battery: %s" % vehicle.battery)
print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
print (" Is Armable?: %s" % vehicle.is_armable)
print (" System status: %s" % vehicle.system_status.state)
print (" Mode: %s" % vehicle.mode.name )   # settable
print (" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print (" relative altitude): %s" % vehicle.location.global_relative_frame.alt)

# while not vehicle.home_location:
#     cmds = vehicle.commands
#     cmds.download()
#     cmds.wait_ready()
#     if not vehicle.home_location:
#         print(" Waiting for home location ...")
# # We have a home location, so print it!        
# print("\n Home location: %s" % vehicle.home_location)


# print("\nSet new home location")
# # Home location must be within 50km of EKF home location (or setting will fail silently)
# # In this case, just set value to current location with an easily recognisable altitude (222)
# my_location_alt = vehicle.location.global_frame
# my_location_alt.alt = 222.0
# vehicle.home_location = my_location_alt
# print(" New Home Location (from attribute - altitude should be 222): %s" % vehicle.home_location)


# #Confirm current value on vehicle by re-downloading commands
# cmds = vehicle.commands
# cmds.download()
# cmds.wait_ready()
# print(" New Home Location (from vehicle - altitude should be 222): %s" % vehicle.home_location)


while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)
    # If required, you can provide additional information about initialisation
    # using `vehicle.gps_0.fix_type` and `vehicle.mode.name`.


print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name) 
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name=='GUIDED':  #Wait until mode has changed
    print(" Waiting for mode change ...")
    time.sleep(1)


arm_and_takeoff(1)

print("Set default/target airspeed to 3")
vehicle.airspeed = 100

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(-.5 ,1., 2)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(1)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(-.5 , 1., 2)
vehicle.simple_goto(point2, groundspeed=30)

# sleep so we can see the change in map
time.sleep(1)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")





# print(" GPS: %s" % vehicle.gps_0)
# print(" Battery: %s" % vehicle.battery)
print(" Velocity: %s" % vehicle.velocity)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Attitude: %s" % vehicle.attitude)
# print(" Mode: %s" % vehicle.mode.name)    # settable
print(" Armed: %s" % vehicle.armed)  
print(" Heading: %s" % vehicle.heading)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator