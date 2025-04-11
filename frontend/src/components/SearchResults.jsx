function SearchResults({ onSelectArtist }) {
    // Dummy data - would come from your actual search logic
    const suggestions = [
      { id: 1, name: "Artist 1", genre: "Rock", image: "path/to/image" },
      { id: 2, name: "Artist 2", genre: "Jazz", image: "path/to/image" },
      // More artists...
    ];
    
    return (
      <div className="bg-black/80 rounded-lg p-4 text-white">
        <h3 className="text-xl mb-4">Suggestions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suggestions.map(artist => (
            <div 
              key={artist.id} 
              className="flex items-center p-3 rounded hover:bg-gray-800 cursor-pointer"
              onClick={() => onSelectArtist(artist)}
            >
              <img src={artist.image} className="w-12 h-12 rounded-full object-cover" alt={artist.name} />
              <div className="ml-3">
                <p className="font-semibold">{artist.name}</p>
                <p className="text-sm text-gray-400">{artist.genre}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }


  export default SearchResults;