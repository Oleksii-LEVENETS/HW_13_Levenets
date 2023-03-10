# HW_17_Levenets_PythonPro_Redis, Django-cache, Pagination  
# HW_16_Levenets_PythonPro_Class based views, pagination
# HW_15_Levenets_PythonPro_Celery beat
# HW_14_Levenets_PythonPro_Celery, django_email
# HW_13_Levenets_PythonPro_annotate_aggregate
================================================  
ДЗ 17. Django Cache  
Заняття 18. Redis, Django-cache, Pagination

1. Основываясь на 15 дз добавить:
- Фикстуры для модели и связанной с ней моделью (Например посты и их автора, цитаты и их автора, автор и его книги,
города и их жители, и т.д.)
https://docs.djangoproject.com/en/4.1/ref/django-admin/#dumpdata
- Фикстуры хранить в папке fixtures
2. Альтернативно - написать менеджмент команду для генерации этих же данных из случайных значений.
Количество записей должно быть большим - 500-1000+.
3. Выводить это все на страницу, используя агрегацию/аннотация для кверисет, что бы добрать недостающие данные, 
в виде вложенного списка, таблицы или блоками.
4. Реализовать на странице пагинацию по большому количеству элементов (100-1000)
(все вышеперечисленное - намеренное ухудшение страницы, что бы хоть как-то оправдать кеширование)
5. Добавить кеширование на эту страницу, и остальные страницы для которых это "действительно имеет смысл".
Для кеширования используйте Redis + django-redis (или встроенный бекенд для редиса если Джанго версии 4+).

```bash
python3 manage.py migrate
```

# Option_1
# Менеджмент-команда create_new_models реализована через celery
```bash
celery -A core worker -l INFO  
```
```bash
./manage.py create_new_models  
```
```bash
./manage.py loaddata aggregation/fixtures/users.json
```

or

# Option_2
```bash
./manage.py loaddata aggregation/fixtures/fresh_db.json
```
```bash
python3 manage.py runserver
```


================================================
HW_16: Class based views, pagination.    
Заняття 17. Class based views, pagination  

1. Основываясь на 13 ДЗ добавить, используя только classbased views,  
- cтраницу создания объекта,  
- страницу редактирования объекта,
- страницу удаления объекта,  
- страницу просмотра объекта,  
- страницу просмотра списка объектов с пагинацией.  
(Для одной модели на ваш выбор)

2. Страница создания, изменения и удаление - login required. (используйте миксин)

Чеклист:
- models
- forms - optional
- views
- urls
- templates

```bash
python3 manage.py migrate
```
```bash
python3 manage.py runserver
```
```bash
./manage.py loaddata aggregation/fixtures/fresh_db.json
```

================================================
HW_15: Celery beat.  
Заняття 16. Celery, celery beat, parsing, BeautifulSoup  

1. Добавить модели Авторов и Цитат (не забываем о связях), и зарегистрируйте их в админке.
Использовать ресурс https://quotes.toscrape.com/  
2. Создать периодическую задачу которая будет добавлять по 5 НОВЫХ цитат (и их авторов с информацией) 
каждый нечетный час. Когда цитаты закончатся - отправьте "себе" уведомление по почте что больше нет цитат (в консоль).  

```bash
python3 manage.py runserver
```
```bash
python3 manage.py migrate
```
```bash
./manage.py loaddata aggregation/fixtures/fresh_db.json  # там user-Admin
```
```bash
celery -A core worker -B -l INFO
```

==============================================
HW_14: Celery, django_email.
Заняття 15. Celery, send_email.

1. Добавить страничку с формой (в базу ничего не сохранять, дизайн не важен - главное работоспособность).
Форма принимает три поля - почта, текст напоминания и датавремя когда это напоминание получить.
2. При отправки формы создается и откладывается задача, которая должна будет выполнится в указанное в форме время
и отправить напоминание на указанную в форму почту.

-- В теме письма можно указать просто "напоминание".
-- Датавремя - учитывайте разницу в таймзонах, но для этого задания это будет не критично.
-- Датавремя не может быть в прошлом, и не может быть более чем на 2 дня вперед.
-- celeryproject.org/en/master/userguide/calling.html#eta-and-countdown
-- Используйте отправку почты в консоль.

https://docs.celeryproject.org/en/stable/userguide/calling.html#eta-and-countdown
https://docs.djangoproject.com/en/4.1/topics/email/
https://docs.djangoproject.com/en/4.1/topics/i18n/timezones/
from django.utils import timezone
now = timezone.now()

```bash
python3 manage.py runserver
```
```bash
celery -A core worker -l INFO
```
```bash
celery -A core  inspect scheduled
```

==============================================
HW-13: annotate aggregate.
Lesson-14. Django-debug-toolbar, select_related, prefetch_related, aggregate, annotate, Q, F.
ДЗ 13. annotate aggregate
Створено: 03.02.2023 21:31
Заняття 14. Django-debug-toolbar, select_related, prefetch_related, aggregate, annotate, Q, F

1. Выполнять в новом приложении. Можете так же создать под это ДЗ новый репозиторий с новым проектом
(Не забыть все обязательные шаги - secret key, flake8, travis, gitignore, requirements, readme)
2. Добавить ddt (Django debug toolbar).
использовать в приложении модели из джанго доки
https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
3. заполнить базу большим количеством данных и предоставить мне возможность так же быстро заполнить базу
(сделайте оба варианта, но ожидаю как минимум один из):
   1) создать менеджмент команду
   2) создать фикстуры (dumpdata loaddata менеджмент команды) 
(только модель пользователя и новые модели из приложения)
4. Добавить модели в админку. Постараться использовать больше функционала 
(inline, фильтры, серчи, вывод и группировка полей в форме, filter_vertical, date_hierarchy ...)
5. создать несколько темплейтов, вьюшек, урлов для вывода данных по моделям.
(Только вывод данных из базы, без форм)
6. в вьюшках и темплейтах нужно стараться минимизировать количество запросов в базу. 
(Префетчи, селекты, аннотации, агрегации)
7. на страницах выводить списки (в таблицах) или единичный элемент - 
например список магазинов или одного автора. Помимо полей из модели обязательно выводить что-то ещё
полученное с использованием «Префетчи, селекты, аннотации, агрегации».
8. количество доступных страниц - 8 (по странице списка и странице элемента на каждую модель)
9. со списка можно попасть на страницу элемента по ссылке которую вы должны сгенерировать 
в темплейте для каждой страницы ({% url ... %}).
10. с дитейл страницы должна быть ссылка на список ({% url ... %}).

# Restore fresh DataBase
```bash
./manage.py loaddata aggregation/fixtures/fresh_db.json
```

or
# Creating fake 10 Authors, 10 Publishers, 500 Books, 10 Stores
```bash
./manage.py create_new_models 
```
# Creating fake 10 Users
```bash
./manage.py create_users 10
```
===============================