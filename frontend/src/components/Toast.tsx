import React from 'react';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface ToastProps {
  message: string;
  type: ToastType;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  const bgColor = {
    success: 'bg-green-500/10 border-green-500 text-green-500',
    error: 'bg-valorant-red/10 border-valorant-red text-valorant-red',
    info: 'bg-blue-500/10 border-blue-500 text-blue-500',
  }[type];

  const Icon = {
    success: CheckCircle,
    error: XCircle,
    info: AlertCircle,
  }[type];

  return (
    <div className={`fixed bottom-8 right-8 z-[200] flex items-center gap-4 p-4 border-l-4 ${bgColor} shadow-2xl animate-slide-in`}>
      <Icon size={20} />
      <span className="font-bold uppercase tracking-widest text-sm">{message}</span>
      <button onClick={onClose} className="ml-4 hover:opacity-70">
        <X size={16} />
      </button>
    </div>
  );
};

export default Toast;
