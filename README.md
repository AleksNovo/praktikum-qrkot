# QRKot - помощь котикам

Бэкенд приложения QRKot на FastAPI для благотворительного фонда, который занимается сбором пожертвований на различные цели, связанные с поддержкой кошек. Фонд использует собранные средства на медицинское обслуживание нуждающихся кошек, обустройство жилища для кошачьей колонии и кормление бездомных кошек.

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Через командную строку запустите проект:

```  
uvicorn app.main:app --reload 
```

## API  
Список доступных эндпоинтов в проекте c примерами запросов, варианты ответов и ошибок приведены в спецификации openapi.yml  или по эндпоинту /docs
