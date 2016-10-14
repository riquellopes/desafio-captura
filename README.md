Desafio Captura
===============

Resolvi batizar a aplicação com o nome [Monk](https://pt.wikipedia.org/wiki/Monk), uma referências ao seriado. Para
construir essa aplicação eu utilizei [python3.5](https://www.python.org)+[tornado](http://www.tornadoweb.org/en/stable/)+[redis](http://redis.io)+[lxml](http://lxml.de). Para orquestrar todos esses serviços eu utilizei [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/). Estando com tudo configurado corretamente, basta executar o comando abaixo.


## Documentation

### Build environment.

```bash
    $ docker-compose up

    # On MacOsx a first time
    $ docker-machine start
    $ docker-machine env
    $ eval $(docker-machine env)

    $ docke-compose up or docke-compose stop
```

### Environment variables.

```bash
    MONK_REDIS_HOST=monk-redis
    MONK_REDIS_PORT=6379
    MONK_REDIS_DB=0
```

### Process jobs.

```bash
  $ make container-task
```

### Run tests.

```bash
   $ make container-test
```

### Clean redis

```bash
   $ make clean-redis
```

### Build setup without container and process jobs

```bash
    $ make venv
    $ source venv/bin/activate
    $ make setup-local

    $ make test
    $ make test-cov
    $ make task

    $ ./worker.py # To run all tasks queued.
```
