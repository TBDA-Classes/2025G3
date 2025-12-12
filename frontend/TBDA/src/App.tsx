import { useState, useEffect, type JSX } from "react";
import SidePanel from "./SidePanel";
import InformationBox from "./InformationBox";
import FilterPanel from "./FilterPanel";
import AlertPanel from "./AlertPanel";
import axios from "axios";

import HourlyChart from "./HourlyChart";

export interface CriticalAlerts {
    log_time: string;
    event_description: string;
  }

function App(): JSX.Element {



  interface DailyTmp {
    log_time: string;
    avg_temp: number;
  }

  interface DailySpin {
    log_time: string;
    avg_spindle: number;
  }


  interface HourlyData {
  log_hour: string;
  avg_temp: number | null;
  avg_spindle: number | null;
  power_kW: number | null;
}

interface DailyPower {
    date: string;
    avg_power_kW: number;
}

  const [selectedDate, setSelectedDate] = useState<string>("");
  const [dailyTemp, setDailyTemp] = useState<DailyTmp | null>(null);
  const [dailySpindle, setDailySpindle] = useState<DailySpin | null>(null);
  const [dailyAlerts, setDailyAlerts] = useState<number | null>(null);
  const [criticalAlerts, setCriticalAlerts] = useState<CriticalAlerts[]>([])
  const [graphData, setGraphData] = useState<HourlyData[]>([]);
  const [dailyPowerData, setDailyPowerData] = useState<DailyPower | null>(null);


  useEffect(() => {
    const fetchDailyTemp = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/daily_temp_avg', {
          params: { date: selectedDate }
        });

        const data = Array.isArray(res.data) ? res.data[0] : res.data;

        setDailyTemp(data);

      } catch(err) {
        console.error("Error fetching daily temperature", err);
      }
    };

    const fetchDailySpindle = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/daily_spindle_avg', {
          params: {date: selectedDate}
        });
        const data = Array.isArray(res.data) ? res.data[0] : res.data;

        setDailySpindle(data);

      } catch(err) {
        console.error("Error fetching daily spindle load", err);
      }
    };

    const fetchDailyAlerts = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/number_daily_alerts', {
          params: { date: selectedDate }
        });


        setDailyAlerts(res.data.num_alarms);

      } catch(err) {
        console.error("Error fetching daily alerts", err);
      }
    };

    const fetchCriticalAlerts = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/critical_alerts', {
          params: { date: selectedDate }
        });

        const data = Array.isArray(res.data) ? res.data : [];

        setCriticalAlerts(data);

      } catch(err) {
        console.error("Error fetching daily alerts", err);
      }
    };


    const fetchGraphData = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/hourly_combined', {
          params: { date: selectedDate }
        });
        const data = Array.isArray(res.data) ? res.data : [];
        setGraphData(data);
      } catch(err) {
        console.error("Error fetching graph data", err);
      }
    };

    const fetchDailyPower = async () => {
        try {
          const res = await axios.get('http://localhost:8000/api/energy_usage/daily', {
            params: { date: selectedDate }
          });
          setDailyPowerData(res.data);
        } catch(err) {
          console.error("Error fetching daily power", err);
        }
      };


    if (selectedDate) {
      fetchDailyTemp();
      fetchDailySpindle();
      fetchDailyAlerts();
      fetchCriticalAlerts();
      fetchGraphData();
      fetchDailyPower();
    }
  }, [selectedDate])

  return (
    <div className="main">
      <div>
        <SidePanel/>
      </div>
      <div className="main-panel">
        <FilterPanel selectedDate={selectedDate} setSelectedDate={setSelectedDate}/>
        <div className="information-boxes-container">
          <InformationBox dataName="Average Daily Temperature" dataValue={dailyTemp?.avg_temp ? `${dailyTemp.avg_temp} °C` : "NaN"}/>
          <InformationBox dataName="Average Daily Spindle Load" dataValue={dailySpindle?.avg_spindle ? `${dailySpindle.avg_spindle} %` : "NaN"}/>
          <InformationBox dataName="Daily Alerts" dataValue={dailyAlerts ?? "NaN"}/>
          <InformationBox 
              dataName="Average Daily Power" 
              dataValue={dailyPowerData?.avg_power_kW ? `${dailyPowerData.avg_power_kW} kW` : "NaN"} 
          />
         </div>
        <div>
          <div className="sub-main-panel">
            <div className="graphs">
               {selectedDate && graphData.length > 0 ? (
                  <HourlyChart data={graphData} />
               ) : (
                 <div style={{color:"white"}}>Select a date to view graph</div>
               )}
            </div>
            <AlertPanel alerts={criticalAlerts}/>
          </div>
        </div>
      </div>
    </div>

  );
}

export default App;
