# coding: utf-8
import ujson as json
from monk.db import MonkQueue, MonkRedis
from redis import Redis
from monk.handler import MonkTask


def test_when_a_name_queue_to_defined_it_concat_a_prefix(mocker):
    mocker.patch("monk.db.db.redis.Redis")
    queue = MonkQueue("minha_fila")
    assert queue.queue_name == "monk:queue:minha_fila"


def test_when_none_name_to_defined(mocker):
    mocker.patch("monk.db.db.redis.Redis")
    queue = MonkQueue()
    assert queue.queue_name == "monk:queue"


def test_task_status_should_be_update_http_status(mocker):
    mock = mocker.patch("monk.db.db.redis.Redis")
    mock.return_value.get.return_value = json.dumps({
        "url": "http://siever.com",
        "klass": "Siever",
        "process_name": "siever",
        "callback": "anything",
        "use_phantomjs": False
    })

    def custom_set(key, value):
        assert key == "process:58e08e105e140306884070615ae8f637"
        value = json.loads(value)

        assert value['status'] == 200
        assert value['url'] == "http://siever.com"

    mock.return_value.set.side_effect = custom_set
    redis = MonkRedis()
    task = MonkTask(**{
        "url": "http://siever.com",
        "klass": "Siever",
        "process_name": "siever",
        "callback": "anything",
        "use_phantomjs": False
    })
    assert redis.task_status(task, 200)
    assert mock.return_value.set.called
    MonkRedis._db = None


def test_method_write_row(mocker):
    mock = mocker.patch("monk.db.db.redis.Redis")
    mock.return_value.get.return_value = json.dumps({
        "url": "http://s.com.br",
        "klass": "Si",
        "process_name": "si",
        "callback": "anything",
        "use_phantomjs": False,
        "to_csv": None,
        "status": 200
    })

    def custom_set2(key, value):
        assert key == "process:b8746f7c2d77cb09e242b34d9db94934"
        value = json.loads(value)

        assert value['status'] == 200
        assert value['url'] == "http://s.com.br"
        assert value['to_csv'][0] == "Sieve do Brasil"
        assert value['to_csv'][1] == "07/10/2016 0:47"

    mock.return_value.set.side_effect = custom_set2

    redis = MonkRedis()
    task = MonkTask(**{
        "url": "http://s.com.br"
    })

    assert redis.write_row(task, ("Sieve do Brasil", "07/10/2016 0:47"))
    MonkRedis._db = None


def test_empty_method_get_true_when_queue_is_empty(mocker):
    MonkQueue._db = None
    mocker.patch.object(Redis, "llen", return_value=0)

    redis = MonkQueue()
    assert redis.empty()


def test_empty_method_get_false_when_queue_isnot_empty(mocker):
    MonkQueue._db = None
    mocker.patch.object(Redis, "llen", return_value=1)

    redis = MonkQueue()
    assert redis.empty() is False
