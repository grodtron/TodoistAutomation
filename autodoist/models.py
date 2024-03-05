import yaml
from typing import List, Optional, Any, Callable, cast
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


class Color(Enum):
    BERRY_RED = "berry_red"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    OLIVE_GREEN = "olive_green"
    LIME_GREEN = "lime_green"
    GREEN = "green"
    MINT_GREEN = "mint_green"
    TEAL = "teal"
    SKY_BLUE = "sky_blue"
    LIGHT_BLUE = "light_blue"
    BLUE = "blue"
    GRAPE = "grape"
    VIOLET = "violet"
    LAVENDER = "lavender"
    MAGENTA = "magenta"
    SALMON = "salmon"
    CHARCOAL = "charcoal"
    GREY = "grey"
    TAUPE = "taupe"


def ExcludeIfNone(value: Optional[Any]) -> bool:
    """Do not include field for None values"""
    return value is not None


def OptField(default_val: Optional[Any] = None) -> Any:
    return field(default=default_val, metadata=config(exclude=lambda x: ExcludeIfNone(x)))


def OptColorField(default_val: Optional[Color] = None) -> Any:
    return field(
        default=default_val,
        metadata=config(
            exclude=lambda x: ExcludeIfNone(x),
            encoder=lambda x: x.value,
            decoder=lambda x: Color(x)
        )
    )


@dataclass_json
@dataclass
class ConcreteTodoistLabel:
    name: str = OptField()
    color: Color = OptColorField()
    is_favorite: bool = OptField()
    id: Optional[int] = OptField()
    item_order: Optional[int] = OptField()
    is_deleted: Optional[bool] = OptField()

    def get_type(self) -> str:
        return "label"


@dataclass_json
@dataclass
class ConcreteTodoistFilter:
    name: str = OptField()
    query: str = OptField()
    color: Color = OptColorField()
    is_favorite: bool = OptField()
    id: Optional[int] = OptField()
    item_order: Optional[int] = OptField()
    is_deleted: Optional[bool] = OptField()

    def get_type(self) -> str:
        return "filter"


@dataclass_json
@dataclass
class ConcreteTodoistProject:
    name: str = OptField()
    color: Color = OptColorField()
    is_favorite: bool = OptField()
    id: Optional[int] = OptField()
    parent_id: Optional[int] = OptField()
    child_order: Optional[int] = OptField()
    collapsed: Optional[bool] = OptField()
    shared: Optional[bool] = OptField()
    sync_id: Optional[int] = OptField()
    is_deleted: Optional[bool] = OptField()
    is_archived: Optional[bool] = OptField()
    view_style: Optional[str] = OptField()
    created_at: Optional[str] = OptField()
    updated_at: Optional[str] = OptField()
    v2_id: Optional[str] = OptField()
    inbox_project: Optional[bool] = OptField()

    def get_type(self) -> str:
        return "project"


@dataclass_json
@dataclass
class ConcreteTodoistObjects:
    labels: List[ConcreteTodoistLabel] = field(default_factory=list)
    filters: List[ConcreteTodoistFilter] = field(default_factory=list)
    projects: List[ConcreteTodoistProject] = field(default_factory=list)

    def get_all_items(self) -> List[Any]:
        return self.labels + self.filters + self.projects


@dataclass_json
@dataclass
class TodoistLabel:
    name: str
    color: Color = OptColorField()
    is_favorite: bool = OptField()


@dataclass_json
@dataclass
class TodoistFilter:
    name: str
    query: str
    color: Color = OptColorField()
    is_favorite: bool = OptField()


@dataclass_json
@dataclass
class TodoistProject:
    name: str
    color: Color = OptColorField()
    is_favorite: bool = OptField()


@dataclass_json
@dataclass
class TodoistCollection:
    labels: List[TodoistLabel] = field(default_factory=list)
    filters: List[TodoistFilter] = field(default_factory=list)
    projects: List[TodoistProject] = field(default_factory=list)


@dataclass_json
@dataclass
class Context:
    name: str
    emojis: str = ""
    color: Color = OptColorField()


@dataclass_json
@dataclass
class CompositeContext:
    name: str
    emojis: str = ""
    color: Color = OptColorField()
    labels: List[str] = field(default_factory=list)


@dataclass_json
@dataclass
class ExclusionList:
    name: str
    color: Color = OptColorField()


@dataclass_json
@dataclass
class GTDState:
    contexts: List[Context] = field(default_factory=list)
    composite_contexts: List[CompositeContext] = field(default_factory=list)
    exclusion_lists: List[ExclusionList] = field(default_factory=list)


def load_gtd_state_from_yaml(yaml_data: str) -> GTDState:
    data = yaml.safe_load(yaml_data)
    return GTDState.from_dict(data)  # type: ignore
