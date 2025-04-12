import React, { useRef, useEffect, useState } from 'react';

function AutocompleteSuggestions({ suggestions, onSelect, isLoading }) {
  const [overlayTop, setOverlayTop] = useState(0);
  const suggestionsRef = useRef(null);
  
  useEffect(() => {
    if (suggestionsRef.current) {
      const rect = suggestionsRef.current.getBoundingClientRect();
      setOverlayTop(rect.top);
    }
  }, [suggestions]);

  const sortedSuggestions = [...suggestions].sort((a, b) => {
    if (a.exactMatch) return -1;
    if (b.exactMatch) return 1;
    return 0;
  });

  return (
    <div className="absolute w-full z-20" ref={suggestionsRef}>
      <div 
        className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm z-10" 
        style={{ 
          top: `${overlayTop}px`,
          pointerEvents: 'none' 
        }} 
      />
      
      <div className="relative z-20 mt-2 bg-black bg-opacity-80 rounded-lg border border-[#c4bbbb] shadow-xl max-h-80 overflow-y-auto">
        {isLoading ? (
          <div className="flex justify-center p-4">
            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : (
          sortedSuggestions.map((artist) => (
            <div
              key={artist.id}
              onClick={() => onSelect(artist)}
              className="flex items-center p-3 hover:bg-[#731C1B] hover:bg-opacity-50 cursor-pointer transition-colors"
            >
              <img
                src={artist.profile_picture}
                alt={artist.name}
                className="w-12 h-12 rounded-full object-cover mr-3"
                onError={(e) => {e.target.src = 'https://via.placeholder.com/48?text=NA'}}
              />
              <div>
                <div className="text-white font-medium">{artist.name}</div>
                <div className="text-gray-400 text-sm">{artist.genre} • {artist.location}</div>
              </div>
            </div>
          ))
        )}
        {!isLoading && suggestions.length === 0 && (
          <div className="p-3 text-gray-400 text-center">No suggestions found</div>
        )}
      </div>
    </div>
  );
}

export default AutocompleteSuggestions;