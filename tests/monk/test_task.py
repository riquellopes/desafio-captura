import pytest
from monk.handler import MonkTask


def test_should_be_get_value_when_property_index_call():
    monk = MonkTask(**{
        "url": "http://siever.com",
        "klass": "Siever",
        "process_name": "siever",
        "callback": "anything",
        "use_phantomjs": False
    })

    assert monk.callback == "anything"


def test_should_be_raise_when_property_not_exist():
    with pytest.raises(AttributeError):
        monk = MonkTask(**{
            "url": "http://siever.com",
            "klass": "Siever",
            "process_name": "siever",
            "callback": "anything",
            "use_phantomjs": False
        })
        monk.caubaque
