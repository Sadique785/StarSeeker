// components/FeaturedCards.jsx
import React from 'react';
import ShimmerCard from './Shimmers/ShimmerCard';


function FeaturedCards({ artists, onSelectArtist, lastArtistRef, isLoading }) {
  if (!artists || artists.length === 0) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full max-w-6xl">
        {[...Array(8)].map((_, index) => (
          <ShimmerCard key={`shimmer-${index}`} />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full max-w-6xl">
      {artists.map((artist, index) => {
        if (artists.length === index + 1) {
          return (
            <div 
              ref={lastArtistRef}
              key={artist.id} 
              className="bg-black/40 backdrop-blur-sm border border-gray-800 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 hover:shadow-red-900/30 cursor-pointer h-full"
              onClick={() => onSelectArtist(artist)}
            >
              <div className="aspect-square overflow-hidden">
                <img 
                  src={artist.profile_picture || `/api/placeholder/300/300?text=${encodeURIComponent(artist.name)}`} 
                  alt={artist.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = `/api/placeholder/300/300?text=${encodeURIComponent(artist.name)}`;
                  }}
                />
              </div>
              <div className="p-4 flex flex-col h-48">
                <h3 className="text-xl font-bold text-white mb-1 line-clamp-2">{artist.name}</h3>
                <p className="text-gray-300">{artist.genre === 'Unknown' ? '' : artist.genre}</p>
                <p className="text-gray-400 text-sm">{artist.location}</p>
                <button 
                  className="mt-auto px-4 py-2 bg-gradient-to-r from-red-900 to-black text-white rounded-full text-sm font-medium hover:from-red-800 hover:to-gray-900 transition-colors w-full"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectArtist(artist);
                  }}
                >
                  View Profile
                </button>
              </div>
            </div>
          );
        } else {
          return (
            <div 
              key={artist.id} 
              className="bg-black/40 backdrop-blur-sm border border-gray-800 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 hover:shadow-red-900/30 cursor-pointer h-full"
              onClick={() => onSelectArtist(artist)}
            >
              <div className="aspect-square overflow-hidden">
                <img 
                  src={artist.profile_picture || `/api/placeholder/300/300?text=${encodeURIComponent(artist.name)}`}
                  alt={artist.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = `/api/placeholder/300/300?text=${encodeURIComponent(artist.name)}`;
                  }}
                />
              </div>
              <div className="p-4 flex flex-col h-48">
                <h3 className="text-xl font-bold text-white mb-1 line-clamp-2">{artist.name}</h3>
                <p className="text-gray-300">{artist.genre === 'Unknown' ? '' : artist.genre}</p>
                <p className="text-gray-400 text-sm">{artist.location}</p>
                <button 
                  className="mt-auto px-4 py-2 bg-gradient-to-r from-red-900 to-black text-white rounded-full text-sm font-medium hover:from-red-800 hover:to-gray-900 transition-colors w-full"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectArtist(artist);
                  }}
                >
                  View Profile
                </button>
              </div>
            </div>
          );
        }
      })}
      
      {isLoading && (
        <div className="col-span-full text-center mt-6 text-white">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-red-900 border-r-transparent">
            <span className="sr-only">Loading...</span>
          </div>
          <p className="mt-2">Loading more artists...</p>
        </div>
      )}
    </div>
  );
}

export default FeaturedCards;