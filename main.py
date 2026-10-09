import json
from datetime import date

FILE_NAME = "students.json"

START_DATE = date(2026, 10, 8)
END_DATE = date(2026, 10, 14)


def load_data():
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def find_student(data, roll_no):
    for student in data["students"]:
        if student["roll_no"] == roll_no:
            return student
    return None


def calculate_percentage(student):
    attendance = student["attendance"]
    total_days = len(attendance)

    if total_days == 0:
        return 0.0

    present_days = sum(
        1 for status in attendance.values() if status == "P"
    )

    return (present_days / total_days) * 100


def valid_date(date_text):
    try:
        parsed_date = date.fromisoformat(date_text)
        return START_DATE <= parsed_date <= END_DATE
    except ValueError:
        return False


def show_percentage(data, roll_no):
    student = find_student(data, roll_no)

    if student is None:
        print("Student not found.")
        return

    present_days = sum(
        1 for status in student["attendance"].values() if status == "P"
    )
    total_days = len(student["attendance"])
    percentage = calculate_percentage(student)

    print(f"Name: {student['name']}")
    print(f"Roll Number: {student['roll_no']}")
    print(f"Present Days: {present_days}")
    print(f"Recorded Days: {total_days}")
    print(f"Attendance Percentage: {percentage:.2f}%")


def check_attendance(data, roll_no, attendance_date):
    student = find_student(data, roll_no)

    if student is None:
        print("Student not found.")
        return

    status = student["attendance"].get(attendance_date)

    if status == "P":
        print(f"{student['name']} was PRESENT on {attendance_date}.")
    elif status == "A":
        print(f"{student['name']} was ABSENT on {attendance_date}.")
    else:
        print(f"No attendance record for {attendance_date}.")


def mark_attendance(data, roll_no, attendance_date, status):
    student = find_student(data, roll_no)

    if student is None:
        print("Student not found.")
        return

    if not valid_date(attendance_date):
        print("Date must be between 2026-10-08 and 2026-10-14.")
        return

    if status not in ("P", "A"):
        print("Status must be P (Present) or A (Absent).")
        return

    student["attendance"][attendance_date] = status
    save_data(data)

    print("Attendance updated successfully!")
    print(json.dumps(student, indent=2, ensure_ascii=False))


def remove_attendance(data, roll_no, attendance_date):
    student = find_student(data, roll_no)

    if student is None:
        print("Student not found.")
        return

    if attendance_date not in student["attendance"]:
        print("No attendance record exists for this date.")
        return

    del student["attendance"][attendance_date]
    save_data(data)

    print("Attendance record removed successfully!")
    print(json.dumps(student, indent=2, ensure_ascii=False))


def show_all(data):
    print("\n--- ATTENDANCE REPORT ---")

    for student in data["students"]:
        percentage = calculate_percentage(student)

        print(
            f"Roll No: {student['roll_no']} | "
            f"Name: {student['name']} | "
            f"Attendance: {percentage:.2f}%"
        )


def class_average(data):
    students = data["students"]

    if not students:
        print("No students available.")
        return

    percentages = [
        calculate_percentage(student) for student in students
    ]

    average = sum(percentages) / len(percentages)
    print(f"Class Average Attendance: {average:.2f}%")


def show_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    try:
        data = load_data()
    except FileNotFoundError:
        print("Error: students.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: students.json contains invalid JSON.")
        return

    print("\n=== ATTENDANCE MANAGEMENT SYSTEM ===")
    print("Commands:")
    print("percentage <roll_no>")
    print("check <roll_no> <YYYY-MM-DD>")
    print("mark <roll_no> <YYYY-MM-DD> <P/A>")
    print("remove <roll_no> <YYYY-MM-DD>")
    print("average")
    print("all")
    print("json")
    print("exit")

    while True:
        command = input("\nEnter command: ").strip()
        parts = command.split()

        if not parts:
            continue

        action = parts[0].lower()

        try:
            if action == "exit":
                print("Goodbye!")
                break

            elif action == "percentage" and len(parts) == 2:
                show_percentage(data, int(parts[1]))

            elif action == "check" and len(parts) == 3:
                check_attendance(data, int(parts[1]), parts[2])

            elif action == "mark" and len(parts) == 4:
                mark_attendance(
                    data, int(parts[1]), parts[2], parts[3].upper()
                )

            elif action == "remove" and len(parts) == 3:
                remove_attendance(data, int(parts[1]), parts[2])

            elif action == "average" and len(parts) == 1:
                class_average(data)

            elif action == "all" and len(parts) == 1:
                show_all(data)

            elif action == "json" and len(parts) == 1:
                show_json(data)

            else:
                print("Invalid command. Please use the listed commands.")

        except ValueError:
            print("Invalid roll number. Please enter a number.")

        except OSError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    main()