import { useState, useEffect } from 'react';
import api from '../../services/api';
import AutocompleteSuggestions from './search/AutocompleteSuggestions';

function SearchBar({ setSelectedArtist, setSearchedArtists, onClearSearch }) {
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
        console.log('autocomplete', response);

        // Mark exact matches to prioritize in suggestions
        const processedSuggestions = response.data.map(artist => ({
          ...artist,
          exactMatch: artist.name.toLowerCase() === query.toLowerCase()
        }));
        
        // Sort to prioritize exact matches
        processedSuggestions.sort((a, b) => {
          if (a.exactMatch && !b.exactMatch) return -1;
          if (!a.exactMatch && b.exactMatch) return 1;
          return 0;
        });

        setSuggestions(processedSuggestions);
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
    // Set the selected artist in parent component
    // setSelectedArtist(artist);
    // Update the search input with the selected artist's name
    setQuery(artist.name);
    // Close autocomplete dropdown
    setSuggestions([]);
    
    // Optional: Perform a search with the selected artist to update results
    handleSearch(null, artist.name);
  };

  const handleSearch = async (e, searchQuery = null) => {
    if (e) {
      e.preventDefault();
    }
    
    const searchTerm = searchQuery || query;
    
    if (!searchTerm.trim()) {
      handleClearSearch();
      return;
    }

    setIsLoadingSearch(true);
    
    try {
      const response = await api.get('/artists/search/', {
        params: { query: searchTerm, page: 1, limit: 12 }
      });
      console.log('searched', response);
      
      // Set the search results in parent component with query and pagination info
      const { results, has_next } = response.data;
      setSearchedArtists(results, searchTerm, has_next);
      setSuggestions([]); // Close autocomplete dropdown
    } catch (error) {
      console.error('Error performing search:', error);
      setSearchedArtists([], searchTerm, false);
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
    onClearSearch();
  };

  return (
    <div className="relative">
      <div className="flex items-center mt-10 bg-black bg-opacity-50 rounded-full overflow-hidden backdrop-blur-sm border border-gray-700">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search for artists, genres, or locations..."
          className="flex-1 px-6 py-3 bg-transparent text-white outline-none placeholder-gray-400"
        />
        
        {query && (
          <button
            onClick={handleClearSearch}
            className="text-gray-400 hover:text-white p-2 mr-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </button>
        )}
        
        <button
          onClick={handleSearch}
          className="px-6 py-3 text-white"
        >
          {isLoadingSearch ? (
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      </div>
      
      {/* Autocomplete dropdown */}
      {suggestions.length > 0 && (
        <AutocompleteSuggestions 
          suggestions={suggestions} 
          onSelect={handleSelectArtist}
          isLoading={isLoadingAutocomplete}
        />
      )}
    </div>
  );
}

export default SearchBar;