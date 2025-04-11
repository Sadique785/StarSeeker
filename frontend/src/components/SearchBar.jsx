import { useState, useEffect } from 'react';
import api from '../../services/api';
import AutocompleteSuggestions from './search/AutocompleteSuggestions';

function SearchBar({ setSelectedArtist, setSearchedArtists }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isLoadingAutocomplete, setIsLoadingAutocomplete] = useState(false);
  const [isLoadingSearch, setIsLoadingSearch] = useState(false);

  // Autocomplete effect with debounce
  useEffect(() => {
    const fetchAutocomplete = async () => {
      if (query.length < 2) {
        setSuggestions([]);
        return;
      }

      setIsLoadingAutocomplete(true);
      try {
        const response = await api.get('/artists/autocomplete/', {
          params: { query }
        });
        setSuggestions(response.data);
      } catch (error) {
        console.error('Error fetching autocomplete suggestions:', error);
      } finally {
        setIsLoadingAutocomplete(false);
      }
    };

    const timer = setTimeout(fetchAutocomplete, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const handleSelectArtist = (artist) => {
    // Just set the selected artist in parent component
    setSelectedArtist(artist);
    setQuery(artist.name);
    setSuggestions([]);
  };

  const handleSearch = async (e) => {
    if (e) {
      e.preventDefault();
    }
    
    if (!query.trim()) {
      return;
    }

    setIsLoadingSearch(true);
    
    try {
      const response = await api.get('/artists/search/', {
        params: { query }
      });
      
      // Set the search results in parent component
      setSearchedArtists(response.data);
      setSuggestions([]); // Close autocomplete dropdown
    } catch (error) {
      console.error('Error performing search:', error);
      setSearchedArtists([]);
    } finally {
      setIsLoadingSearch(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Clear search state
  const handleClearSearch = () => {
    setQuery('');
    setSelectedArtist(null);
    setSearchedArtists([]);
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSearch} className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search for artists..."
          className="w-full p-4 pl-10 pr-16 rounded-lg bg-black bg-opacity-50 text-white placeholder-gray-400 border border-[#a59898] focus:outline-none focus:ring-2 focus:ring-[#6e6e6e] focus:border-transparent shadow-lg"
        />
        {query && (
          <button
            type="button"
            onClick={handleClearSearch}
            className="absolute right-24 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
        <button
          type="submit"
          className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-[#731C1B] hover:bg-opacity-80 text-white px-4 py-2 rounded-md transition-colors"
          disabled={isLoadingSearch}
        >
          {isLoadingSearch ? (
            <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
          ) : (
            'Search'
          )}
        </button>
        {isLoadingAutocomplete && (
          <div className="absolute right-24 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
          </div>
        )}
      </form>

      {/* Autocomplete Suggestions */}
      {suggestions.length > 0 && (
        <AutocompleteSuggestions suggestions={suggestions} onSelectArtist={handleSelectArtist} />
      )}
    </div>
  );
}

export default SearchBar;