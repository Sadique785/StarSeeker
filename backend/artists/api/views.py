# views.py
from elasticsearch_dsl import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..documents import ArtistDocument
from ..artist_abbreviations import ARTIST_ABBREVIATIONS
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from ..models import Artist
from .serializers import ArtistSerializer


class ArtistPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['has_next'] = self.page.has_next()
        return response

class ArtistListView(ListAPIView):
    queryset = Artist.objects.all().order_by('-popularity')
    serializer_class = ArtistSerializer
    pagination_class = ArtistPagination

class ArtistDetailView(generics.RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_field = 'id'
class ArtistSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"results": [], "correction": None})
        
        lower_query = query.lower().replace(' ', '')
        if lower_query in ARTIST_ABBREVIATIONS:
            expanded_query = ARTIST_ABBREVIATIONS[lower_query]
            search = ArtistDocument.search()
            search = search.query('match', name={'query': expanded_query})
            search = search.sort('_score', '-popularity')
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
        
        search = ArtistDocument.search()
        
        combined_query = Q(
            'bool',
            should=[
                Q('term', name__raw={'value': query, 'boost': 10.0}),
                Q('match', name={'query': query, 'boost': 5.0}),
                Q('match', name={
                    'query': query,
                    'fuzziness': 'AUTO',
                    'boost': 3.0
                }),
                Q('match', name__edge_ngram={'query': query, 'boost': 1.0}),
            ],
            minimum_should_match=1
        )
        
        search = search.query(combined_query)
        search = search.sort('_score', '-popularity')
        
        response = search.execute()
        
        exact_match = any(hit.meta.score > 8.0 for hit in response)
        correction = None
        
        if not exact_match and len(response) > 0:
            top_hit = response[0]
            if top_hit.meta.score > 3.0:
                correction = top_hit.name
        
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
        query = request.query_params.get('query', '')
        if not query:
            return Response([])
        
        suggest = ArtistDocument.search()
        suggest = suggest.suggest(
            'name_suggestions',
            query,
            completion={
                'field': 'name.suggest',
                'size': 10
            }
        )
        
        suggest_response = suggest.execute()
        
        suggestions = []
        
        if hasattr(suggest_response, 'suggest') and 'name_suggestions' in suggest_response.suggest:
            for suggestion in suggest_response.suggest.name_suggestions[0].options:
                artist_doc = ArtistDocument.get(id=suggestion._id)
                suggestions.append({
                    'id': suggestion._id,
                    'name': suggestion.text,
                    'profile_picture': getattr(artist_doc, 'profile_picture', None),
                    'popularity': getattr(artist_doc, 'popularity', 0),
                    'source': 'completion',
                })
        
        if len(suggestions) < 5:
            search = ArtistDocument.search()
            search = search.query(
                Q('match', name__edge_ngram={'query': query})
            )
            
            remaining = 5 - len(suggestions)
            search = search[:remaining]
            search = search.sort('-popularity')
            
            response = search.execute()
            
            for hit in response:
                if not any(s['id'] == hit.meta.id for s in suggestions):
                    suggestions.append({
                        'id': hit.meta.id,
                        'name': hit.name,
                        'profile_picture': getattr(hit, 'profile_picture', None),
                        'popularity': getattr(hit, 'popularity', 0),
                        'source': 'search',
                    })
        
        suggestions.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        return Response(suggestions)