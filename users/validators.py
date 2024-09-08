from rest_framework import serializers


class TimeOffsetValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_offset = dict(value).get(self.field)
        if time_offset is None:
            return

        if -12 < time_offset < 14:
            raise serializers.ValidationError("Wrong time offset")
