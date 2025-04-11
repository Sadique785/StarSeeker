import React from 'react';

function LoadingAnimation() {
  return (
    <div className="flex justify-center items-center p-4">
      <div className="relative w-12 h-12">
        <div className="absolute top-0 left-0 right-0 bottom-0 animate-pulse bg-[#731C1B] rounded-full opacity-75"></div>
        <div className="absolute top-1 left-1 right-1 bottom-1 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <div className="absolute top-3 left-3 right-3 bottom-3 bg-black rounded-full"></div>
      </div>
    </div>
  );
}

export default LoadingAnimation;