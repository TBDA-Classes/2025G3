import { useEffect, useState } from "react";
import axios from "axios";

interface Unit {
    id_var: number;
    date: string;
    value: string;
}

export default function Example(){
    const [data, setData] = useState<Unit[]>([]);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        axios
            .get<Unit[]>("http://localhost:8000/api?limit=10")
            .then((res) => setData(res.data))
            .catch((err) => setError(err.message));
    },[]);

    if (error) return <p style={{color:"red"}}> Error: {error}</p>;


    return (
        <div>
            <h2>Latest 10 runs of machine</h2>
            {data.length === 0 ? (
                <p>Loading...</p>
            ) : (
                <>
                <ul>
                    {data.map((unit) => (
                        <li key={unit.id_var}>{unit.date} - {unit.value}</li>
                    ))}
                </ul>
                </>
            )}
        </div>
    )
}

