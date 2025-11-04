import { useEffect, useState } from "react";
import axios from "axios";

import "./style.css"

interface SidePanelData {
    dataName: string;
    dataValue: string;
}



export default function InformationBox({dataName, dataValue}: SidePanelData){
    
    return (
        <div className="information-box">
            <h5>{dataName}</h5>
            <h1>{dataValue}</h1>
        </div>
    )

}

