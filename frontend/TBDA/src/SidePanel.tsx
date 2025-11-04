import { useEffect, useState } from "react";
import axios from "axios";

import "./style.css"


export default function SidePanel(){

    useEffect(() => {
        
    },[]);

    return (
        <div className="sidepanel">
            <button>Dashboard</button>
            <button>Compare Machines</button>
            <button>Download Report</button>
        </div>
    )

}

