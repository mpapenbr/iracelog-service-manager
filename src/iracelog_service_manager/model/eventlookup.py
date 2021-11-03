from dataclasses import dataclass, field
@dataclass
class EventLookup:
    lookup: dict = field(default_factory=dict)