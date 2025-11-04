import { useEffect, useState } from "react";
import axios from "axios";

import "./style.css"



export default function FilterPanel(){
    
    return (
        <div className="filter-panel">
            <input type="text" />
            <input type="text" />
            <input type="text" />
            <button>Apply</button>
        </div>
    )

}

