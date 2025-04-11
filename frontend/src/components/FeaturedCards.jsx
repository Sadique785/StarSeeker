// components/FeaturedCards.jsx
import { useState } from 'react';

function FeaturedCards() {
  // Example featured artists data
  const [featuredArtists] = useState([
    {
      id: 1,
      name: "Justin Beiber",
      genre: "Pop",
      imageUrl: "/images/artist1.jpg" 
    },
    {
      id: 2,
      name: "The Weeknd",
      genre: "R&B",
      imageUrl: "/images/artist2.jpg" 
    },
    {
      id: 3,
      name: "Bruno Mars",
      genre: "Hip Hop",
      imageUrl: "/images/artist3.jpg" 
    },
    {
        id: 4,
        name: "Billie Eilish",
        genre: "Alternative",
        imageUrl: "/images/artist4.jpg" 
      }
  ]);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-6xl">
      {featuredArtists.map((artist) => (
        <div 
          key={artist.id} 
          className="bg-black/30 backdrop-blur-sm border border-gray-600 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 hover:shadow-purple-500/30"
        >
          <div className="aspect-square overflow-hidden">
            <img 
              src={artist.imageUrl} 
              alt={artist.name}
              className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
              // If you don't have images, use placeholder:
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = `/api/placeholder/300/300?text=${encodeURIComponent(artist.name)}`;
              }}
            />
          </div>
          <div className="p-4">
            <h3 className="text-xl font-bold text-white mb-1">{artist.name}</h3>
            <p className="text-gray-300">{artist.genre}</p>
            <button className="mt-3 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full text-sm font-medium hover:from-purple-700 hover:to-blue-700 transition-colors w-full">
              View Profile
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default FeaturedCards;