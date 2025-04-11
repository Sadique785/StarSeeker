function SearchBar() {
  return (
    <div className="relative">
      <input
        type="text"
        placeholder="Search for artists..."
        className="w-full p-3 rounded bg-white bg-opacity-20 text-white placeholder-white focus:outline-none"
      />
      {/* SuggestionList will come here later */}
    </div>
  );
}

export default SearchBar;
