import os
import pickle
import random
import traci
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import xml.etree.ElementTree as xml_parser

sumo_port = 8813
step = 0
counter = 0
charging_vehicles = []
modified_vehicles = []
vehicles_log = []
traci.start(
    port=sumo_port,
    cmd=["sumo-gui", "-c", "charging_station_sumoconfig.sumocfg", "--quit-on-end"],
)
direction_flag = True
while step < 1000:
    traci.simulationStep()
    for vehicle_id in traci.vehicle.getIDList():
        if not vehicle_id in modified_vehicles:
            vehicle_battery_capcity = float(
                traci.vehicle.getParameter(vehicle_id, "device.battery.capacity")
            )
            if np.random.choice([0, 1], p=[0.08, 0.92]) == 0:

                traci.vehicle.setParameter(
                    vehicle_id,
                    "device.battery.actualBatteryCapacity",
                    str(vehicle_battery_capcity * 0.15),
                )
                # print(f"Lower vehicle charge level. {counter}")
            else:
                traci.vehicle.setParameter(
                    vehicle_id,
                    "device.battery.actualBatteryCapacity",
                    str(vehicle_battery_capcity * random.uniform(0.4, 0.9)),
                )
            modified_vehicles.append(vehicle_id)

        current_battery = float(
            traci.vehicle.getParameter(
                vehicle_id,
                "device.battery.actualBatteryCapacity",
            )
        )
        vehicles_log.append((vehicle_id, current_battery / vehicle_battery_capcity))
        if (
            current_battery <= vehicle_battery_capcity * 0.15
            and not vehicle_id in charging_vehicles
        ):
            if traci.vehicle.getPosition(vehicle_id)[0] < 55:
                try:
                    selected_station_id = "cs_0"
                    traci.vehicle.setRoute(vehicle_id, ["E3", "E6", "E7", "E8"])
                    traci.vehicle.setChargingStationStop(
                        vehicle_id,
                        selected_station_id,
                    )
                    print(
                        f"vehicle {vehicle_id} with battery level {current_battery} started charging."
                    )
                    charging_vehicles.append(vehicle_id)
                except:
                    print("error in setting routes")

            # charging_cars_ids = traci.chargingstation.getVehicleIDs("cs_0")

        for v_id in charging_vehicles:

            current_battery = float(
                traci.vehicle.getParameter(
                    v_id,
                    "device.battery.actualBatteryCapacity",
                )
            )
            vehicle_battery_capcity = float(
                traci.vehicle.getParameter(v_id, "device.battery.capacity")
            )
            # print(
            #     f"battery:{current_battery}, capacity: {vehicle_battery_capcity},Vehicle: {v_id}"
            # )

            if current_battery >= vehicle_battery_capcity * 0.2:
                print(f"vehicle with id {v_id} was charged.{current_battery}")
                traci.vehicle.resume(v_id)
                charging_vehicles.remove(v_id)
        # print(f"must recharge.{counter}")
    step += 1
traci.close()

time.sleep(3)
BATTERY_DATA_FILE = "battery_output.xml"  # مسیر خروجی داده‌های باتری
