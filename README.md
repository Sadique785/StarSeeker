# Star Seeker - Artist Search Application

Star Seeker is a powerful and fast artist search application that allows users to explore artists worldwide, powered by **Django**, **PostgreSQL**, **Elasticsearch**, and a modern **React + Vite + Tailwind** frontend.

Real-time suggestions, smart corrections, and detailed artist profiles — all in one place!

## ✨ Features

* 🔍 **Fast Artist Search**
   * Instant search results with auto-suggestions
   * Phonetic search for similar sounding names
   * Partial name matches (e.g., *Cold Play* → *Coldplay*)
* 🧠 **Smart Corrections**
   * Typo-tolerant search
   * Suggested corrections for misspelled queries
* 🎨 **Beautiful UI**
   * Clean landing page with video background
   * Smooth transitions and responsive design
   * Dark overlay on search focus for immersive experience
* 🗂️ **Detailed Artist Pages**
   * Display artist name, genre, country, profile image, and more!
   * Scalable structure for future metadata like albums and tracks

## ⚙️ Tech Stack

* **Backend:** Django + Django REST Framework
* **Database:** PostgreSQL (Dockerized)
* **Search Engine:** Elasticsearch (Dockerized)
* **Frontend:** React (Vite) + Tailwind CSS
* **Containerization:** Docker & Docker Compose
* **Version Control:** Git + GitHub

## 🔍 Elasticsearch Implementation

### Docker Configuration
- Containerized Elasticsearch for easy deployment
- Configured with persistent volume mapping

### Elasticsearch-DSL Integration
- Using Python's Elasticsearch-DSL client library
- Custom document mappings with proper field types

### Search Types
- **Basic Text Search**: Standard full-text search across artist names
- **Fuzzy Search**: Handles typos using Levenshtein distance
- **Phonetic Search**: Matches similar-sounding names
- **Prefix & Partial Matching**: For incomplete queries
- **Combined Search Strategy**: Multi-field search with boosting

## 🚀 Getting Started

### Prerequisites
* Docker & Docker Compose
* Node.js & npm
* Python 3.8+

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-username/star-seeker.git
cd star-seeker/backend

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Docker Services
```bash
# Start PostgreSQL and Elasticsearch
docker-compose up -d
```

## 📋 Environment Configuration

### Backend (.env)
```
SECRET_KEY=your-secret-key-here

# Database Configuration
POSTGRES_DB=musicdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# API Keys
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
LASTFM_API_KEY=your-lastfm-api-key
```

### Frontend (.env)
```
VITE_BACKEND_URL=http://localhost:8000/api
VITE_VIDEO_URL_1=/path/to/background/video.mp4
VITE_LASTFM_API_KEY=your-lastfm-api-key
```

## 📚 Resources

- **API Documentation**: [Link to API Documentation](#)
- **Demo Video**: [Link to Loom Video](#)

## 📁 Directory Structure
```
/
├── backend/
│   ├── api/
│   ├── artists/
│   ├── core/
│   ├── data_collection/
│   └── search/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
├── docker/
│   ├── elasticsearch/
│   └── postgres/
└── docker-compose.yml
```

## 💡 Future Improvements
* Add **Kibana** for Elasticsearch visualization
* Enhance **ranking algorithm** (popularity, relevance)
* Add **user accounts** and saved searches
* Add **unit tests** and integration tests
* Deploy to **AWS Free Tier**

## 🤝 Contribution
Contributions, issues, and feature requests are welcome! Feel free to open a PR or submit an issue.

## 📄 License
This project is licensed under the MIT License.