import { useState } from "react";
import "./style.css";

interface FilterPanelProps {
  selectedDate: string;
  setSelectedDate: (date: string) => void;
}

export default function FilterPanel({ selectedDate, setSelectedDate}: FilterPanelProps) {

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
