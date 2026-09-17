from datetime import datetime

employees = []
next_id = 1


def create_employee(employee_data):
    global next_id

    employee = {
        "id": next_id,
        "name": employee_data.name.strip(),
        "email": str(employee_data.email),
        "department": employee_data.department.strip(),
        "primary_skill": employee_data.primary_skill.strip(),
        "location": employee_data.location.strip(),
        "work_mode": employee_data.work_mode,
        "is_active": employee_data.is_active,
        "created_at": datetime.now()
    }

    employees.append(employee)
    next_id += 1
    return employee


def get_all_employees():
    return employees


def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    return None


def update_employee(employee_id, employee_data):
    employee = get_employee(employee_id)

    if employee is None:
        return None

    update_data = employee_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if isinstance(value, str) and key in {
            "name", "department", "primary_skill", "location"
        }:
            value = value.strip()
        if key == "email":
            value = str(value)
        employee[key] = value

    return employee


def delete_employee(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return None

    employees.remove(employee)
    return employee
