from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from omegaconf import MISSING

@dataclass
class VariableSchema:
    states: Dict[str, int] = field(default_factory=dict)

@dataclass
class VariablesSchema:
    variables: Dict[str, VariableSchema] = field(default_factory=dict)