import { useState, type JSX } from "react";
import SidePanel from "./SidePanel";
import InformationBox from "./InformationBox";
import FilterPanel from "./FilterPanel";
import AlertPanel from "./AlertPanel";

function App(): JSX.Element {

  /* const informationView = (): void => {
    setInformation("General")
  }; */

  //const [information, setInformation] = useState<String>("home");


  const testData = {dataName: "Energy", dataValue: "321 kWh"}

  return (
    <div className="main">
      <div>
        <SidePanel/>
      </div>
      <div className="main-panel">
        <FilterPanel/>
        <div className="information-boxes-container">
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
          <InformationBox dataName={testData.dataName} dataValue={testData.dataValue}/>
        </div>
        <div>
          <AlertPanel/>
        </div>
      </div>
    </div>

  );
}

export default App;
