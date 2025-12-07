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
          {/* Grid lines with low opacity to blend into dark bg */}
          <CartesianGrid strokeDasharray="3 3" stroke="white" opacity={0.1} vertical={false} />
          
          <XAxis 
             dataKey="log_hour" 
             tickFormatter={formatXAxis} 
             stroke="var(--text-color)"
             tick={{fill: 'var(--text-color)', fontSize: 12}}
             minTickGap={15}
          />
          
          {/* LEFT AXIS: Temperature (matches avg_temp) */}
          <YAxis 
            yAxisId="left" 
            stroke="var(--accent-color)" 
            tick={{fill: 'var(--accent-color)'}}
            width={40}
          />

          {/* RIGHT AXIS: Spindle Load (matches avg_spindle) */}
          <YAxis 
            yAxisId="right" 
            orientation="right" 
            stroke="#ff7300" 
            tick={{fill: '#ff7300'}}
            width={40}
          />

          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ paddingTop: '10px' }}/>

          {/* LINE 1: Temperature (Cyan) */}
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="avg_temp" 
            name="Temperature"
            unit="°C"
            stroke="var(--accent-color)" 
            strokeWidth={3}
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
            strokeWidth={3}
            dot={false} 
            activeDot={{ r: 6, strokeWidth: 0 }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HourlyChart;