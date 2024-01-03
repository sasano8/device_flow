from datetime import datetime, timezone
from time import time


class Timestamp(float):
    @classmethod
    def create(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0):
        return Timestamp(
            AwareDatetime(year, month, day, hour, minute, second, microsecond, tzinfo=timezone.utc).timestamp()
        )

    @classmethod
    def now(cls):
        return cls(time())

    @classmethod
    def utcnow(cls):
        return cls(time())

    def to_datetime(self):
        return datetime.fromtimestamp(self, tz=timezone.utc)

    def to_isoformat(self):
        return self.to_datetime().isoformat()


class AwareDatetime(datetime):
    def __init__(self, *args, **kwargs):
        if not self.tzinfo:
            raise ValueError("AwareDatetime must be aware")

    @classmethod
    def create(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc):
        return cls(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo)

    @classmethod
    def now(cls, tz=timezone.utc):
        return super().now(tz=tz)

    @classmethod
    def utcnow(cls):
        return cls.fromtimestamp(time(), tz=timezone.utc)

    def to_timestamp(self):
        return Timestamp(self.timestamp())

    def to_isoformat(self):
        return ISOFormat(self.isoformat(), skip_validation=True)


class ISOFormat(str):
    def __new__(cls, object, skip_validation=False):
        if isinstance(object, cls):
            return object

        if not skip_validation:
            dt = datetime.fromisoformat(object)
            if not dt.tzinfo:
                raise ValueError(f"{object} is not an aware datetime")

        return super().__new__(cls, object)

    @classmethod
    def create(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc):
        return cls(
            AwareDatetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo).isoformat(),
            skip_validation=True,
        )

    @classmethod
    def now(cls, tz=timezone.utc):
        return cls(AwareDatetime.now(tz=tz).to_isoformat(), skip_validation=True)

    @classmethod
    def utcnow(cls):
        return cls(AwareDatetime.utcnow().to_isoformat(), skip_validation=True)

    def to_timestamp(self):
        return self.to_datetime().to_timestamp()

    def to_datetime(self):
        return AwareDatetime.fromisoformat(self)


utcnow_dt = AwareDatetime.utcnow
utcnow_float = Timestamp.utcnow
