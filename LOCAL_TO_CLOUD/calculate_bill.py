"""

This script reads SESSION_LOG_<date>.json file and calculates total bill


@author : Taizun J 
@date   : 23:06:20 Aug 20 2025

"""



# import json
# from datetime import datetime, timezone

# def calculate_total_energy(log_file_path):
#     """
#     Calculates the total energy consumed based on voltage and current data from a JSON log file.

#     The function reads a log file where each line is a JSON object containing a timestamp,
#     'present_Voltage', and 'present_Current'. It calculates the energy consumed between
#     consecutive valid data points and sums them up.

#     The energy for each interval is calculated using the trapezoidal rule, which provides a
#     more accurate approximation of the integral of power over time:
#     Energy_interval = (Power_1 + Power_2) / 2 * time_difference_in_seconds

#     Args:
#         log_file_path (str): The path to the log file.

#     Returns:
#         tuple: A tuple containing the total energy in Watt-seconds (Joules)
#                and Watt-hours.
#     """
#     valid_readings = []
#     try:
#         with open(log_file_path, 'r') as f:
#             for line in f:
#                 try:
#                     log_entry = json.loads(line)
                    
#                     # Ensure all required keys exist and are not null
#                     timestamp_str = log_entry.get("timestamp")
#                     voltage = log_entry.get("present_Voltage")
#                     current = log_entry.get("present_Current")

#                     if timestamp_str and voltage is not None and current is not None:
#                         # Parse the timestamp string into a timezone-aware datetime object
#                         # The 'Z' indicates UTC timezone.
#                         timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
#                         valid_readings.append({
#                             "timestamp": timestamp,
#                             "voltage": float(voltage),
#                             "current": float(current)
#                         })
#                 except (json.JSONDecodeError, TypeError, ValueError) as e:
#                     print(f"Skipping malformed line: {line.strip()} - Error: {e}")
#                     continue
#     except FileNotFoundError:
#         print(f"Error: The file '{log_file_path}' was not found.")
#         return 0, 0

#     # Sort readings by timestamp just in case the log file is not ordered
#     valid_readings.sort(key=lambda x: x['timestamp'])

#     if len(valid_readings) < 2:
#         print("Not enough valid data points to calculate energy usage.")
#         return 0, 0

#     total_energy_ws = 0.0  # Total energy in Watt-seconds (Joules)

#     # Iterate through consecutive pairs of readings to calculate energy for each interval
#     for i in range(len(valid_readings) - 1):
#         reading1 = valid_readings[i]
#         reading2 = valid_readings[i+1]

#         # Calculate power (Watts) for each reading: Power = Voltage * Current
#         power1 = reading1["voltage"] * reading1["current"]
#         power2 = reading2["voltage"] * reading2["current"]

#         # Calculate the time difference between the two readings in seconds
#         time_diff_seconds = (reading2["timestamp"] - reading1["timestamp"]).total_seconds()

#         # If there's no time difference, we can't calculate energy for this interval
#         if time_diff_seconds <= 0:
#             continue

#         # Calculate the average power over the interval
#         average_power = (power1 + power2) / 2.0

#         # Calculate the energy for this interval (Energy = Power * Time)
#         energy_interval_ws = average_power * time_diff_seconds

#         # Add the interval energy to the total
#         total_energy_ws += energy_interval_ws
        
#     # Convert total energy from Watt-seconds to Watt-hours (1 Wh = 3600 Ws)
#     total_energy_wh = total_energy_ws / 3600.0

#     return total_energy_ws, total_energy_wh

# if __name__ == "__main__":


#     log_filename = "/Users/taizunj/Documents/Personal_Projects/EXTENDEV/ChargeSOM_LOGS/Session_Logs/SESSION_LOG_2025-08-20_23-13-13.json"
#     # --- USAGE ---
#     # Pass the path to your log file to the function.
#     energy_ws, energy_wh = calculate_total_energy(log_filename)

#     print(f"Calculation complete.")
#     print(f"Total Energy Consumed: {energy_ws:.2f} Watt-seconds (Joules)")
#     print(f"Total Energy Consumed: {energy_wh:.4f} Watt-hours")



##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################


# import json
# import sys
# from datetime import datetime, timezone

# def calculate_total_energy(log_file_path):
#     """
#     Calculates the total energy consumed based on voltage and current data from a JSON log file.

#     The function reads a log file where each line is a JSON object containing a timestamp,
#     'present_Voltage', and 'present_Current'. It calculates the energy consumed between
#     consecutive valid data points and sums them up.

#     The energy for each interval is calculated using the trapezoidal rule, which provides a
#     more accurate approximation of the integral of power over time:
#     Energy_interval = (Power_1 + Power_2) / 2 * time_difference_in_seconds

#     Args:
#         log_file_path (str): The path to the log file.

#     Returns:
#         tuple: A tuple containing the total energy in Watt-seconds (Joules)
#                and Watt-hours.
#     """
#     valid_readings = []
#     try:
#         with open(log_file_path, 'r') as f:
#             for line in f:
#                 try:
#                     log_entry = json.loads(line)
                    
#                     # Ensure all required keys exist and are not null
#                     timestamp_str = log_entry.get("timestamp")
#                     voltage = log_entry.get("present_Voltage")
#                     current = log_entry.get("present_Current")

#                     if timestamp_str and voltage is not None and current is not None:
#                         # Parse the timestamp string into a timezone-aware datetime object
#                         # The 'Z' indicates UTC timezone.
#                         timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
#                         valid_readings.append({
#                             "timestamp": timestamp,
#                             "voltage": float(voltage),
#                             "current": float(current)
#                         })
#                 except (json.JSONDecodeError, TypeError, ValueError) as e:
#                     print(f"Skipping malformed line: {line.strip()} - Error: {e}")
#                     continue
#     except FileNotFoundError:
#         print(f"Error: The file '{log_file_path}' was not found.")
#         return 0, 0
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return 0, 0

#     # Sort readings by timestamp just in case the log file is not ordered
#     valid_readings.sort(key=lambda x: x['timestamp'])

#     if len(valid_readings) < 2:
#         print("Not enough valid data points to calculate energy usage.")
#         return 0, 0

#     total_energy_ws = 0.0  # Total energy in Watt-seconds (Joules)

#     # Iterate through consecutive pairs of readings to calculate energy for each interval
#     for i in range(len(valid_readings) - 1):
#         reading1 = valid_readings[i]
#         reading2 = valid_readings[i+1]
#         # Calculate power (Watts) for each reading: Power = Voltage * Current
#         power1 = reading1["voltage"] * reading1["current"]
#         power2 = reading2["voltage"] * reading2["current"]
#         # Calculate the time difference between the two readings in seconds
#         time_diff_seconds = (reading2["timestamp"] - reading1["timestamp"]).total_seconds()

#         # If there's no time difference, we can't calculate energy for this interval
#         if time_diff_seconds <= 0:
#             continue
#         # Calculate the average power over the interval
#         average_power = (power1 + power2) / 2.0
#         # Calculate the energy for this interval (Energy = Power * Time)
#         energy_interval_ws = average_power * time_diff_seconds
#         total_energy_ws += energy_interval_ws
        
#     # Convert total energy from Watt-seconds to Watt-hours (1 Wh = 3600 Ws)
#     total_energy_wh = total_energy_ws / 3600.0

#     return total_energy_ws, total_energy_wh

# if __name__ == "__main__":
#     # Check if a command-line argument (the log file path) was provided.
#     if len(sys.argv) < 2:
#         # sys.argv[0] is the script name itself.
#         print(f"Usage: python {sys.argv[0]} <path_to_log_file>")
#         sys.exit(1) # Exit the script with an error code.

#     # The first argument after the script name is the log file path.
#     log_filename = sys.argv[1]

#     # --- USAGE ---
#     # Pass the path to your log file to the function.
#     energy_ws, energy_wh = calculate_total_energy(log_filename)

#     if energy_ws is not None and energy_wh is not None:
#         print(f"Calculation complete for file: '{log_filename}'")
#         print(f"Total Energy Consumed: {energy_wh:.4f} Watt-hours")

import json
import sys
import os
import csv
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables. 
load_dotenv()

def calculate_total_energy(log_file_path):
    """
    Calculates the total energy consumed based on voltage and current data from a JSON log file.

    The function reads a log file where each line is a JSON object containing a timestamp,
    'present_Voltage', and 'present_Current'. It calculates the energy consumed between
    consecutive valid data points and sums them up.

    The energy for each interval is calculated using the trapezoidal rule, which provides a
    more accurate approximation of the integral of power over time:
    Energy_interval = (Power_1 + Power_2) / 2 * time_difference_in_seconds

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        tuple: A tuple containing the total energy in Watt-seconds (Joules)
               and Watt-hours, or (None, None) if an error occurs.
    """
    valid_readings = []
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    
                    timestamp_str = log_entry.get("timestamp")
                    voltage = log_entry.get("present_Voltage")
                    current = log_entry.get("present_Current")

                    if timestamp_str and voltage is not None and current is not None:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        valid_readings.append({
                            "timestamp": timestamp,
                            "voltage": float(voltage),
                            "current": float(current)
                        })
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    print(f"Skipping malformed line: {line.strip()} - Error: {e}")
                    continue
    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

    valid_readings.sort(key=lambda x: x['timestamp'])

    if len(valid_readings) < 2:
        print("Not enough valid data points to calculate energy usage.")
        return 0.0, 0.0

    total_energy_ws = 0.0

    for i in range(len(valid_readings) - 1):
        reading1 = valid_readings[i]
        reading2 = valid_readings[i+1]
        
        power1 = reading1["voltage"] * reading1["current"]
        power2 = reading2["voltage"] * reading2["current"]
        
        time_diff_seconds = (reading2["timestamp"] - reading1["timestamp"]).total_seconds()

        if time_diff_seconds <= 0:
            continue
            
        average_power = (power1 + power2) / 2.0
        energy_interval_ws = average_power * time_diff_seconds
        total_energy_ws += energy_interval_ws
        
    total_energy_wh = total_energy_ws / 3600.0

    return total_energy_ws, total_energy_wh

def log_to_csv(filename, energy_wh):
    """
    Appends the filename and its calculated energy usage to a CSV file.
    Creates the file and adds a header if it doesn't exist.
    """
    csv_filename = os.getenv('ENERGY_CSV_FILE')
    # Check if the CSV file already exists to determine if we need to write a header.
    file_exists = os.path.isfile(csv_filename)
    
    try:
        # Open the file in append mode ('a'). `newline=''` prevents extra blank rows.
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # If the file is new, write the header row first.
            if not file_exists:
                writer.writerow(["Session Parameter Log File", "Energy Consumed (Wh)"])
            
            # Write the data row.
            writer.writerow([filename, f"{energy_wh:.4f}"])
        
        print(f"✔️ Results successfully logged to {csv_filename}")
        
    except IOError as e:
        print(f"Error: Could not write to CSV file '{csv_filename}'. Reason: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_log_file>")
        sys.exit(1)

    log_filepath = sys.argv[1]
    
    energy_ws, energy_wh = calculate_total_energy(log_filepath)

    # Proceed only if the calculation was successful.
    if energy_wh is not None:
        print(f"Calculation complete for file: '{os.path.basename(log_filepath)}'")
        print(f"Total Energy Consumed: {energy_wh:.4f} Watt-hours")
        
        # --- New Feature: Log the result to a CSV file ---
        log_to_csv(os.path.basename(log_filepath), energy_wh)

