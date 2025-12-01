
import type { CriticalAlerts } from "./App";

import "./style.css"
import AlertCard from "./AlertCard";

interface AlertPanelProps {
  alerts: CriticalAlerts[];
}

export default function AlertPanel({alerts}: AlertPanelProps){

  console.log(alerts)

    return (
          <div className="alert-panel">
            <h1>Critical Alerts</h1>
                {alerts.length === 0 ? (
                  <p>No Critical alerts for this date.</p>
                ) : (
                  alerts.map((alertItem, index) => (
                    <AlertCard key={index} alert={alertItem}/>
                  ))
                )}
        </div>
    )

}

