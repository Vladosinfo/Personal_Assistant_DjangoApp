# Personal Assistant Web Application

Цей проєкт реалізує веб-додаток "Personal Assistant", який дозволяє зберігати контакти, нотатки, виконувати пошук, сортування, додаваня файлів, переглядання новин та багато іншого.

## Вміст

1. [Вступ](#вступ)
2. [Вимоги](#вимоги)
3. [Встановлення](#встановлення)
4. [Використання](#використання)
5. [Авторизація](#авторизація)
6. [Безпека](#безпека)
7. [Ліцензія](#ліцензія)

## Вступ

Цей проект є веб-інтерфейсом до персонального помічника, розробленого на основі курсу Python Web. Він включає ряд функціональних можливостей для керування контактами, нотатками, завантаженням файлів та інформацією з новин.

## Вимоги

- Зберігання контактів з іменами, адресами, номерами телефонів, email та днями народження.
- Виведення списку контактів з нагадуванням про дні народження.
- Валідація введеного номера телефону та email.
- Пошук контактів серед записів.
- Зберігання та управління нотатками з підтримкою тегів.
- Пошук та сортування нотаток за ключовими словами (тегами).
- Завантаження файлів користувача на сервер та фільтрація за категоріями (зображення, документи, відео тощо).
- Виведення короткого зведення новин за обраною тематикою (фінанси, погода).

## Встановлення

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/Vladosinfo/Personal_Assistant_DjangoApp
   cd project/

2. Instalation in consol: 
    create .env
    poetry install.
    docker run --name per_assist-postgres -p 5540:5432 -e POSTGRES_PASSWORD=changeme -d postgres
    docker ps
    docker exec -it per_assist-postgres bash
    psql -h localhost -U postgres
    CREATE DATABASE per_assist; 
    \l    - list of databases

3. Navigate to the project directory:
cd Personal_Assistant_DjangoApp/per_assist

4. Run the application:
python manage.py migrate
python manage.py runserver

5. Run in localhost:8000/:


## Використання
Після встановлення та запуску проекту ви зможете:

Додавати, редагувати та видаляти контакти та нотатки.
Завантажувати файли та фільтрувати їх за категоріями.
Отримувати зведення новин з обраної тематики.
Використовувати пошук та сортування для ефективного управління інформацією.

## Авторизація
Для доступу до функціоналу потрібно авторизуватись. Користувачі можуть створювати облікові записи та відновлювати паролі через email.

## Безпека
Всі критичні дані, такі як налаштування бази даних та інші конфіденційні дані, зберігаються у змінних середовищах і не зберігаються в репозиторії проекту.

## Ліцензія
This project is licensed under the BSD 2-Clause License.