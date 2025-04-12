// components/ShimmerCard.jsx
import React from 'react';

function ShimmerCard() {
  return (
    <div className="bg-black/30 backdrop-blur-sm border border-gray-600 rounded-lg overflow-hidden animate-pulse">
      <div className="aspect-square bg-gray-700"></div>
      
      <div className="p-4 space-y-3">
        <div className="h-6 bg-gray-700 rounded w-3/4"></div>
        
        <div className="h-4 bg-gray-700 rounded w-1/2"></div>
        
        <div className="h-4 bg-gray-700 rounded w-2/3"></div>
        
        <div className="h-10 bg-gray-700 rounded-full mt-3"></div>
      </div>
    </div>
  );
}

export default ShimmerCard;