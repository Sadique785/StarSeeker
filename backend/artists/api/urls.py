from django.urls import path
from .views import ArtistSearchView, ArtistAutocompleteView, ArtistListView

urlpatterns = [
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/search/', ArtistSearchView.as_view(), name='artist-search'),
    path('artists/autocomplete/', ArtistAutocompleteView.as_view(), name='artist-autocomplete'),
]