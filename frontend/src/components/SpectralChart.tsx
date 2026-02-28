'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { useTheme } from './ThemeProvider';

interface SpectralDataPoint {
  wavenumber: number;
  intensity: number;
  reference?: number;
}

interface SpectralChartProps {
  data: SpectralDataPoint[];
  showReference?: boolean;
  title?: string;
  className?: string;
}

export function SpectralChart({
  data,
  showReference = false,
  title,
  className = '',
}: SpectralChartProps) {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === 'dark';

  const gridColor = isDark ? '#334155' : '#e5e7eb';
  const textColor = isDark ? '#94a3b8' : '#6b7280';
  const tooltipBg = isDark ? '#1e293b' : '#ffffff';
  const tooltipBorder = isDark ? '#475569' : '#e5e7eb';

  return (
    <div className={`w-full ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          {title}
        </h3>
      )}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
          <XAxis
            dataKey="wavenumber"
            tick={{ fill: textColor, fontSize: 12 }}
            tickFormatter={(value) => `${value}`}
            label={{
              value: 'Wavenumber (cm⁻¹)',
              position: 'insideBottom',
              offset: -5,
              fill: textColor,
              fontSize: 12,
            }}
            reversed
          />
          <YAxis
            tick={{ fill: textColor, fontSize: 12 }}
            label={{
              value: 'Intensity',
              angle: -90,
              position: 'insideLeft',
              fill: textColor,
              fontSize: 12,
            }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: tooltipBg,
              border: `1px solid ${tooltipBorder}`,
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
            labelStyle={{ color: isDark ? '#f1f5f9' : '#111827', fontWeight: 600 }}
            itemStyle={{ color: textColor }}
            formatter={(value?: number) => [value != null ? value.toFixed(4) : '0', 'Intensity']}
            labelFormatter={(label) => `Wavenumber: ${label} cm⁻¹`}
          />
          <Legend
            wrapperStyle={{ color: textColor }}
          />
          <Line
            type="monotone"
            dataKey="intensity"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            name="Sample"
            activeDot={{ r: 4, fill: '#3b82f6' }}
          />
          {showReference && (
            <Line
              type="monotone"
              dataKey="reference"
              stroke="#22c55e"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              name="Reference"
              activeDot={{ r: 4, fill: '#22c55e' }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function generateMockSpectralData(pointCount: number = 200): SpectralDataPoint[] {
  const data: SpectralDataPoint[] = [];
  const startWavenumber = 4000;
  const endWavenumber = 400;
  const step = (startWavenumber - endWavenumber) / pointCount;

  for (let i = 0; i < pointCount; i++) {
    const wavenumber = startWavenumber - i * step;
    const baseIntensity = 0.5 + Math.random() * 0.1;
    
    const peak1 = Math.exp(-Math.pow((wavenumber - 2900) / 50, 2)) * 0.3;
    const peak2 = Math.exp(-Math.pow((wavenumber - 1700) / 30, 2)) * 0.25;
    const peak3 = Math.exp(-Math.pow((wavenumber - 1100) / 40, 2)) * 0.2;
    const peak4 = Math.exp(-Math.pow((wavenumber - 3400) / 60, 2)) * 0.15;
    
    const intensity = baseIntensity + peak1 + peak2 + peak3 + peak4;
    const reference = intensity + (Math.random() - 0.5) * 0.05;

    data.push({
      wavenumber: Math.round(wavenumber),
      intensity: parseFloat(intensity.toFixed(4)),
      reference: parseFloat(reference.toFixed(4)),
    });
  }

  return data;
}
