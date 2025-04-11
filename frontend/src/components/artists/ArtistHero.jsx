import React from 'react';

const ArtistHero = ({ artist }) => {
  // Find the largest image from lastfm or use a fallback
  const heroImage = artist.profile_picture;

  return (
    <div className="relative h-96 w-full mt-0">
      {/* Hero Background - Changed to object-contain or object-cover with proper positioning */}
      <div className="absolute inset-0 overflow-hidden">
        <img
          src={heroImage}
          alt={`${artist.name}`}
          className="w-full h-full object-cover object-center"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-gray-900/90"></div>
      </div>

      {/* Content positioned at the bottom of the hero */}
      <div className="absolute bottom-0 left-0 w-full p-8">
        <div className="container mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-2">{artist.name}</h1>
          {artist.stats && (
            <p className="text-gray-300">
              {parseInt(artist.stats.listeners).toLocaleString()} listeners · {parseInt(artist.stats.playcount).toLocaleString()} plays
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ArtistHero;