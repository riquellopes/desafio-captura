import pytest
from monk.exception import MonkException
from monk.handler import MonkTask


def test_should_be_get_value_when_property_index_call():
    task = MonkTask(**{
        "url": "http://siever.com",
        "klass": "Siever",
        "process_name": "siever",
        "callback": "anything",
        "use_phantomjs": False
    })

    assert task.callback == "anything"
    assert task.id == "58e08e105e140306884070615ae8f637"


def test_should_be_raise_when_url_does_not_exist():
    with pytest.raises(MonkException) as e:
        task = MonkTask(**{
            "klass": "Siever",
            "process_name": "siever",
            "callback": "anything",
            "use_phantomjs": False
        })
        task.id
    assert "Task doesn't have Url." in str(e.value)


def test_should_be_raise_when_property_not_exist():
    with pytest.raises(AttributeError):
        task = MonkTask(**{
            "url": "http://siever.com",
            "klass": "Siever",
            "process_name": "siever",
            "callback": "anything",
            "use_phantomjs": False
        })
        task.caubaque


def test_should_be_set_extra_index_in_process_response():
    task = MonkTask(**{
        "url": "http://siever.com",
        "klass": "Siever",
        "process_name": "siever",
        "callback": "anything",
        "use_phantomjs": False
    })

    process = task.to_process()
    assert process.processed is False
    assert process.status is None
    assert process.closed is False
    assert process.to_csv is None

    job = task.to_job()
    assert process != job
    assert "processed" not in job
    assert "status" not in job
    assert "closed" not in job
    assert "to_csv" not in job
