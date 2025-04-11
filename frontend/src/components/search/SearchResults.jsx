import React from 'react';

function SearchResults({ results }) {

  console.log('resultsfromsearchresults',results)
  return (
    <div className="mt-8">
      <h3 className="text-xl text-white font-semibold mb-4">Search Results</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {results.map((artist) => (
          <div key={artist.id} className="bg-black bg-opacity-70 rounded-lg p-4 border border-[#731C1B] hover:border-white transition-colors">
            <div className="flex items-start">
              <img 
                src={artist.profile_picture} 
                alt={artist.name} 
                className="w-20 h-20 rounded-lg object-cover mr-4"
                onError={(e) => {e.target.src = 'https://via.placeholder.com/80?text=NA'}}
              />
              <div>
                <h2 className="text-lg font-bold text-white">{artist.name}</h2>
                <p className="text-gray-300">{artist.genre}</p>
                <p className="text-gray-400 text-sm">{artist.location}</p>
                <button className="mt-2 bg-[#731C1B] hover:bg-opacity-80 text-white px-4 py-1 text-sm rounded-lg transition-colors">
                  View Profile
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchResults;