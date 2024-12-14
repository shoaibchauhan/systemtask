import psutil
import time
import requests
import socket
from datetime import datetime

API_ENDPOINT = "http://127.0.0.1:8000/api/process-data/"

def get_process_details():
    processes = []
    print("Fetching processes...")
    for process in psutil.process_iter(attrs=["pid", "name", "username", "create_time"]):
        try:
            process_info = process.info
            process_info["create_time"] = datetime.fromtimestamp(process_info["create_time"]).isoformat()
            processes.append({
                "name": process_info["name"],
                "username": process_info["username"],
                "pid": process_info["pid"],
                "create_time": process_info["create_time"]
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print(f"Found {len(processes)} processes.")
    return processes

def send_data_to_server(process_data):
    try:
        system_name = socket.gethostname() 
        payload = {
            "system_name": system_name,
            "processes": process_data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Sending data to server: {payload}")
        response = requests.post(API_ENDPOINT, json=payload)
        response.raise_for_status()  
        print(f"Data sent successfully: {response.status_code}")  
        print("Process data sent successfully!\n") 
    except requests.RequestException as e:
        print(f"Error sending data to server: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        print("Starting process monitoring...") 
        while True:
            try:
                process_data = get_process_details()
                if process_data:
                    send_data_to_server(process_data)
                else:
                    print("No process data to send.")
            except Exception as e:
                print(f"Error in main loop: {e}")
            time.sleep(5)  
    except Exception as e:
        print(f"Unexpected error in the script: {e}")
