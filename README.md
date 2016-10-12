Desafio Captura
===============

Resolvi batizar a aplicação com o nome [Monk](https://pt.wikipedia.org/wiki/Monk), uma referências ao seriado. Para
construir essa aplicação eu utilizei [python3.5](https://www.python.org)+[tornado](http://www.tornadoweb.org/en/stable/)+[redis](http://redis.io)+[lxml](http://lxml.de). Para orquestrar todos esses serviços eu utilizei [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/). Estando com tudo configurado corretamente, basta executar o comando abaixo.

## Respostas:
- O monk já foi modelado pesando nesse cenário. Talvez depois de analisar eu só precise ter mais workers rodando,
para aumentar a velocidade da scraping.
- Eu usaria o phantomjs.
- Eu usaria um proxy para maquiar a origem da requisição.
- O scraping é um solução paleativa, para o cliente/site que não possui um xml/api/soap que possa ser consultado,
para não concorrer com os acessos do site. Eu diminuiria a quantidade de acessos diários e negociaria com cliente para que ele disponibilize esse conteúdo em um xml talvez.


## Documentação

### Criar ambiente.

```bash
    $ docker-compose up

    # No MacOsx a primeira vez
    $ docker-machine start
    $ docker-machine env
    $ eval $(docker-machine env)

    $ docke-compose up or docke-compose stop
```

### Variavéis de ambiente.

```bash
    MONK_REDIS_HOST=monk-redis
    MONK_REDIS_PORT=6379
    MONK_REDIS_DB=0
```

### Processar tarefas.

```bash
  $ make container-task
```

### Executar testes.

```bash
   $ make container-test
```

### Limpar redis

```bash
   $ make clean-redis
```

## Referências proxy:
    - http://proxymesh.com
    - http://www.ninjasproxy.com
    - https://www.hidemyass.com
    - https://www.proxyrain.com/pricing
    - https://scrapinghub.com
