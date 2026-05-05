import os
import sqlite3
import time
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import numpy as np
from sklearn.linear_model import LinearRegression

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email_alert(current_temp):
    msg = EmailMessage()
    msg.set_content(f"CRITICAL ALERT: Cold chain temperature threshold breached!\n"
                    f"Current Temperature: {current_temp}°C\n"
                    f"Status: Immediate action required to save the shipment.")
    msg['Subject'] = 'EcoTrack: Temperature Violation Alert'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(">>> SUCCESS: Alert email sent!")
    except Exception as e:
        print(f">>> ERROR: {e}")

class EcoTrackMonitor:
    def __init__(self, db_name="cold_chain.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS shipment_data 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                             temperature REAL)''')
            conn.commit()

    def log_data(self, temp):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO shipment_data (temperature) VALUES (?)", (temp,))
            conn.commit()
        print(f"[LOG] {time.strftime('%H:%M:%S')} - Recorded Temperature: {temp}°C")

    def get_all_temperatures(self):
        """Get all temperatures from database for ML."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT temperature FROM shipment_data ORDER BY id")
            rows = cursor.fetchall()
        return [row[0] for row in rows]

    def predict_next_temperature(self):
        """ML: Predict next temperature from historical data."""
        temps = self.get_all_temperatures()
        if len(temps) < 3:
            print("[ML] Not enough data to predict yet.")
            return None
        X = np.array(range(len(temps))).reshape(-1, 1)
        y = np.array(temps)
        model = LinearRegression()
        model.fit(X, y)
        next_temp = model.predict([[len(temps)]])[0]
        print(f"[ML] Predicted next temperature: {round(next_temp, 2)}°C")
        if next_temp > 8.0 or next_temp < 2.0:
            print(f"[ML] WARNING: Next temperature may breach threshold!")
        return next_temp

    def start_monitoring(self, cycles=5):
        print("\n" + "="*40)
        print(" ECOTRACK MONITORING SYSTEM ACTIVE ")
        print("="*40)
        for i in range(cycles):
            temp = round(random.uniform(1.0, 10.0), 2)
            self.log_data(temp)
            if temp > 8.0 or temp < 2.0:
                print(f"!!! CRITICAL: {temp}°C is OUTSIDE safe limits !!!")
                send_email_alert(temp)
            self.predict_next_temperature()
            time.sleep(3)
        print("="*40)
        print(" MONITORING SESSION COMPLETED ")
        print("="*40)

if __name__ == "__main__":
    monitor = EcoTrackMonitor()
    monitor.start_monitoring(cycles=5)