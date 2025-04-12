from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter
from .models import Artist

# Custom analyzer
edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer='standard',
    filter=['lowercase', token_filter('edge_ngram_filter', type='edge_ngram', min_gram=1, max_gram=20)]
)

@registry.register_document
class ArtistDocument(Document):
    name = fields.TextField(
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
            'edge_ngram': fields.TextField(analyzer=edge_ngram_analyzer),
            'suggest': fields.CompletionField(),  
        }
    )
    genre = fields.TextField()
    profile_picture = fields.TextField()
    location = fields.TextField()
    popularity = fields.IntegerField(attr='get_popularity')  # Remove the default parameter
    
    class Index:
        name = 'artists'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'analyzer': {
                    'edge_ngram_analyzer': {
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'edge_ngram_filter']
                    }
                },
                'filter': {
                    'edge_ngram_filter': {
                        'type': 'edge_ngram',
                        'min_gram': 1,
                        'max_gram': 20
                    }
                }
            }
        }
    
    class Django:
        model = Artist
        fields = []
    
    def prepare_popularity(self, instance):

        try:
            return instance.get_popularity()
        except (AttributeError, TypeError):
            return 0