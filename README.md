Star Seeker Documentation
Project Overview
Star Seeker is a music artist search application that allows users to search through a database of 100,000+ artists, providing real-time auto-suggestions and displaying artist information (name, genre, profile picture, location).
Technical Architecture

Backend: Django + Django REST Framework
Database: PostgreSQL (Dockerized)
Search Engine: Elasticsearch (Dockerized)
Frontend: React with Vite + Tailwind CSS
Containerization: Docker & Docker Compose

Key Features

Fast artist search with auto-suggestions
Smart correction for typos and misspellings
Beautiful UI with video background
Detailed artist profiles

Elasticsearch Implementation
Docker Configuration

Containerized Elasticsearch for easy deployment
Configured with persistent volume mapping

Elasticsearch-DSL Integration

Using Python's Elasticsearch-DSL client library
Custom document mappings with proper field types

Search Types

Basic Text Search: Standard full-text search across artist names
Fuzzy Search: Handles typos using Levenshtein distance
Phonetic Search: Matches similar-sounding names
Prefix & Partial Matching: For incomplete queries
Combined Search Strategy: Multi-field search with boosting

Environment Configuration
Backend (.env)
SECRET_KEY=your-secret-key-here
POSTGRES_DB=musicdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
LASTFM_API_KEY=your-lastfm-api-key
Frontend (.env)
VITE_BACKEND_URL=http://localhost:8000/api
VITE_VIDEO_URL_1=/path/to/background/video.mp4
VITE_LASTFM_API_KEY=your-lastfm-api-key
Resources

API Documentation: Link to API Documentation
Demo Video: Link to Loom Video

Current Status
The application has an established foundation but requires environment file standardization and Docker configuration finalization before deployment.
License
This project is licensed under the MIT License.
