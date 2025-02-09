# Проект YaMDb 

## Описание проекта 

Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Тимлид проекта Артём Куликов

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)

### Соавтор Кагиров Денис

tg: [@Denis_Kagirov](https://t.me/Denis_Kagirov)

[GitHub](https://github.com/KagirovDenis)

### Соавтор Львов Евгений

tg: [@Denis_Kagirov](https://t.me/jenique13)

[GitHub](https://github.com/DruNik88)

## Используемые технологии 

Проек реализован на языке python c использованием следюующих библиотек: 

* Django (v 3.2.16) 
* djangorestframework(v 3.12.4) 
* djangorestframework-simplejwt (v 5.3.1) 
* requests (v 2.26.0)

и др. 

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:berg96/api_yamdb.git
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Выполнить импорт данных из csv-фалов:
```
python manage.py csvall
```
Запустить проект:
```
python manage.py runserver
```

## [Документация](http://127.0.0.1:8000/redoc/)
