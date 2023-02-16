
# stripe_django_test

Ссылка на проект http://51.250.84.205:8000/

Данные для входа в админку: 
```
Логин - admin
Пароль - test
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Bogdan-Malina/stripe_django_test
```

```
cd stripe_django_test
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Обновить pip в виртуальном окружении
```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
```
```
python manage.py migrate
```
Создать .env файл в директории stripe_test
```
STRIPE_PUBLIC_KEY=(Находится в личном кабинете на stripe.com)
STRIPE_SECRET_KEY=(Находится в личном кабинете на stripe.com)
STRIPE_WEBHOOK_SECRET=(Находится в личном кабинете на stripe.com)
SECRET_KEY=(Ключ приложения django)
```

Запустить проект:

```
python manage.py runserver
```


## Бонусные задачи:

- ✓ Запуск используя Docker 

- ✓ Использование environment variables 

- ✓ Просмотр Django Моделей в Django Admin панели 

- ✓ Запуск приложения на удаленном сервере, доступном для тестирования 

- ✓ Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items 

- ✓ Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 

- ☒ Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте

- ✓ Реализовать не Stripe Session, а Stripe Payment Intent.


