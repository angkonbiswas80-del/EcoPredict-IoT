import sqlite3
import random
import time
from datetime import datetime

def log_to_db(shipment_id, temp, humidity):
    conn = sqlite3.connect('cold_chain.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shipment_data (shipment_id, temperature, humidity)
        VALUES (?, ?, ?)
    ''', (shipment_id, temp, humidity))
    conn.commit()
    conn.close()

def start_monitoring(shipment_id):
    print(f"--- Monitoring Started for {shipment_id} ---")
    
    try:
        while True:
            
            current_temp = round(random.uniform(1.5, 9.0), 2)
            current_humidity = round(random.uniform(40, 60), 2)
            
            
            status = "NORMAL"
            if current_temp > 8.0:
                status = "⚠️ CRITICAL: TOO HOT"
            elif current_temp < 2.0:
                status = "❄️ CRITICAL: TOO COLD"
            
            
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Temp: {current_temp}°C | Status: {status}")
            
            
            log_to_db(shipment_id, current_temp, current_humidity)
            
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


if __name__ == "__main__":
    start_monitoring("VACCINE-BATCH-101")