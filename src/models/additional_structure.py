# --- import section --- #
from enum import Enum
from dataclasses import dataclass
from typing import Any 
from typing import Optional

class EslabonStatus(str, Enum):
    AVAILABLE = "Available"
    RUNNING = "Running"
    UNASSIGNED = "Unassigned"

class TaskStatus(str, Enum):
    PENDING     = "pending"
    RUNNING     = "running"
    DONE        = "done"
    FAILED      = "failed"
    CANCELLED   = "cancelled"

# Data clases
@dataclass
class TaskInfo:
    task_id: str
    method_name: str
    status: TaskStatus
    result: Any = None
    error: Optional[Exception] = None
    created_at: float = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
