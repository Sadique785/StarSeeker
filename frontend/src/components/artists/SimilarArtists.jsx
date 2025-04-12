
// src/components/artists/SimilarArtists.jsx
import React from 'react';

const SimilarArtists = ({ artists }) => {
  if (!artists || artists.length === 0) return null;
  
  return (
    <div className="bg-[090B07] rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Similar Artists</h2>
      <div className="space-y-4">
        {artists.map((artist, index) => (
          <div key={index} className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-full bg-gray-700 overflow-hidden">
              <img 
                src={artist.image?.[0]?.["#text"] || "/api/placeholder/48/48"} 
                alt={artist.name} 
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1">
              <p className="font-medium truncate">{artist.name}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimilarArtists;
