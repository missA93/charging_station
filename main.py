import pickle
import traci
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

sumo_port = 8813
step = 0
counter = 0
charging_vehicles = []
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
                "device.battery.chargeLevel",
                str(vehicle_battery_capcity * 0.15),
            )
            # print(f"Lower vehicle charge level. {counter}")
        current_battery = float(
            traci_connection.vehicle.getParameter(
                vehicle_id,
                "device.battery.chargeLevel",
            )
        )
        if current_battery <= vehicle_battery_capcity * 0.15:
            counter += 1
            if traci_connection.vehicle.getPosition(vehicle_id)[0] < -2:
                traci_connection.vehicle.setRoute(vehicle_id, ["E0", "E1", "E2", "E4"])
                traci_connection.vehicle.setParkingAreaStop(
                    vehicle_id,
                    "pa_0",
                    duration=600,
                    until=50,
                )
                charging_vehicles.append(vehicle_id)
            if len(charging_vehicles) > 0:
                for v_id in charging_vehicles:
                    current_battery = float(
                        traci_connection.vehicle.getParameter(
                            v_id,
                            "device.battery.chargeLevel",
                        )
                    )
                    vehicle_battery_capcity = float(
                        traci_connection.vehicle.getParameter(
                            v_id, "device.battery.capacity"
                        )
                    )
                    print(
                        f"battery:{current_battery}, capacity: {vehicle_battery_capcity},Vehicle: {v_id}"
                    )
                    if current_battery >= vehicle_battery_capcity * 0.9:
                        traci.vehicle.resume(v_id)
                        charging_vehicles.remove(v_id)
            # print(f"must recharge.{counter}")
    step += 1
