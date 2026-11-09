"""Демонстрация заданий 1 и 2 — ровно те проверки, что описаны в задании.

Запуск::

    python -m salon.demo

Каждый блок проверки начинается с пустого списка записей, поэтому
``len(appointments)`` в конце блока совпадает с ожидаемым результатом.
"""

from salon import appointments, create_appointment, reset_appointments


def show_appointments() -> None:
    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)


def task_1() -> None:
    print("=" * 60)
    print("Задание 1. Класс Appointment (запись клиента)")
    print("=" * 60)

    # Проверка 1: две корректные записи.
    reset_appointments()
    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")
    print("Тип возвращаемого значения:", type(first_appointment).__name__)
    show_appointments()
    print()

    # Проверка 2: частично не заполнены поля.
    reset_appointments()
    no_correct_appointment = create_appointment("", 1, 1, "12:00")
    print("Результат записи с пустым именем:", no_correct_appointment)
    print("Количество записей:", len(appointments))
    print()


def task_2() -> None:
    print("=" * 60)
    print("Задание 2. Запись только в часы работы салона: 08:00-20:00")
    print("=" * 60)

    # Проверка 1: две корректные записи.
    reset_appointments()
    create_appointment("Иванова А.А.", 1, 1, "10:00")
    create_appointment("Петрова А.А.", 1, 1, "11:00")
    show_appointments()
    print()

    # Проверка 2: некорректное время.
    reset_appointments()
    no_correct_appointment = create_appointment("Сидорова А.А.", 1, 1, "00:00")
    print("Результат записи на 00:00:", no_correct_appointment)
    print("Количество записей:", len(appointments))
    print()

    # Дополнительно: граничные значения правила 08:00-20:00.
    reset_appointments()
    print("08:00 ->", create_appointment("Сидорова А.А.", 1, 1, "08:00"))
    print("19:59 ->", create_appointment("Петрова А.А.", 1, 1, "19:59"))
    print("20:00 ->", create_appointment("Иванова А.А.", 1, 1, "20:00"))
    print("Количество записей:", len(appointments))
    print()

    # Дополнительно: одно время у разных мастеров — можно.
    reset_appointments()
    create_appointment("Иванова А.А.", 1, 1, "10:00")
    create_appointment("Петрова А.А.", 2, 2, "10:00")
    print("Два разных мастера на 10:00:")
    show_appointments()
    print("Количество записей:", len(appointments))


if __name__ == "__main__":
    task_1()
    print()
    task_2()
