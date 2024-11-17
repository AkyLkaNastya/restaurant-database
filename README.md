# Предметная область

# Функциональные требования
### К базе данных:
[1] Возможность дополнения/изменения/удаления данных (например, добавить нового сотрудника и информацию о нём, обновить информацию о месте жительства, номер телефона и т.д. или формирование и добавление нового заказа, автоматическая генерация номера заказа, система должна автоматически связывать заказ со свободным сотрудником).
[2] Осуществление поиска по системе (например, найти поставщика, посмотреть поставляемый товар).
[3] Контроль за вместимостью (система должна проверять и обновлять оставшуюся вместимость склада для каждого ингредиента после выполнения каждого заказа/новой поставки).
Мониторинг остатка продуктов (система должна уведомлять о том, что товар скоро закончится, если его количества недостаточно для приготовления блюда).
Далее необязательные требования (со звёздочкой):
[4] Предоставление отчётов: система должна выдавать отчёты, например, о продажах за определённый период (расходы на продукты, зарплату сотрудников, выручку). 
[5] Экспорт данных: возможность экспортировать данные в CSV-файл.

### К приложению:
[1] Создание базы данных (на случай первого запуска приложения пользователем)
[2] Удаление базы данных
[3] Вывод содержимого таблиц
[4] Очистка таблиц (Частичная / полная)
[5] Добавление новых данных
[6] Поиск по текстовому не ключевому полю
[7] Обновление кортежа
[8] Удаление по заранее выбранному текстовому не ключевому полю
[9] Удаление конкретной записи, выбранной пользователем

# Количество таблиц: 8

# Нормальные формы базы данных
1: Все данные в таблицах атомарны. Мы рассматриваем ФИО и адрес только как цельную информацию, так как нам не важно есть ли среди персонала однофамильцы, тёзки и живут ли они на одной и той же улице. Нам важно только наличие этой информации.
2 и 3: Каждый столбец, не являющийся ключом, зависит от и только от первичного ключа. Стоимость ингредиентов определяем средней рыночной. У каждого индредиента возможен только один поставщик, чтобы избежать различия в качестве продуктов.