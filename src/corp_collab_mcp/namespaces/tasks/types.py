"""Types for tasks namespace."""

from enum import Enum

from pydantic import BaseModel, Field

from corp_collab_mcp.types.common import UserIdentity


class TaskStatus(str, Enum):
    """Task status."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskComment(BaseModel):
    """Task comment."""

    id: str
    author: UserIdentity
    content: str
    created_at: str
    updated_at: str | None = None


class Task(BaseModel):
    """Task/Issue representation."""

    id: str
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    assignee: UserIdentity | None = None
    reporter: UserIdentity
    project: str | None = None
    labels: list[str] | None = None
    due_date: str | None = None
    created_at: str
    updated_at: str
    comments: list[TaskComment] | None = None
    parent_id: str | None = None
    subtasks: list["Task"] | None = None
    metadata: dict[str, str] | None = None


class CreateTaskRequest(BaseModel):
    """Request to create a new task."""

    title: str = Field(..., min_length=1)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: str | None = None
    project: str | None = None
    labels: list[str] | None = None
    due_date: str | None = None
    parent_id: str | None = None


class UpdateTaskRequest(BaseModel):
    """Request to update a task."""

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: str | None = None
    labels: list[str] | None = None
    due_date: str | None = None


class SearchTasksRequest(BaseModel):
    """Request to search tasks."""

    query: str | None = None
    status: list[TaskStatus] | None = None
    priority: list[TaskPriority] | None = None
    assignee_id: str | None = None
    reporter_id: str | None = None
    project: str | None = None
    labels: list[str] | None = None
    limit: int = Field(default=20, ge=1, le=100)


# Update forward references
Task.model_rebuild()
