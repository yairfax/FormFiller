from model import *
from xeger import Xeger

x = Xeger()

def parse_to_ast(data) -> AST:
    match data:
        case {"url": url, "actions": actions}:
            if not url:
                raise TypeError("url cannot be empty")
            return AST(url, parse_actionlist(actions))
        case _:
            raise TypeError(f"error parsing to ast: {data}")

def parse_actionlist(data) -> list[Action]:
    match data:
        case [dict(obj), *rest]:
            return [parse_action(obj)] + parse_actionlist(rest)
        case []:
            return []
        case _:
            raise TypeError(f"error in parsing action list: {data}")

def parse_action(data) -> Action:
    match data:
        case {"data": list(points)}:
            return DataEntryAction(parse_dataentry(points))
        case {"click": rest}:
            return parse_click_action(rest)
        case {"sleep": time}:
            return SleepAction(time)
        case _:
            raise TypeError(f"unrecognized action: {data}")

def parse_click_action(data) -> ClickAction:
    match data:
        case {"id": str(btn), **rest}:
            return ClickAction(btn, parse_wait(rest), FieldType.ID)
        case {"name": str(btn), **rest}:
            return ClickAction(btn, parse_wait(rest), FieldType.NAME)
        case _:
            raise TypeError(f"error parsing click action: {data}")

def parse_wait(data) -> bool:
    match data:
        case {"wait": bool(wait)}:
            return wait
        case {}:
            return True
        case _:
            raise TypeError(f"error parsing wait: {data}")        

def parse_dataentry(data) -> list[DataPoint]:
    match data:
        case [{"name": name, "value": value}, *rest]:
            return [DataPoint(name, parse_datapoint(value), FieldType.NAME)] + parse_dataentry(rest)
        case [{"id": name, "value": value}, *rest]:
            return [DataPoint(name, parse_datapoint(value), FieldType.ID)] + parse_dataentry(rest)
        case []:
            return []
        case _:
            raise TypeError(f"error in parsing data entry: {data}")

def parse_datapoint(data) -> str:
    match data:
        case str(val):
            return val
        case {"regex": str(val)}:
            return x.xeger(val)
        case _:
            raise TypeError(f"unrecognized data point: {data}")