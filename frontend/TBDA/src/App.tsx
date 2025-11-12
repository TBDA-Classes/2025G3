import { useState, useEffect, type JSX } from "react";
import SidePanel from "./SidePanel";
import InformationBox from "./InformationBox";
import FilterPanel from "./FilterPanel";
import AlertPanel from "./AlertPanel";
import axios from "axios";

function App(): JSX.Element {

  /* const informationView = (): void => {
    setInformation("General")
  }; */

  //const [information, setInformation] = useState<String>("home");


  interface DailyTmp {
    log_time: string;
    avg_temp: number;
  }

  interface DailySpin {
    log_time: string;
    avg_spindle: number;
  }

  const testData = {dataName: "Energy", dataValue: "321 kWh"}

  const [selectedDate, setSelectedDate] = useState<string>("");
  const [dailyTemp, setDailyTemp] = useState<DailyTmp | null>(null);
  const [dailySpindle, setDailySpindle] = useState<DailySpin | null>(null);

  useEffect(() => {
    const fetchDailyTemp = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/daily_temp_avg', {
          params: { date: selectedDate }
        });

        const data = Array.isArray(res.data) ? res.data[0] : res.data;

        setDailyTemp(data);
        console.log("setDailyTemp", dailyTemp);

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
        console.log("dailySpindle", dailySpindle);

      } catch(err) {
        console.error("Error fetching daily spindle load", err);
      }
    };

    if (selectedDate) {
      fetchDailyTemp();
      fetchDailySpindle();
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
          <InformationBox dataName="Average Daily Temperature" dataValue={dailyTemp?.avg_temp ?? "NaN"}/>
          <InformationBox dataName="Average Daily Spindle Load" dataValue={dailySpindle?.avg_spindle ?? "NaN"}/>
          {/*<InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
         */}</div>
        <div>
          <AlertPanel/>
        </div>
      </div>
    </div>

  );
}

export default App;
