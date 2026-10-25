# Как применить подготовленный комплект ПР6 + ПР7

**Внимание:** ZIP — набор новых и изменённых файлов для существующего репозитория, а не независимая полная копия проекта. Исходные файлы, которых нет в архиве, остаются на месте.

1. Склонируйте репозиторий `https://github.com/pkpal-uhobp/electronic-invitations` или откройте его локальную копию.
2. Сохраните незакоммиченные изменения (`git status`); лучше создайте новую ветку:
   `git switch -c pr7-sql-and-error-pages`.
3. Распакуйте содержимое `electronic-invitations-pr6-pr7-update.zip` **в корень проекта рядом с `manage.py`**, соглашаясь с заменой существующих файлов.
4. Создайте venv, установите зависимости (`python -m pip install -r requirements.txt`).
5. Из корня проекта выполните:
   `python -m db.import_json`
   `python manage.py migrate`
   `python manage.py check`
   `pytest -q`
   `python manage.py runserver`
6. Проверьте `/events/search/?date=2026-12-28`, `/events/available/?event_id=1`, `/invitations/statistics/`.
7. Для кастомной 404 в режиме `DEBUG=False`:
   - Windows PowerShell: `$env:DJANGO_DEBUG='0'; $env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost,testserver'`;
   - затем `python manage.py runserver` и откройте `/no-such-page/`.
8. Проверьте `git diff`, после чего:
   `git add README.md db/ sql/ data/invitations.sqlite inviteweb/ homepage/ events_web/ invitations_web/ users_web/ guests_web/ templates/ tests/`
   `git commit -m "PR7: SQLite, SQL web pages and custom error handlers"`
   `git push -u origin pr7-sql-and-error-pages`

Для принятия Pull Request требуются права записи или право создавать ветку/PR из форка.
