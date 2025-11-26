# Frontend Overview
This section describes the frontend architecture, mockups, and components

---

## UX Draft (presented on 3/11)
### User and Goals
Users
- Machine operators and engineers
- Analysts monitoring performance and energy use

Their goals:
- Identify when the machine is operating, idle, or in error
- Visualize KPIs like energy per program, cycle duration, spindle load
- See alerts or anomalies in real time

### Key Information to show
- **Machine State**: operating / standby / emergency / stopped
- **Program Info**: name, progress, tool used
- **Performance Metrics**: spindle load, temperature, feedrate, operation time
- **Alerts**: overheat, emergency, vibration
- **Energy**: estimated energy per program

### UX Draft
![UI overview](../assets/UX_Mockup_1.png)

[Updated FIGMA draft](https://www.figma.com/make/6YPQxr4f99iAVQY5Oej8Y4/CNC-Analytics-Dashboard-Design?fullscreen=1)

### Feedback from the professor
We don’t have access to current data so we won’t be able to show that. More interesting is to be able to go back in time and see which programs and data points during certain dates etc.

### Next Steps and Goals
We’re now beginning the development of the website. Its main purpose is to let users select a past date and view a dashboard displaying machine-operation data for that specific day. For the time being, the daily data we intend to present includes:
- Average daily temperature
- Average daily spindle load
- Energy consumed
- Graphs showing temperature, spindle load and energy consumption throughout the day
- Alerts (if applicable)

## First draft on website (presented 24/11)
### Website Draft
![Website overview](../assets/Website_Draft_1.png)

### Progress
We have successfully established a connection between the client and the server which is connected to the database. On the dashboard, we have currently implemented the following:
- Average daily temperature
- Average daily spinde load

### Next Steps
Our immediate focus is to include alerts on the dashboard. Following this, we will implement the energy-consumption metric. If time and resources permit, we will proceed with developing the visualization graphs for these measurements.

