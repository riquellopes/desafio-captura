# coding: utf-8
from monk.db.redis import MonkRedis, task_queued


def test_get_true_when_exist_item_in_queue(mocker):
    mocker.patch.object(MonkRedis, "task_queued", return_value=True)
    assert task_queued("http://local")


def test_get_false_when_not_exist_item_in_queue(mocker):
    mocker.patch.object(MonkRedis, "task_queued", return_value=False)
    assert task_queued("http://local") is False
