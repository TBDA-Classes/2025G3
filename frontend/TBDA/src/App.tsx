import { useState, type JSX } from "react";
import Example from "./Example";
import ExampleChart from "./ExampleChart";




function App(): JSX.Element {

  /* const informationView = (): void => {
    setInformation("General")
  }; */

  const [information, setInformation] = useState<String>("home");

  const renderContect = (): JSX.Element => {
    switch (information) {
      case "current":
        return <Example/>;
      //case "advanced":
        //return <Advanced/>
      default:
        return (
        <>
          <h1>Dashboard</h1>
          <div style={{ width: "100%", display: "flex"}}>
            <div style={{flex:1}}>
              <h2>Overview of machine health</h2>
                <ExampleChart/>
                <ExampleChart/>
              </div>  
            <div style={{flex:1, margin:"1rem"}}>
              <h2>Overview of machine stats</h2>
                <ExampleChart/>
                <ExampleChart/>
              </div>
          </div>
           
          
        </>
        )
    }
  }

  return (
    <div style={{ padding: "2rem" }}>
    <div>
      <button onClick={() => setInformation("home")}>Home</button>
      <button onClick={() => setInformation("current")}>Current</button>
      <button onClick={() => setInformation("advanced")}>Advanced Information</button>
    </div>
      {renderContect()}      
    </div>

  );
}

export default App;
