import pickle
import traci
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

sumo_port = 8813
step = 0
counter = 0
traci_connection = traci.connect(port=sumo_port)
while step < 600:
    traci_connection.simulationStep()
    for vehicle_id in traci_connection.vehicle.getIDList():
        vehicle_battery_capcity = float(
            traci_connection.vehicle.getParameter(vehicle_id, "device.battery.capacity")
        )
        if np.random.choice([0, 1], p=[0.01, 0.99]) == 0:

            traci_connection.vehicle.setParameter(
                vehicle_id,
                "device.battery.actualBatteryCapacity",
                str(vehicle_battery_capcity * 0.2),
            )
            # print(f"Lower vehicle charge level. {counter}")
            # counter += 1
        current_battery = float(
            traci_connection.vehicle.getParameter(
                vehicle_id,
                "device.battery.actualBatteryCapacity",
            )
        )
        if current_battery <= vehicle_battery_capcity:
            print("must recharge.")
    step += 1
