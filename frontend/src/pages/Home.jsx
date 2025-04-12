import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FeaturedCards from "../components/FeaturedCards";
import BackgroundVideo from "../components/BackgroundVideo";
import api from "../../services/api";


function Home() {
  const navigate = useNavigate();
  
  // States for artists data
  const [initialArtists, setInitialArtists] = useState([]);
  const [searchedArtists, setSearchedArtists] = useState([]);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [isSearchActive, setIsSearchActive] = useState(false);
  
  // States for pagination and infinite scrolling
  const [page, setPage] = useState(1);
  const [searchPage, setSearchPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [searchHasMore, setSearchHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const observer = useRef();
  
  // Load initial data when component mounts
  useEffect(() => {
    fetchInitialArtists();
  }, []);
  
  // Fetch initial artists data
  const fetchInitialArtists = async (pageNum = 1) => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await api.get('/artists/', {
        params: { page: pageNum, limit: 12 }
      });
      
      const { results, has_next } = response.data;
      
      if (pageNum === 1) {
        setInitialArtists(results);
      } else {
        setInitialArtists(prev => [...prev, ...results]);
      }
      
      setHasMore(has_next);
      setPage(pageNum + 1);
    } catch (error) {
      console.error('Error fetching artists:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // When an artist is selected from search or featured cards
  useEffect(() => {
    if (selectedArtist) {
      navigate(`/artist/${selectedArtist.id}`);
    }
  }, [selectedArtist, navigate]);
  
  // Handle artist selection from featured cards
  const handleArtistSelect = (artist) => {
    setSelectedArtist(artist);
  };
  
  // Setup infinite scrolling
  const lastArtistElementRef = useCallback(node => {
    if (isLoading) return;
    
    if (observer.current) observer.current.disconnect();
    
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        if (isSearchActive && searchHasMore) {
          loadMoreSearchResults();
        } else if (!isSearchActive && hasMore) {
          fetchInitialArtists(page);
        }
      }
    });
    
    if (node) observer.current.observe(node);
  }, [isLoading, isSearchActive, searchHasMore, hasMore, page]);
  
  // Load more search results for infinite scrolling
  const loadMoreSearchResults = async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await api.get('/artists/search/', {
        params: { query: searchQuery.current, page: searchPage, limit: 12 }
      });
      
      const { results, has_next } = response.data;
      
      setSearchedArtists(prev => [...prev, ...results]);
      setSearchHasMore(has_next);
      setSearchPage(searchPage + 1);
    } catch (error) {
      console.error('Error loading more search results:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Reference to store the current search query
  const searchQuery = useRef('');
  
  // Handle search state
  const handleSearchResults = (results, query, hasMore = true) => {
    searchQuery.current = query;
    setSearchedArtists(results);
    setIsSearchActive(true);
    setSearchPage(2); // Reset search pagination
    setSearchHasMore(hasMore);
  };
  
  // Handle clear search
  const handleClearSearch = () => {
    setIsSearchActive(false);
    setSearchedArtists([]);
    searchQuery.current = '';
  };
  
  return (
    <div className="relative h-screen overflow-hidden">
      <BackgroundVideo />
      
      <div className="relative z-10 flex flex-col items-center h-full">
        <Header />
        
        <div className="w-full max-w-2xl px-4 mt-16">
          <SearchBar 
            setSelectedArtist={setSelectedArtist}
            setSearchedArtists={handleSearchResults}
            onClearSearch={handleClearSearch}
          />
        </div>
        
        <div className="flex-1 w-full px-4 mt-10 overflow-auto">
          {isSearchActive ? (
             <div>
             <h2 className="text-2xl font-bold text-white mb-6 text-center">Search Results</h2>
             <div className="flex justify-center">
               <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full max-w-6xl">
                 {searchedArtists.map((artist, index) => {
                  if (searchedArtists.length === index + 1) {
                    return (
                      <div 
                        ref={lastArtistElementRef}
                        key={artist.id} 
                        className="cursor-pointer bg-black bg-opacity-50 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 hover:shadow-purple-500/30"
                        onClick={() => handleArtistSelect(artist)}
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
                        <div className="p-4">
                          <h3 className="text-xl font-bold text-white mb-1">{artist.name}</h3>
                          <p className="text-gray-300">{artist.genre}</p>
                          <p className="text-gray-400 text-sm">{artist.location}</p>
                        </div>
                      </div>
                    );
                  } else {
                    return (
                      <div 
                        key={artist.id} 
                        className="cursor-pointer bg-black bg-opacity-50 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 hover:shadow-purple-500/30"
                        onClick={() => handleArtistSelect(artist)}
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
                        <div className="p-4">
                          <h3 className="text-xl font-bold text-white mb-1">{artist.name}</h3>
                          <p className="text-gray-300">{artist.genre}</p>
                          <p className="text-gray-400 text-sm">{artist.location}</p>
                        </div>
                      </div>
                    );
                  }
                })}
              </div>
            </div>

              {isLoading && (
                <div className="text-center mt-6 text-white">Loading more artists...</div>
              )}
            </div>
          ) : (
            <div>
              <h2 className="text-2xl font-bold text-white mb-6 text-center">Featured Artists</h2>
              <div className="flex justify-center">
                <FeaturedCards 
                  artists={initialArtists} 
                  onSelectArtist={handleArtistSelect} 
                  lastArtistRef={lastArtistElementRef}
                  isLoading={isLoading}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;