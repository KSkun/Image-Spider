# Image-Spider

An image spider Python module for common image search engines. Part of software course project.

Root repo: https://github.com/KSkun/Image-Text-Nontext-Classifier-Service

## Features

### Spider

#### Baidu

The spider for Baidu makes use of a "next page" API which called by the original frontend when you scroll to the end of
current page.

URL: `GET https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word=<keyword>&pn=<page_start>&rn=<page_limit>`

Parameters:

- `word`: keyword to search for
- `pn`: the start index of this page, counting from 0
- `rn`: the number of results of this page, max value is about 100

The response will be a JSON document, the spider extracts `objURL` field for each result and decodes it. Decoding
algorithm can be found in [baidu.py](src/spider/baidu.py).

#### Google

The spider for Google uses Google's custom search engine service. Before deployment, you should set up the custom engine
and get an API key.

URL: `GET https://customsearch.googleapis.com/customsearch/v1?cx=<engine_id>&key=<api_key>&q=<keyword>&num=<page_limit>&start=<page_start>`

Parameters:

- `cx`: your custom search engine ID
- `key`: your API key
- `q`: keyword to search for
- `num`: the number of results of this page, max value is 10
- `start`: the start index of this page, counting from 1

The response will be a JSON document, the spider extracts `cse_image` field for each result.

#### Image Download

After crawling, the images will be downloaded and stored at `./workdir/tmp/<task ObjectId>/<image filename>`.

### Communication

The spider uses [redis stream](https://redis.io/topics/streams-intro) to receive crawling commands. It registers itself
to group `spider` of stream `spider_cmd`, and trys to fetch a command from the stream.

Command pattern: a single `cmd` field contains a JSON document string with fields below

- `task_id`: task ObjectId in MongoDB
- `operation`: operation, one of `init`, `crawl`
- `keyword`: keyword to search for
- `engines`: array of search engines to search for, element should be one of `baidu`, `google`
- `limit`: result count limit

To cooperate with backend and classifier, after crawling of each command, the spider creates image documents in `image`
collection.

### Tests

Unit tests are at `./test`. Includes function tests of spiders and consumer client.

## Configuration

### Local Startup

An example of working environment is in `./workdir`.

Config files store in `./workdir/config`, an example can be found as `default.json`.

Configuration steps:

1. Run `pip install -r requirements.txt`.
2. Set environment variable `CONFIG_FILE` to your config filename, if not set, it's `default.json`.
3. Create symlinks from image tmp directory to `./workdir`
4. Inside your config file, make sure the requirements below:
    1. `image_tmp_dir` set to your symlinks as step 3.
    2. `image_url` is your static resource site prefix.
    3. `mongo_xxx` is your global MongoDB settings.
    4. `redis_xxx` is your global Redis settings.
    5. `gg_xxx` is your Google custom search engine settings.
    6. `proxies` set to your proxy server address if needed.
5. Create a redis stream `spider_cmd` and a consumer group `spider` in your redis database.

   You can use an *init command* as `XADD spider_cmd * cmd "{\"operation\": \"init\"}"` to create the stream.
6. Run `python ../src/main.py` with working directory `./workdir`.

### Docker

See [docker configuration repo](https://github.com/KSkun/Image-Text-Nontext-Classifier-Service).