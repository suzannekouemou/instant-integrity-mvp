import { cn } from '@/lib/utils';
import { getStatusColor } from '@/lib/utils';

interface BadgeProps {
  status: string;
  className?: string;
}

export function StatusBadge({ status, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border capitalize',
        getStatusColor(status),
        className
      )}
    >
      {status}
    </span>
  );
}
