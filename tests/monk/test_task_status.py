# coding: utf-8
from monk.db.redis import MonkRedis, task_status


def test_get_dict(mocker):
    mocker.patch.object(MonkRedis, "task_status", return_value={})
    assert task_status(mocker.MagicMock(), "okay") == {}
