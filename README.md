# **OrderCloser**

**OrderCloser** — это микросервис для автоматического управления заказами в системе **Smartomato**. 
Сервис принимает входящие API-запросы, обрабатывает их и выполняет действия через API Smartomato, 
такие как отмена новых заказов или закрытие подтверждённых заказов.

## **Функциональность**

1. **Приём API-запросов** через FastAPI:
    - Запросы приходят из другого сервиса на том же сервере (соседний контейнер).
2. **Отмена новых неоплаченных заказов**.
3. **Закрытие подтверждённых заказов**.
4. **Логирование** действий и ошибок с использованием библиотеки **loguru**.
5. **Взаимодействие с внешним API Smartomato**:
    - Получение списка заказов по статусу заказа и статусу оплаты.
    - Изменение статуса заказа.

---

## **Основные эндпоинты**

| Метод | URL                       | Описание                                                     |
|-------|---------------------------|--------------------------------------------------------------|
| POST  | `/orders/cancel-unpaid`   | Отменяет новые неоплаченные заказы(незадействован)           |
| POST  | `/orders/close-confirmed` | Закрывает подтверждённые заказы                              |
| POST  | `/orders/count`           | Возвращает кол-во заказов с определенным статусом(недопилен) |



### **Пример запроса**

**POST** `/orders/close-confirmed`:
```json
{
   "token": "aae434bc2f336032e9a99845c695b907"
}
```

---

## **Логирование**

Все действия и ошибки логируются с использованием **loguru**. Логи сохраняются в папке **`logs/`** 
с ротацией каждый день в 23:55 и хранением до 10 дней.

---

## **Docker**

### **Сборка Docker-образа**
```bash
docker build -t ordercloser .
```

### **Запуск контейнера**
```bash
docker run -p 8000:8000 ordercloser
```

---

## **Дальнейшие улучшения**

1. Добавить более детальные тесты.
2. Реализовать обработку повторных ошибок через **retry**.
3. Допилить получение кол-ва заказов с определенным статусом.