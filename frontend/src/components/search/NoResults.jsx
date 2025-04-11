import React from 'react';

function NoResults({ query }) {
  return (
    <div className="mt-8 text-center p-8 bg-black bg-opacity-50 rounded-lg border border-[#a59898]">
      <p className="text-gray-300 text-lg">No artists found matching "{query}"</p>
      <p className="text-gray-400 mt-2">Try adjusting your search terms or explore our featured artists.</p>
    </div>
  );
}

export default NoResults;