import json
import hashlib
from enum import Enum
from datetime import datetime
from typing import Any, Optional


class MemoryType(str, Enum):
    STARTUP_IDEA = "startup_idea"
    MARKET_DATA = "market_data"
    COMPETITOR_DATA = "competitor_data"
    BUSINESS_STRATEGY = "business_strategy"
    INVESTOR_FEEDBACK = "investor_feedback"
    PITCH_DATA = "pitch_data"
    SCORES = "scores"
    HISTORY = "history"
    AGENT_OUTPUT = "agent_output"
    KNOWLEDGE_CONTEXT = "knowledge_context"


class MemoryEntry:
    def __init__(
        self,
        key: str,
        value: Any,
        memory_type: MemoryType,
        version: int = 1,
        source_agent: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        self.key = key
        self.value = value
        self.memory_type = memory_type
        self.version = version
        self.source_agent = source_agent
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = self.created_at
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        raw = f"{self.key}:{json.dumps(self.value, sort_keys=True, default=str)}:{self.version}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
            "memory_type": self.memory_type.value,
            "version": self.version,
            "source_agent": self.source_agent,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "hash": self.hash,
        }


class SharedMemory:
    def __init__(self, project_id: int):
        self.project_id = project_id
        self._store: dict[str, list[MemoryEntry]] = {}
        self._current_version: dict[str, int] = {}

    def set(self, key: str, value: Any, memory_type: MemoryType, source_agent: Optional[str] = None) -> MemoryEntry:
        version = self._current_version.get(key, 0) + 1
        self._current_version[key] = version

        entry = MemoryEntry(
            key=key,
            value=value,
            memory_type=memory_type,
            version=version,
            source_agent=source_agent,
        )

        if key not in self._store:
            self._store[key] = []
        self._store[key].append(entry)
        return entry

    def get(self, key: str, version: Optional[int] = None) -> Optional[MemoryEntry]:
        if key not in self._store:
            return None
        entries = self._store[key]
        if version is not None:
            for entry in entries:
                if entry.version == version:
                    return entry
            return None
        return entries[-1] if entries else None

    def get_latest(self, key: str) -> Optional[Any]:
        entry = self.get(key)
        return entry.value if entry else None

    def get_all_versions(self, key: str) -> list[MemoryEntry]:
        return self._store.get(key, [])

    def get_by_type(self, memory_type: MemoryType) -> dict[str, Any]:
        result = {}
        for key, entries in self._store.items():
            if entries and entries[-1].memory_type == memory_type:
                result[key] = entries[-1].value
        return result

    def get_all(self) -> dict[str, Any]:
        return {key: entries[-1].value for key, entries in self._store.items() if entries}

    def rollback(self, key: str, version: int) -> Optional[MemoryEntry]:
        if key not in self._store:
            return None
        for entry in self._store[key]:
            if entry.version == version:
                self._current_version[key] = version
                return entry
        return None

    def get_agent_context(self, agent_type: str) -> dict:
        context = self.get_all()
        context["_agent_type"] = agent_type
        context["_project_id"] = self.project_id
        return context

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "entries": {
                key: [entry.to_dict() for entry in entries]
                for key, entries in self._store.items()
            },
            "current_versions": self._current_version,
        }
