# coding: utf-8
from monk.db import MonkQueue
from monk.monk import MonkWorker


def test_property_queue_get_MonkQueue_instancie(mocker):
    mm = MonkWorker(mocker.MagicMock())
    assert isinstance(mm.queue, MonkQueue)
