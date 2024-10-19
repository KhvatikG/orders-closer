from tomato_api.change_order_status import change_order_status


def close_orders(orders: list, token: str):
    result = {
        "closed": 0,
        "total": len(orders),
        "problem_numbers": []
    }

    counter = 0

    for order in orders:
        counter += 1

        # Если удалось то change_order_status вернет True
        done = change_order_status(
            order=order,
            new_status='complete',
            token=token
        )

        # Считаем удачные
        if done: result["closed"] += 1
        else: result['problem_numbers'].append(order.get('number', 'неудалось получить номер'))
        print(f"Шаг {counter} из {result['total']}")

    print(f"Удалось закрыть {result['closed']} заказов из {result['total']}")
    if result["problem_numbers"]:
        print("Не удалось закрыть следующие заказы:")
        for order_num in result["problem_numbers"]:
            print(order_num)