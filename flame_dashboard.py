import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_icon="🔥", page_title="Flame Dashboard", layout="wide")
st.title("🔥Flame-resistant barrier in normal air\n")
df = pd.read_excel("Dashboard_Data.xlsx")

st.sidebar.title("User control panel")
material = st.sidebar.selectbox("Select the material", df["Material"].unique())
mat_row = df[df["Material"] == material].iloc[0]


o2_min, o2_max = sorted(
    [float(mat_row["Initial_O2"]), float(mat_row["Final_O2"])]
)
fan_min, fan_max = sorted([
    float(mat_row["Ignition_Fan_Speed.Pot"]),
    float(mat_row["Extinction_Fan_Speed.Pot"]),
])


o2_range = st.sidebar.slider(
    "O2 percentage (Initial - Final)",
    0.0,
    25.0,
    (o2_min, o2_max),
    step=0.1,
)
fan_range = st.sidebar.slider(
    "Fan speed (Initial - Final)", 0.0, 10.0, (fan_min, fan_max), step=0.1
)


current_o2 = o2_range[1]
current_fan = fan_range[1]

col1, col2 = st.columns(2)
if (
    current_o2 >= mat_row["Initial_O2"]
    and current_fan < mat_row["Extinction_Fan_Speed.Pot"]
):
  level, color = 100, "red"
  with col2:
    st.error(f"🚨 **HIGH FIRE RISK** {mat_row['Fire_Status']}")
    st.warning(f"**(Safety Action):** {mat_row['Physics_Action']}")
    st.info(
        "💡Higher the fan speed to:"
        f" **{mat_row['Extinction_Fan_Speed.Pot']}** or lower the O2"
        " percentage to lower than:"
        f" {mat_row['Initial_O2']}% to prevent the spread of flame for"
        f" material {material}."
    )
else:
  level, color = 20, "green"
  with col2:
    st.success(f"✅ **SAFE CONDITION**")
    st.info(f"💡 {mat_row['Fire_Status']}")

with col1:
  fig = px.bar(
      x=[material],
      y=[level],
      range_y=[0, 110],
      labels={"x": "Material", "y": "Fire Intensity"},
  )
  fig.update_traces(marker_color=color, width=0.3)
  st.plotly_chart(fig)

