import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# 🔽 Ordnerpfad mit den CSV-Dateien
folder_path = r"E:\Messdaten"

# 🔽 Funktion: eine CSV-Datei laden und vorbereiten
def load_sensor_data(file_path):
    df = pd.read_csv(file_path, sep=",")
    df["Temperatur"] = df["Temperatur"].str.replace(",", ".").astype(float)
    df["Zeitstempel"] = pd.to_datetime(df["Zeitstempel"], format="%d.%m.%Y %H:%M:%S")
    return df

# 🔽 Liste mit Dash-Komponenten für jede Datei aufbauen
graphs = []

# 🔽 Alle .csv-Dateien im Ordner durchgehen
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".csv"):
        full_path = os.path.join(folder_path, filename)
        df = load_sensor_data(full_path)

        # 🔽 Sensorname z. B. "Messfühler_01"
        sensor_name = os.path.splitext(filename)[0]

        # 🔽 Diagramm für diesen Sensor erstellen
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Zeitstempel"], y=df["Temperatur"],
            name="Temperatur (°C)", yaxis="y1"
        ))

        fig.add_trace(go.Scatter(
            x=df["Zeitstempel"], y=df["Luftfeuchtigkeit"],
            name="Luftfeuchtigkeit (%)", yaxis="y2"
        ))

        fig.update_layout(
            title=f"{sensor_name} – Temperatur & Luftfeuchtigkeit",
            xaxis_title="Zeit",
            yaxis=dict(title="Temperatur (°C)", side="left"),
            yaxis2=dict(
                title="Luftfeuchtigkeit (%)",
                overlaying="y",
                side="right"
            ),
            margin=dict(l=60, r=60, t=50, b=50)
        )

        # 🔽 Abschnitt in der App hinzufügen
        graphs.append(
            html.Div([
                html.H3(sensor_name),
                dcc.Graph(figure=fig)
            ])
        )

# 🔽 Dash-App starten
app = Dash(__name__)

# 🔽 Layout enthält alle Grafen untereinander
app.layout = html.Div([
    html.H1("Alle Messfühler"),
    *graphs  # Entpackt die Liste in mehrere Dash-Komponenten
])

if __name__ == "__main__":
    app.run(debug=True)
