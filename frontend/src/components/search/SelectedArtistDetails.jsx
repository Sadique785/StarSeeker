import React from 'react';

function SelectedArtistDetails({ artist }) {
  return (
    <div className="mt-8 bg-black bg-opacity-70 rounded-lg p-6 border border-[#731C1B]">
      <div className="flex flex-col md:flex-row items-center md:items-start">
        <img 
          src={artist.profilePicture} 
          alt={artist.name} 
          className="w-40 h-40 rounded-lg object-cover mb-4 md:mb-0 md:mr-6"
          onError={(e) => {e.target.src = 'https://via.placeholder.com/160?text=No+Image'}}
        />
        <div className="text-center md:text-left">
          <h2 className="text-2xl font-bold text-white">{artist.name}</h2>
          <p className="text-xl text-gray-300 mt-2">{artist.genre}</p>
          <p className="text-gray-400 mt-1">{artist.location}</p>
          <div className="mt-4">
            <button className="bg-[#731C1B] hover:bg-opacity-80 text-white px-6 py-2 rounded-lg transition-colors">
              View Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SelectedArtistDetails;