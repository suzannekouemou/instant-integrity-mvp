'use client';

import { cn } from '@/lib/utils';

interface ConfidenceGaugeProps {
  value: number;
  size?: 'sm' | 'md' | 'lg';
  status?: 'authentic' | 'suspect' | 'inconclusive';
  showLabel?: boolean;
  className?: string;
}

export function ConfidenceGauge({
  value,
  size = 'md',
  status = 'inconclusive',
  showLabel = true,
  className = '',
}: ConfidenceGaugeProps) {
  const percentage = Math.round(value * 100);
  
  const sizes = {
    sm: { container: 'w-20 h-20', text: 'text-lg', label: 'text-xs', stroke: 6 },
    md: { container: 'w-32 h-32', text: 'text-2xl', label: 'text-sm', stroke: 8 },
    lg: { container: 'w-40 h-40', text: 'text-3xl', label: 'text-base', stroke: 10 },
  };

  const statusColors = {
    authentic: {
      stroke: '#22c55e',
      bg: 'bg-green-50 dark:bg-green-950/30',
      text: 'text-green-600 dark:text-green-400',
    },
    suspect: {
      stroke: '#ef4444',
      bg: 'bg-red-50 dark:bg-red-950/30',
      text: 'text-red-600 dark:text-red-400',
    },
    inconclusive: {
      stroke: '#eab308',
      bg: 'bg-yellow-50 dark:bg-yellow-950/30',
      text: 'text-yellow-600 dark:text-yellow-400',
    },
  };

  const { container, text, label, stroke } = sizes[size];
  const { stroke: strokeColor, text: textColor } = statusColors[status];

  const radius = 50 - stroke / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className={cn('flex flex-col items-center', className)}>
      <div className={cn('relative', container)}>
        <svg
          className="transform -rotate-90"
          viewBox="0 0 100 100"
        >
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={stroke}
            className="text-gray-200 dark:text-slate-700"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-500 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn('font-bold', text, textColor)}>
            {percentage}%
          </span>
        </div>
      </div>
      {showLabel && (
        <span className={cn('mt-2 font-medium capitalize', label, textColor)}>
          {status}
        </span>
      )}
    </div>
  );
}
