# The Graphicsearch

The Graphicsearch privides simple image search backend.

## Build the image

```bash
$ docker build -t graphicsearch .
```

## Start the app

```bash
$ docker-compose up -d
```

## Create an index

You may need to create an index for the first time to access to the app.

```bash
$ docker-compose exec app bash -c "(echo 'from elasticsearch_interface import ElasticsearchInterface'; echo \"ElasticsearchInterface('image_net_b0').create_index()\") | python"
```

## Index an image

```bash
$ curl -XPOST -F file=@/path/to/image.jpg localhost:5000
```

## Search images

```bash
$ curl -XPOST -F file=@/path/to/image.jpg localhost:5000/search
```
