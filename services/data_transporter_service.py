from typing import Dict, List

channels: Dict[str, List] = {}


def listen(channel: str, func):
    if channel in channels:
        channels[channel].append(func)
    else:
        channels[channel] = [func]


def fire(channel: str, data):
    if channel in channels:
        for func in channels[channel]:
            func(data)
