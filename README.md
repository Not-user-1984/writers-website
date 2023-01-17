

# **Моя версия учебного проекта яндекса Yatube** 
#### **Стек**
![python version](https://img.shields.io/badge/Python-3.10-green)
![django version](https://img.shields.io/badge/Django-4.1-green)
![pillow version](https://img.shields.io/badge/Pillow-8.3-green)
![pytest version](https://img.shields.io/badge/pytest-6.2-green)
![requests version](https://img.shields.io/badge/requests-2.26-green)
![sorl-thumbnail version](https://img.shields.io/badge/thumbnail-12.7-green)
### **Описание**
Социальная сеть блогеров. **Учебный проект**.
Сообщество для публикаций. Блог с возможностью публикации постов, подпиской на группы и авторов, а также комментированием постов.
<details>
<summary>
<b>Запуск проекта в dev-режиме 
</summary>
Инструкция ориентирована на операционную систему windows и утилиту git bash.<br/>
Для прочих инструментов используйте аналоги команд для вашего окружения.

1. Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/Banes31/hw05_final.git
```

```
cd hw05_final
```

2. Установите и активируйте виртуальное окружение
```
python -m venv venv
``` 
```
source venv/Scripts/activate
```

3. Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

4. В папке с файлом manage.py выполните миграции:
```
python manage.py migrate
```

5. В папке с файлом manage.py запустите сервер, выполнив команду:
```
python manage.py runserver
```
</details>

<details>
<summary>
<b>Что могут делать пользователи 
</summary>
Что могут делать пользователи

  **Залогиненные** пользователи могут:
  1. Просматривать, публиковать, удалять и редактировать свои публикации;
  2. Просматривать информацию о сообществах;
  3. Просматривать и публиковать комментарии от своего имени к публикациям других пользователей *(включая самого себя)*, удалять и          редактировать **свои** комментарии;
  4. Подписываться на других пользователей и просматривать **свои** подписки.<br/>
  ***Примечание***: Доступ ко всем операциям записи, обновления и удаления доступны только после аутентификации и получения токена.

  **Анонимные :alien:** пользователи могут:
  1. Просматривать публикации;
  2. Просматривать информацию о сообществах;
  3. Просматривать комментарии;
</details>

<details>
<summary>
<b>Набор доступных эндпоинтов
</summary>

* ```posts/``` - Отображение постов и публикаций (_GET, POST_);
* ```posts/{id}``` - Получение, изменение, удаление поста с соответствующим **id** (_GET, PUT, PATCH, DELETE_);
* ```posts/{post_id}/comments/``` - Получение комментариев к посту с соответствующим **post_id** и публикация новых комментариев(_GET, POST_);
* ```posts/{post_id}/comments/{id}``` - Получение, изменение, удаление комментария с соответствующим **id** к посту с соответствующим **post_id** (_GET, PUT, PATCH, DELETE_);
* ```posts/groups/``` - Получение описания зарегестрированных сообществ (_GET_);
* ```posts/groups/{id}/``` - Получение описания сообщества с соответствующим **id** (_GET_);
* ```posts/follow/``` - Получение информации о подписках текущего пользователя, создание новой подписки на пользователя (_GET, POST_).<br/>
</details>

### **Мои доработки**

### **Автор**
[Дима Плужников](https://github.com/Banes31)
