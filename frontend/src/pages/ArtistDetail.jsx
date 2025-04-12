import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import axios from 'axios';

// Import components
import Header from '../components/Header';
import ArtistHero from '../components/artists/ArtistHero';
import ArtistBiography from '../components/artists/ArtistBiography';
import ArtistAlbums from '../components/artists/ArtistAlbums';
import ArtistTracks from '../components/artists/ArtistTracks';
import ArtistProfile from '../components/artists/ArtistProfile';
import ArtistTags from '../components/artists/ArtistTags';
import SimilarArtists from '../components/artists/SimilarArtists';
import LoadingSpinner from '../components/artists/LoadingSpinner';

const ArtistDetail = () => {
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [artist, setArtist] = useState(null);
  const [additionalInfo, setAdditionalInfo] = useState(null);
  const [error, setError] = useState(null);
  const apiKey = import.meta.env.VITE_LASTFM_API_KEY;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Step 1: Get basic artist data from your database
        const artistResponse = await api.get(`/artists/${id}`);
        const artistData = artistResponse.data;
        
        // Step 2: Use the artist name to fetch additional data from Last.fm
        if (artistData && artistData.name) {
          const lastFmResponse = await axios.get(
            `https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=${encodeURIComponent(
              artistData.name
            )}&api_key=${apiKey}&format=json`
          );
          console.log('lastFmResponse',lastFmResponse)
          
          // Merge LastFM data with our artist data
          const mergedArtist = {
            ...artistData,
            lastfmImage: lastFmResponse.data.artist?.image || [],
            stats: lastFmResponse.data.artist?.stats || null
          };
          
          setArtist(mergedArtist);
          
          setAdditionalInfo({
            bio: lastFmResponse.data.artist?.bio?.content || null,
            tags: lastFmResponse.data.artist?.tags?.tag || [],
            similar: lastFmResponse.data.artist?.similar?.artist || []
          });
        } else {
          setArtist(artistData);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching artist data:', err);
        setError('Failed to load artist information');
        setLoading(false);
      }
    };

    fetchData();
  }, [id, apiKey]);

  if (loading) return (
    <>
      <Header isTransparent={false} />
      <LoadingSpinner />
    </>
  );
  
  if (error) return (
    <>
      <Header isTransparent={false} />
      <div className="text-red-500 text-center p-4 mt-16">{error}</div>
    </>
  );
  
  if (!artist) return (
    <>
      <Header isTransparent={false} />
      <div className="text-center p-4 mt-16">Artist not found</div>
    </>
  );

  return (
    <div className="bg-gradient-to-b from-[#731C1B] via-[#090B07] to-black text-white min-h-screen">
      {/* Header */}
      <Header isTransparent={true} />
      
      {/* Hero Section */}
      <ArtistHero artist={artist} />

      {/* Content Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <ArtistBiography 
              bio={additionalInfo?.bio} 
              description={artist.description} 
            />
            <ArtistAlbums albums={artist.albums} />
            <ArtistTracks tracks={artist.topTracks} />
          </div>

          {/* Sidebar */}
          <div>
            <ArtistProfile artist={artist} />
            <ArtistTags tags={additionalInfo?.tags} />
            <SimilarArtists artists={additionalInfo?.similar} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArtistDetail;