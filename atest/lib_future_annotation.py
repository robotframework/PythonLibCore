from __future__ import annotations

from typing_extensions import TypedDict

from robotlibcore import DynamicCore, keyword


class Location(TypedDict):
    longitude: float
    latitude: float


class lib_future_annotation(DynamicCore):

    def __init__(self) -> None:
        DynamicCore.__init__(self, [])

    @keyword
    def future_annotations(self, arg: Location):
        longitude = arg["longitude"]
        latitude = arg["latitude"]
        return f'{longitude} type({type(longitude)}), {latitude} {type(latitude)}'
