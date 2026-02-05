import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AlertProps {
  type: 'success' | 'error' | 'info';
  message: string;
  className?: string;
}

export function Alert({ type, message, className }: AlertProps) {
  const styles = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
  };

  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: AlertCircle,
  };

  const Icon = icons[type];

  return (
    <div className={cn('flex items-center gap-3 p-4 rounded-lg border', styles[type], className)}>
      <Icon className="h-5 w-5 flex-shrink-0" />
      <p className="text-sm">{message}</p>
    </div>
  );
}
