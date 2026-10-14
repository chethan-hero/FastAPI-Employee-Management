
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models import Employee, WorkItem


VALID_STATUSES = {"TODO", "IN_PROGRESS", "COMPLETED"}

ALLOWED_TRANSITIONS = {
    "TODO": {"IN_PROGRESS"},
    "IN_PROGRESS": {"COMPLETED"},
    "COMPLETED": set(),
}


class StatusTransitionError(Exception):
    """Raised when a work-item status transition is not allowed."""


def change_work_item_status(
    db: Session,
    work_item: WorkItem,
    new_status: str,
) -> WorkItem:
    """
    Validate and apply a status change.

    Requesting the current status again is treated as a no-op.
    """

    if new_status not in VALID_STATUSES:
        raise StatusTransitionError("Invalid work-item status")

    current_status = work_item.status

    if new_status == current_status:
        return work_item

    allowed = ALLOWED_TRANSITIONS.get(current_status, set())

    if new_status not in allowed:
        raise StatusTransitionError(
            f"Cannot change status from {current_status} "
            f"to {new_status}"
        )

    work_item.status = new_status
    return work_item


def update_work_item(
    db: Session,
    work_item_id: int,
    update_data: dict,
) -> WorkItem | None:
    """
    Update a work item.

    Use this function for PUT and PATCH so that both endpoints
    apply the same status-transition rules.
    """

    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        return None

    new_status = update_data.get("status")

    if new_status is not None:
        change_work_item_status(db, work_item, new_status)

    new_employee_id = update_data.get("employee_id")

    if new_employee_id is not None:
        employee = (
            db.query(Employee)
            .filter(Employee.id == new_employee_id)
            .first()
        )

        if employee is None:
            raise ValueError("Assigned employee does not exist")

    try:
        for field, value in update_data.items():
            if field == "status":
                continue

            if hasattr(work_item, field):
                setattr(work_item, field, value)

        db.commit()
        db.refresh(work_item)
        return work_item

    except Exception:
        db.rollback()
        raise


def get_employee_work_item_summary(
    db: Session,
    employee_id: int,
) -> dict | None:
    """
    Return status counts for an existing employee.

    Returns None if the employee does not exist.
    Counts are calculated by the database.
    """

    employee_exists = (
        db.query(Employee.id)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee_exists is None:
        return None

    result = (
        db.query(
            func.count(WorkItem.id).label("total_work_items"),
            func.coalesce(
                func.sum(
                    case(
                        (WorkItem.status == "TODO", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("todo"),
            func.coalesce(
                func.sum(
                    case(
                        (WorkItem.status == "IN_PROGRESS", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("in_progress"),
            func.coalesce(
                func.sum(
                    case(
                        (WorkItem.status == "COMPLETED", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("completed"),
        )
        .filter(WorkItem.employee_id == employee_id)
        .one()
    )

    return {
        "total_work_items": result.total_work_items,
        "todo": result.todo,
        "in_progress": result.in_progress,
        "completed": result.completed,
    }


def delete_work_item(
    db: Session,
    work_item_id: int,
) -> bool:
    """Delete a work item and return whether it existed."""

    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        return False

    try:
        db.delete(work_item)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
