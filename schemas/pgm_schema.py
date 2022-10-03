from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from omegaconf import MISSING

@dataclass
class PGMCPD:
    probabilities: List[List[float]] = field(default_factory=list)
    evidence: Optional[List[str]] = None
    evidence_card: Optional[List[int]] = None

@dataclass
class PGMModel:
    edges: List[List[str]] = field(default_factory=list)
    cpd: Dict[str, PGMCPD] = field(default_factory=dict)