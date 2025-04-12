import base64
import requests
import time
import logging
from typing import Dict, Optional, List, Any

logger = logging.getLogger(__name__)

class SpotifyClient:
    """
    Client for interacting with the Spotify Web API
    """
    BASE_URL = "https://api.spotify.com/v1"
    AUTH_URL = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0
    
    def _get_auth_header(self) -> Dict[str, str]:
        """
        Create authorization header for client credentials flow
        """
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        return {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def _ensure_token(self) -> None:
        """
        Ensure we have a valid access token, obtaining a new one if needed
        """
        current_time = time.time()
        if not self.access_token or current_time >= (self.token_expiry - 60):
            self._get_access_token()
    
    def _get_access_token(self) -> None:
        """
        Get new access token using client credentials flow
        """
        headers = self._get_auth_header()
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(self.AUTH_URL, headers=headers, data=data)
            response.raise_for_status()
            
            response_data = response.json()
            self.access_token = response_data.get("access_token")
            expires_in = response_data.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in
            
            logger.info("Successfully obtained Spotify access token")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain Spotify access token: {str(e)}")
            raise
    
    def _make_api_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an authenticated request to the Spotify API
        """
        self._ensure_token()
        
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_msg = f"Spotify API error: {status_code}"
            
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    if isinstance(error_data["error"], dict) and "message" in error_data["error"]:
                        error_msg += f" - {error_data['error']['message']}"
                    else:
                        error_msg += f" - {error_data['error']}"
            except (ValueError, KeyError):
                pass
            
            logger.error(error_msg)
            
            if status_code == 429: 
                retry_after = int(e.response.headers.get("Retry-After", 3))
                logger.warning(f"Rate limited by Spotify. Retry after {retry_after} seconds")
            
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Spotify API failed: {str(e)}")
            raise
    
    def search_artist(self, name: str, limit: int = 5) -> Dict:
        """
        Search for an artist by name
        """
        endpoint = "search"
        params = {
            "q": name,
            "type": "artist",
            "limit": limit
        }
        return self._make_api_request("get", endpoint, params)
    
    def get_artist(self, artist_id: str) -> Dict:
        """
        Get detailed information about an artist by their Spotify ID
        """
        endpoint = f"artists/{artist_id}"
        return self._make_api_request("get", endpoint)
    
    def get_best_artist_match(self, name: str) -> Optional[Dict]:
        """
        Search for an artist and return the best match based on name
        
        Returns None if no good match is found
        """
        try:
            search_results = self.search_artist(name)
            artists = search_results.get("artists", {}).get("items", [])
            
            if not artists:
                logger.info(f"No artists found for '{name}'")
                return None

            best_match = artists[0]
            
            if best_match["name"].lower() != name.lower():
                logger.info(f"Best match for '{name}' is '{best_match['name']}' (not exact)")
            
            return best_match
        except Exception as e:
            logger.error(f"Error finding artist match for '{name}': {str(e)}")
            return None