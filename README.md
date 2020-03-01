# The Graphicsearch

The Graphicsearch provides simple image search backend.

## Start the app

```bash
$ docker-compose up
```

## API Docs

Visit: [localhost:8000/redoc](http://localhost:8000/redoc)

## Create an index

You may need to create an index for the first time to access to the app.

```bash
$ docker-compose exec app bash -c "(echo 'from elasticsearch_interface import ElasticsearchInterface'; echo \"ElasticsearchInterface('image_net_b0').create_index()\") | python"
```

## Index an image

```bash
$ curl -XPOST -F file=@/path/to/image.jpg localhost:8000/index
```

## Search images

```bash
$ curl -XPOST -F file=@/path/to/image.jpg localhost:8000/search
```
