from datetime import datetime, timezone

import pytest

from pp.utils import AwareDatetime, ISOFormat, Timestamp


def test_datetime():
    dt = AwareDatetime.now()
    assert dt.tzinfo == timezone.utc
    assert isinstance(dt, datetime)

    dt = AwareDatetime.utcnow()
    assert dt.tzinfo == timezone.utc
    assert isinstance(dt, datetime)


def test_isoformat():
    dt = ISOFormat.now()
    assert isinstance(dt, str)

    dt = ISOFormat.utcnow()
    assert isinstance(dt, str)


def test_timestamp():
    dt = Timestamp.now()
    assert isinstance(dt, float)

    dt = Timestamp.utcnow()
    assert isinstance(dt, float)


def test_datetime_types():
    with pytest.raises(ValueError, match="must be aware"):
        dt = AwareDatetime(2000, 1, 1)

    dt = AwareDatetime(2000, 1, 1, tzinfo=timezone.utc)
    assert dt.tzinfo == timezone.utc

    v1 = AwareDatetime.create(2000, 1, 1)
    v2 = ISOFormat.create(2000, 1, 1)
    v3 = Timestamp.create(2000, 1, 1)

    assert isinstance(v1, datetime)
    assert v1 == v2.to_datetime()
    assert v1 == v3.to_datetime()

    assert isinstance(v2, str)
    assert v2 == v1.to_isoformat()
    assert v2 == v3.to_isoformat()

    assert isinstance(v3, float)
    assert v3 == v1.to_timestamp()
    assert v3 == v2.to_timestamp()

    assert v2 == "2000-01-01T00:00:00+00:00"
