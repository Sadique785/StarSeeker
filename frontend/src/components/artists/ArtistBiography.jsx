import React, { useState } from 'react';

const ArtistBiography = ({ bio, description }) => {
  const [expanded, setExpanded] = useState(false);
  const bioText = bio ? bio.replace(/<a.*?<\/a>/g, '') : (description || "No biography available for this artist.");
  
  // Characters to show in collapsed state
  const charLimit = 300;
  const isBioLong = bioText.length > charLimit;
  
  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  return (
    <div className="bg-[090B07] rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold mb-4">Biography</h2>
      <div className="prose prose-invert max-w-none">
        <p>
          {isBioLong && !expanded ? (
            <>
              {bioText.substring(0, charLimit)}...
              <button 
                onClick={toggleExpanded}
                className="ml-2 text-blue-400 hover:underline font-medium"
              >
                See More
              </button>
            </>
          ) : (
            <>
              {bioText}
              {isBioLong && expanded && (
                <button 
                  onClick={toggleExpanded}
                  className="ml-2 text-blue-400 hover:underline font-medium"
                >
                  See Less
                </button>
              )}
            </>
          )}
        </p>
      </div>
    </div>
  );
};

export default ArtistBiography;