from elasticsearch import Elasticsearch
import numpy as np

ES_URL = 'http://elasticsearch:9200'
IMAGE_VECTOR_DIMENSION = 1000
MAPPINGS = {
    'mappings': {
        'properties': {
            'image_vector': {
                'type': 'dense_vector',
                'dims': IMAGE_VECTOR_DIMENSION
            }
        }
    }
}

class ElasticsearchInterface():
    def __init__(self, index_name):
        self.index_name = index_name
        self.es = Elasticsearch(ES_URL)

    def create_index(self):
        return self.es.indices.create(index=self.index_name, body={'mappings': MAPPINGS}, ignore=400)

    def index_image(self, image_vector):
        return self.es.index(index=self.index_name, body={"image_vector": self.to_list(image_vector)})

    def search_image(self, image_vector):
        body = {
            'query': {
                'script_score': {
                    'query': {
                        'match_all': {},
                    },
                    'script': {
                        'source': "cosineSimilarity(params.query_vector, doc['image_vector']) + 1.0",
                        'params': {
                            'query_vector': self.to_list(image_vector)
                        }
                    }
                }
            },
        }
        return self.es.search(index=self.index_name, body=body)

    def to_list(self, image_vector):
        return image_vector.tolist()[0]
