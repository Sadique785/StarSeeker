
// src/components/artists/ArtistTags.jsx
import React from 'react';

const ArtistTags = ({ tags }) => {
  if (!tags || tags.length === 0) return null;
  
  return (
    <div className="bg-[090B07] rounded-lg p-6 mb-8">
      <h2 className="text-xl font-bold mb-4">Tags</h2>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag, index) => (
          <span key={index} className="px-3 py-1 bg-gray-700 rounded-full text-sm">
            {tag.name}
          </span>
        ))}
      </div>
    </div>
  );
};

export default ArtistTags;