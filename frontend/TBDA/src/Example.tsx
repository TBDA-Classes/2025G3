import { useEffect, useState } from "react";
import axios from "axios";

import "./style.css"

interface Run {
    date: string;
    value: string;
}

interface Zones {
    values: boolean[];
}

export default function Example(){
    const [run, setRun] = useState<Run | null>(null);
    const [zones, setZones] = useState<Zones | null>(null);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        const fetchRunData = async () => {
            try {
                const [runRes, zonesRes] = await Promise.all([
                    axios.get('http://localhost:8000/api/recent_run'),
                    axios.get('http://localhost:8000/api/active_zones'),
                ]);
                setRun(runRes.data);


                setZones({
                    values: zonesRes.data.zones.map((v: number) => Boolean(v))
                    });
            } catch (error) {
                setError(String(error))
                console.error('Error fetching run data: ', error);
            }
        };

        fetchRunData();
    },[]);

    if (error) return <p style={{color:"red"}}> Error: {error}</p>;


    return (
        <div>
            <h2>Current Run</h2>
            {!run ? (
                <p>Loading...</p>
            ) : (
                <>
                <div className="run-container">
                    <h3>{run.date}: </h3>
                    <p>{run.value}</p>
                </div> 
                <div className="zones-container">
                    Active Zones:{" "}
                    {zones?.values.map((val, i) =>
                        <div 
                            key={i} 
                            className={`zone-box ${val ? "active" : "inactive"}`}
                            title={`Zone ${i+1}: ${val ? "Active": "Inactive"}`}>
                            Zone {i + 1}
                        </div>
                    )}   
                </div>
                </>
            )}
        </div>
    )

}

