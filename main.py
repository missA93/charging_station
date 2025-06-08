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
while step < 2000:
    traci_connection.simulationStep()
    for vehicle_id in traci_connection.vehicle.getIDList():
        vehicle_battery_capcity = float(
            traci_connection.vehicle.getParameter(vehicle_id, "device.battery.capacity")
        )
        if np.random.choice([0, 1], p=[0.01, 0.99]) == 0:

            traci_connection.vehicle.setParameter(
                vehicle_id,
                "device.battery.actualBatteryCapacity",
                str(vehicle_battery_capcity * 0.15),
            )
            # print(f"Lower vehicle charge level. {counter}")
        current_battery = float(
            traci_connection.vehicle.getParameter(
                vehicle_id,
                "device.battery.actualBatteryCapacity",
            )
        )
        if current_battery <= vehicle_battery_capcity * 0.15:
            if traci_connection.vehicle.getPosition(vehicle_id)[0] < -2:
                charging_cars_station_1 = (
                    traci_connection.chargingstation.getVehicleIDs("cs_0")
                )
                charging_cars_station_2 = (
                    traci_connection.chargingstation.getVehicleIDs("cs_1")
                )
                selected_station_id = (
                    "cs_0"
                    if len(charging_cars_station_1) < len(charging_cars_station_2)
                    else "cs_1"
                )
                if selected_station_id == "cs_0":
                    traci_connection.vehicle.setRoute(vehicle_id, ["E0", "E1", "E2", "E4"])
                else:
                    traci_connection.vehicle.setRoute(vehicle_id, ["E0", "E6", "E7", "E8"])
                    
                traci_connection.vehicle.setChargingStationStop(
                    vehicle_id,
                    selected_station_id,
                    duration=600,
                    until=1000,
                )

            charging_cars_ids = traci_connection.chargingstation.getVehicleIDs("cs_0")
            charging_cars_ids = (
                charging_cars_ids
                + traci_connection.chargingstation.getVehicleIDs("cs_1")
            )

            for v_id in charging_cars_ids:

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
                if current_battery >= vehicle_battery_capcity * 0.8:
                    print(f"vehicle with id {v_id} was charged.")
                    traci_connection.vehicle.resume(v_id)
            # print(f"must recharge.{counter}")
    step += 1
