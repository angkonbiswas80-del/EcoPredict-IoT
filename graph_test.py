import sqlite3
import pandas as pd
import plotly.express as px

def show_graph():
    
    conn = sqlite3.connect('cold_chain.db')
    query = "SELECT timestamp, temperature FROM shipment_data"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("No data found in database!")
        return


    fig = px.line(df, x='timestamp', y='temperature', 
                  title='EcoTrack: Real-time Temperature Monitoring',
                  labels={'timestamp': 'Time', 'temperature': 'Temperature (°C)'},
                  markers=True)


    fig.add_hline(y=8, line_dash="dot", line_color="red", annotation_text="Upper Limit (8°C)")
    fig.add_hline(y=2, line_dash="dot", line_color="blue", annotation_text="Lower Limit (2°C)")

    
    fig.show()

if __name__ == "__main__":
    show_graph()