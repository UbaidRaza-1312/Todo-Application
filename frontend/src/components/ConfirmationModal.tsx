import React from 'react';

interface ConfirmationModalProps {
  isOpen: boolean;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
  confirmText?: string;
  cancelText?: string;
}

const ConfirmationModal: React.FC<ConfirmationModalProps> = ({
  isOpen,
  message,
  onConfirm,
  onCancel,
  confirmText = 'Yes',
  cancelText = 'No'
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
      <div className="bg-gray-800 rounded-xl p-8 max-w-md w-full mx-4 border border-gray-700 shadow-2xl transform transition-transform duration-300 scale-95 animate-in fade-in-90 zoom-in-90">
        <div className="text-white mb-6 text-center">
          <h3 className="text-xl font-bold mb-2">Confirm Action</h3>
          <p className="text-gray-300 whitespace-pre-line">{message}</p>
        </div>

        <div className="flex justify-center space-x-4">
          <button
            onClick={onCancel}
            className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200 font-medium"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 font-medium"
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;