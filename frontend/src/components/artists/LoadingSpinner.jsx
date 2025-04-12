// src/components/ui/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
      <span className="ml-3">Loading artist details...</span>
    </div>
  );
};

export default LoadingSpinner;