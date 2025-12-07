
import "./style.css"

interface InformationData {
    dataName: string;
    dataValue: string | number;
}



export default function InformationBox({dataName, dataValue}: InformationData){
    
    return (
        <div className="information-box">
            <h5>{dataName}</h5>
            <h1>{dataValue}</h1>
        </div>
    )

}

