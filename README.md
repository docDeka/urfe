# URFE – Освітній репозиторій навчальних матеріалів

## 🔍 Опис
URFE (Useful Repositories For Education) — це Django-застосунок, що дозволяє користувачам зберігати, систематизувати та переглядати навчальні матеріали, такі як лекції, категорії та інше.

## 💡 Можливості
- Реєстрація та авторизація користувачів
- Додавання / редагування / видалення матеріалів
- Категоризація матеріалів
- Перегляд матеріалів у зручній формі

## 🧱 Структура проекту
django-repo/
├── materials/... #файли які прикріпляють користувачі
├── media/... # медіа файли такі як аватари та фони
├── repo_project/... # тут знаходяться py-файли які треба для роботи сайту(settings.py, urls.py, __init__.py)
	urfe/
	├── pycache/ # файли для роботи сайту
	├── migrations/ # Міграції для роботи програми
	├── static/ # Статичні файли (CSS, JS)
	├── templates/urfe: # HTML шаблони для інтерфейсу
			base.html
			create_material.html
			edit_profile.html
			home.html
			login.html
			material_detail.html
			profile.html
			register.html
			welcome.html
	├──... # інші файли потрібні для роботи такі як: views.py, models.py, тощо.
├── .gitignore # файли які не потребують коміту
├── db.sqlite3 # база даних в якій зберігаються потрібні дані
├── manage.py # Django launcher
├── README.md - # інформація про проект та про те як зробити такий самий
├── requirements.txt - # завантажені бібліотеки
└── start_django.bat - # батник для швидкого запуску проекту
└── urfe/ # Налаштування проєкту (urls.py, settings.py)

## 🚀 Запуск
1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/docDeka/urfe.git
   cd urfe

2. Створити віртуальне середовище та активувати:
		python -m venv .venv
		.venv\Scripts\activate   # Для Windows

3. Встановити залежності:
		pip install -r requirements.txt

4. Запустити сервер:
		python manage.py runserver

📋 Автор
docDeka(Ygen(Ханейчук Дем'ян))

