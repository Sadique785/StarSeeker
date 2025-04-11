function DetailCard({ artist, onClose }) {
    if (!artist) return null;
    
    return (
      <div className="bg-black/80 rounded-lg overflow-hidden">
        <div className="flex flex-col md:flex-row">
          {/* Left side - Image */}
          <div className="w-full md:w-2/5 h-96 md:h-auto">
            <img
              src={artist.image}
              alt={artist.name}
              className="w-full h-full object-cover"
            />
          </div>
          
          {/* Right side - Details */}
          <div className="w-full md:w-3/5 p-8 text-white">
            <div className="flex justify-between items-start">
              <h2 className="text-3xl font-bold">{artist.name}</h2>
              <button 
                onClick={onClose}
                className="text-gray-400 hover:text-white"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="mt-6 space-y-4">
              <div>
                <h3 className="text-gray-400 text-sm">Genre</h3>
                <p>{artist.genre}</p>
              </div>
              
              <div>
                <h3 className="text-gray-400 text-sm">Location</h3>
                <p>{artist.location}</p>
              </div>
              
              <div>
                <h3 className="text-gray-400 text-sm">Biography</h3>
                <p className="text-sm leading-relaxed">{artist.bio}</p>
              </div>
              
              <div className="mt-8">
                <button className="bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-6 rounded-full">
                  View More
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }


export default DetailCard;