# views.py
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from ..documents import ArtistDocument
from ..artist_abbreviations import ARTIST_ABBREVIATIONS




class ArtistSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": [], "correction": None})
        
        # Check for abbreviation
        lower_query = query.lower().replace(' ', '')
        if lower_query in ARTIST_ABBREVIATIONS:
            expanded_query = ARTIST_ABBREVIATIONS[lower_query]
            search = ArtistDocument.search()
            search = search.query('match', name={'query': expanded_query})
            response = search.execute()
            
            results = [{
                'id': hit.meta.id,
                'name': hit.name,
                'genre': getattr(hit, 'genre', ''),
                'profile_picture': getattr(hit, 'profile_picture', ''),
                'location': getattr(hit, 'location', ''),
                'score': hit.meta.score
            } for hit in response]
            
            return Response({
                "results": results,
                "correction": expanded_query,
                "abbreviation_expanded": True
            })
        
        # Start with a multi-match search
        search = ArtistDocument.search()
        
        # Layered search strategy
        combined_query = Q(
            'bool',
            should=[
                # Layer 1: Exact match (highest weight)
                Q('term', name__raw={'value': query, 'boost': 10.0}),
                
                # Layer 2: Standard text match
                Q('match', name={'query': query, 'boost': 5.0}),
                
                # Layer 3: Fuzzy matching for typos
                Q('match', name={
                    'query': query,
                    'fuzziness': 'AUTO',
                    'boost': 3.0
                }),
                
                # Layer 4: Partial matching with edge n-grams
                Q('match', name__edge_ngram={'query': query, 'boost': 1.0}),
            ],
            minimum_should_match=1
        )
        
        search = search.query(combined_query)
        
        # Add sorting by score and popularity
        search = search.sort('_score')
        # Uncomment the following line if you have popularity data
        # search = search.sort('_score', '-popularity')
        
        # Get results
        response = search.execute()
        
        # Check if we need to offer a correction
        exact_match = any(hit.meta.score > 8.0 for hit in response)
        correction = None
        
        if not exact_match and len(response) > 0:
            # Get the top result as a suggestion
            top_hit = response[0]
            if top_hit.meta.score > 3.0:  # Only suggest if confidence is reasonable
                correction = top_hit.name
        
        # Serialize results
        results = [{
            'id': hit.meta.id,
            'name': hit.name,
            'genre': getattr(hit, 'genre', ''),
            'profile_picture': getattr(hit, 'profile_picture', ''),
            'location': getattr(hit, 'location', ''),
            'score': hit.meta.score
        } for hit in response]
        
        return Response({
            "results": results,
            "correction": correction
        })

class ArtistAutocompleteView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        # Create a completion suggester query
        suggest = ArtistDocument.search()
        suggest = suggest.suggest(
            'name_suggestions',
            query,
            completion={
                'field': 'name.suggest',  # Use name.suggest instead of name.completion
                'size': 10
            }
        )
        
        # Execute the suggester query
        suggest_response = suggest.execute()
        
        # Process suggestion results
        suggestions = []
        
        # Extract suggestions from the completion suggester
        if hasattr(suggest_response, 'suggest') and 'name_suggestions' in suggest_response.suggest:
            for suggestion in suggest_response.suggest.name_suggestions[0].options:
                suggestions.append({
                    'id': suggestion._id,  # Access the ID correctly
                    'name': suggestion.text,  # Access the suggestion text
                    'source': 'completion'
                })
        
        # If we don't have enough suggestions, fall back to edge n-gram search
        if len(suggestions) < 5:
            # Use edge n-grams for fallback autocomplete
            search = ArtistDocument.search()
            search = search.query(
                Q('match', name__edge_ngram={'query': query})
            )
            
            # Limit results (adjusted to fill remaining spots)
            remaining = 5 - len(suggestions)
            search = search[:remaining]
            
            # Execute search
            response = search.execute()
            
            # Process results and append to suggestions
            for hit in response:
                # Avoid duplicates
                if not any(s['id'] == hit.meta.id for s in suggestions):
                    suggestions.append({
                        'id': hit.meta.id,
                        'name': hit.name,
                        'source': 'search'
                    })
        
        return Response(suggestions)