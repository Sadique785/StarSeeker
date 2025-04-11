import { useState } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FeaturedCards from "../components/FeaturedCards";
import AnimatedTransition from "../components/AnimatedTransition";
import SearchResults from "../components/SearchResults";
import DetailCard from "../components/DetailCard";
import BackgroundVideo from "../components/BackgroundVideo";

function Home() {
  // State to control which view is showing
  const [view, setView] = useState('featured'); // 'featured', 'search', or 'detail'
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [searchActive, setSearchActive] = useState(false);
  
  const handleArtistSelect = (artist) => {
    setSelectedArtist(artist);
    setView('detail');
  };
  
  const handleSearchFocus = (isFocused) => {
    setSearchActive(isFocused);
    if (isFocused) setView('search');
    else setView('featured');
  };
  
  return (
    <div className="relative h-screen overflow-hidden">
      {/* Background Video */}
      <BackgroundVideo />
      
      <div className="relative z-10 flex flex-col items-center h-full">
        <Header />
        
        {/* Search Bar */}
        <div className="w-full max-w-2xl px-4 mt-6">
          <SearchBar 
            onFocus={() => handleSearchFocus(true)}
            onBlur={() => handleSearchFocus(false)}
          />
        </div>
        
        {/* Dynamic Content Area */}
        <div className="flex-1 w-full px-4 mt-10 overflow-hidden">
          {/* Content switches based on view state */}
          {/* Featured Cards section */}
          <div className="flex-1 w-full px-4 mt-10">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Featured Artists</h2>
            <div className="flex justify-center">
              <FeaturedCards onSelectArtist={handleArtistSelect} />
            </div>
          </div>
          
          {/* <AnimatedTransition show={view === 'search'}>
            <SearchResults onSelectArtist={handleArtistSelect} />
          </AnimatedTransition> */}
          
          <AnimatedTransition show={view === 'detail'}>
            <DetailCard artist={selectedArtist} onClose={() => setView('featured')} />
          </AnimatedTransition>
        </div>
      </div>
    </div>
  );
}

export default Home;