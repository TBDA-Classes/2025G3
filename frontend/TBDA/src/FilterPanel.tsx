import { useState } from "react";
import "./style.css";

export default function FilterPanel() {
  const [selectedDate, setSelectedDate] = useState<string>("");

  return (
    <div className="filter-panel">
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
      />
      <button>Apply</button>
    </div>
  );
}
