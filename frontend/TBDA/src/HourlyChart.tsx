import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

interface HourlyChartProps {
    data: any[]; 
}

const formatXAxis = (tickItem: string) => {
    try {
      const date = new Date(tickItem);
      // Formats as HH:MM (e.g., 14:00)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
    } catch (e) {
      return tickItem;
    }
};

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ 
            backgroundColor: 'var(--secondary-bg-color)', 
            border: '1px solid var(--accent-color)', 
            borderRadius: '8px',
            padding: '10px',
            color: 'var(--text-color)'
        }}>
          <p style={{marginBottom: '5px', fontWeight: 'bold'}}>{`Time: ${formatXAxis(label)}`}</p>
          {payload.map((entry: any, index: number) => (
             <p key={index} style={{ color: entry.color, margin: 0 }}>
                {/* Dynamically display name, value and unit */}
                {`${entry.name}: ${entry.value} ${entry.unit}`}
             </p>
          ))}
        </div>
      );
    }
    return null;
};

const HourlyChart: React.FC<HourlyChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
      return <div style={{color: 'white', padding: 20}}>Waiting for data...</div>;
  }

  return (
    <div style={{ 
        backgroundColor: 'var(--secondary-bg-color)', 
        borderRadius: '20px', 
        padding: '20px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
    }}>
      <h3 style={{color: 'var(--text-color)', marginTop: 0, textAlign: 'center'}}>Hourly Performance</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{ top: 10, right: 30, left: 10, bottom: 5 }}
        >
          {/* Subtle grid */}
          <CartesianGrid strokeDasharray="3 3" stroke="white" opacity={0.1} vertical={false} />
          
          <XAxis 
             dataKey="log_hour" 
             tickFormatter={formatXAxis} 
             stroke="var(--text-color)"
             tick={{fill: 'var(--text-color)', fontSize: 12}}
             minTickGap={15}
          />
          
          {/* --- AXES --- */}

          {/* 1. LEFT AXIS: Temperature */}
          <YAxis 
            yAxisId="left" 
            stroke="var(--accent-color)" 
            tick={{fill: 'var(--accent-color)'}}
            width={40}
            label={{ value: '°C', position: 'insideTopLeft', dy: -10, fill: 'var(--accent-color)', fontSize: 10 }}
          />

          {/* 2. RIGHT AXIS: Spindle Load */}
          <YAxis 
            yAxisId="right" 
            orientation="right" 
            stroke="#ff7300" 
            tick={{fill: '#ff7300'}}
            width={40}
            label={{ value: '%', position: 'insideTopRight', dy: -10, fill: '#ff7300', fontSize: 10 }}
          />

          {/* 3. HIDDEN AXIS for Power (kW) 
              We give it its own domain so it scales independently (autoscales to fit data) 
              but we hide the visual axis line/numbers to keep UI clean.
          */}
          <YAxis 
            yAxisId="power" 
            orientation="left" 
            hide={true} 
            domain={[0, 'auto']} 
          />

          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ paddingTop: '10px' }}/>

          {/* --- LINES --- */}

          {/* LINE 1: Temperature (Cyan/Blue) */}
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="avg_temp" 
            name="Temperature"
            unit="°C"
            stroke="var(--accent-color)" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6, strokeWidth: 0 }} 
          />

          {/* LINE 2: Spindle (Orange) */}
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="avg_spindle" 
            name="Spindle Load"
            unit="%"
            stroke="#ff7300" 
            strokeWidth={2}
            dot={false} 
            activeDot={{ r: 6, strokeWidth: 0 }} 
          />

          {/* LINE 3: Power (Green Dashed) */}
          <Line 
            yAxisId="power"
            type="monotone" 
            dataKey="power_kW" 
            name="Power Usage"
            unit="kW"
            stroke="#82ca9d" 
            strokeWidth={2}
            strokeDasharray="5 5" // Makes the line dashed
            dot={false} 
            activeDot={{ r: 6, strokeWidth: 0 }} 
          />

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HourlyChart;