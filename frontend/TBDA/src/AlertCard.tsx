
import "./style.css"
import type { CriticalAlerts } from "./App";


interface AlertCardProps {
    alert: CriticalAlerts
}

export default function AlertCard({alert}: AlertCardProps){


    return (
        <div className="alert-card">
            <p>{alert.log_time}</p>
            <h3>{alert.event_description}</h3>
        </div>
    )

}

