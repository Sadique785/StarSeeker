
// src/components/artists/ArtistTracks.jsx
import React from 'react';

const ArtistTracks = ({ tracks }) => {
  return (
    <div className="bg-[090B07] rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Top Tracks</h2>
      {tracks ? (
        <div className="space-y-2">
          {tracks.map((track, index) => (
            <div key={index} className="flex items-center p-3 hover:bg-gray-700 rounded-md">
              <div className="text-gray-500 w-8">{index + 1}</div>
              <div className="flex-1 truncate">
                <p className="font-medium">{track.title}</p>
                <p className="text-sm text-gray-400">{track.album}</p>
              </div>
              <div className="text-gray-400">{track.duration}</div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-400">No tracks available</p>
      )}
    </div>
  );
};

export default ArtistTracks;