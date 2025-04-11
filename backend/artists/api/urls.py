from django.urls import path
from .views import ArtistSearchView, ArtistAutocompleteView, ArtistListView, ArtistDetailView

urlpatterns = [
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/<int:id>/', ArtistDetailView.as_view(), name='artist-detail'),

    path('artists/search/', ArtistSearchView.as_view(), name='artist-search'),
    path('artists/autocomplete/', ArtistAutocompleteView.as_view(), name='artist-autocomplete'),
]