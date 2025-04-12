
// src/components/artists/ArtistProfile.jsx
import React from 'react';

const ArtistProfile = ({ artist }) => {
  console.log('artist',artist)
  // Get the appropriate last.fm image based on the response data
  const getProfileImage = () => {
    if (artist.lastfmImage && artist.lastfmImage.length > 0) {
      // Find extralarge or large image
      const extraLargeImage = artist.lastfmImage.find(img => img.size === 'extralarge');
      const largeImage = artist.lastfmImage.find(img => img.size === 'large');
      return extraLargeImage?.['#text'] || largeImage?.['#text'] || artist.image || "/api/placeholder/300/300";
    }
    return artist.image || "/api/placeholder/300/300";
  };

  return (
    <div className="bg-[090B07] rounded-lg p-6 mb-8">
      <div className="rounded-md overflow-hidden mb-4">
        <img 
          src={artist.profile_picture}
          alt={artist.name} 
          className="w-full object-cover"
        />
      </div>
      <div className="flex flex-col space-y-3">
        {artist.followers && (
          <div className="flex justify-between">
            <span className="text-gray-400">Followers:</span>
            <span>{artist.followers.toLocaleString()}</span>
          </div>
        )}
        {artist.popularity && (
          <div className="flex justify-between">
            <span className="text-gray-400">Popularity:</span>
            <div className="w-24 bg-gray-700 rounded-full h-2.5">
              <div 
                className="bg-green-500 h-2.5 rounded-full" 
                style={{ width: `${artist.popularity}%` }}
              ></div>
            </div>
          </div>
        )}
        {artist.formed && (
          <div className="flex justify-between">
            <span className="text-gray-400">Formed:</span>
            <span>{artist.formed}</span>
          </div>
        )}
        {artist.stats && (
          <>
            <div className="flex justify-between">
              <span className="text-gray-400">Listeners:</span>
              <span>{parseInt(artist.stats.listeners).toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Playcount:</span>
              <span>{parseInt(artist.stats.playcount).toLocaleString()}</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ArtistProfile;
