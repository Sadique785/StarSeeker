from django.urls import path
from .views import ArtistSearchView, ArtistAutocompleteView

urlpatterns = [
    path('artists/search/', ArtistSearchView.as_view(), name='artist-search'),
    path('artists/autocomplete/', ArtistAutocompleteView.as_view(), name='artist-autocomplete'),
]