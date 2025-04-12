
// src/components/artists/ArtistAlbums.jsx
import React from 'react';

const ArtistAlbums = ({ albums }) => {
  return (
    <div className="bg-[090B07] rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold mb-4">Popular Albums</h2>
      {albums ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {albums.map((album, index) => (
            <div key={index} className="group">
              <div className="relative overflow-hidden rounded-md aspect-square mb-2">
                <img 
                  src={album.image || "/api/placeholder/200/200"} 
                  alt={album.title} 
                  className="w-full h-full object-cover transition-transform group-hover:scale-110" 
                />
              </div>
              <h3 className="font-medium text-sm truncate">{album.title}</h3>
              <p className="text-gray-400 text-xs">{album.year}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-400">No albums available</p>
      )}
    </div>
  );
};

export default ArtistAlbums;
