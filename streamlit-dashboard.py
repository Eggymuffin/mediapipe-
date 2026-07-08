# The reason we resort to crude file-on-disk (i.e. "state.json") syncing
# is because of the clash between paho-mqtt's `on_mesage()` background
# thread and streamlit's thread. These two do not share context and it
# complicates code. For a demo, we just use file-on-disk syncing
#
# CLI: streamlit run streamlit-aiot-dashboard.py
#
import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AIoT Dashboard")

st.title("🏠 Home Automation Dashboard")

st_autorefresh(interval=500, key="refresh")

try:
    with open("state.json") as f:
        state = json.load(f)

except:
    state = {}


DEVICES = {

    "strath/home/light":
        ("💡 Light", "OFF", "ON"),

    "strath/home/door":
        ("🚪 Door", "LOCKED", "UNLOCKED"),

    "strath/home/alarm":
        ("🚨 Alarm", "DEACTIVATED", "ACTIVATED"),
}


for topic, (title, off, on) in DEVICES.items():

    col1, col2 = st.columns([2,1])

    value = state.get(topic, False)

    with col1:
        st.subheader(title)

    with col2:

        label = on if value else off

        if st.button(
            label,
            key=topic,
            type="primary" if value else "secondary",
        ):
            
            # toggle state
            state[topic] = not value

            # save to disk
            with open("state.json", "w") as f:
                json.dump(state, f)

            # redraw the page
            st.rerun()