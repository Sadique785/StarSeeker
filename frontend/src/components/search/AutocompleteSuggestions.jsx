import React, { useRef, useEffect, useState } from 'react';

function AutocompleteSuggestions({ suggestions, onSelectArtist }) {
  const [overlayTop, setOverlayTop] = useState(0);
  const suggestionsRef = useRef(null);
  
  // Calculate position for the overlay based on suggestions position
  useEffect(() => {
    if (suggestionsRef.current) {
      const rect = suggestionsRef.current.getBoundingClientRect();
      setOverlayTop(rect.top);
    }
  }, [suggestions]);

  return (
    <div className="absolute w-full z-20" ref={suggestionsRef}>
      {/* Overlay that starts below the suggestions container */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm z-10" 
        style={{ 
          top: `${overlayTop}px`,
          pointerEvents: 'none' 
        }} 
      />
      
      {/* Suggestions dropdown */}
      <div className="relative z-20 mt-2 bg-black bg-opacity-80 rounded-lg border border-[#c4bbbb] shadow-xl max-h-80 overflow-y-auto">
        {suggestions.map((artist) => (
          <div
            key={artist.id}
            onClick={() => onSelectArtist(artist)}
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
        ))}
      </div>
    </div>
  );
}

export default AutocompleteSuggestions;