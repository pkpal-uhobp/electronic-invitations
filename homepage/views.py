"""Главная страница и общий HTML-каркас веб-интерфейса ПР5."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с Bootstrap, CSS и общей навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
  <style>
    body {{ background: #f8f9fa; }}
    main {{ padding-top: 2rem; padding-bottom: 3rem; }}
    .app-card {{ border: 0; box-shadow: 0 .25rem 1rem rgba(0,0,0,.08); }}
  </style>
</head>
<body>
  <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="/">Приглашения</a>
      <div class="navbar-nav flex-row flex-wrap gap-1">
        <a class="nav-link" href="/events/">События</a>
        <a class="nav-link" href="/invitations/">Приглашения</a>
        <a class="nav-link" href="/users/">Пользователи</a>
        <a class="nav-link" href="/guests/">Гости</a>
      </div>
    </div>
  </nav>
  <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Показать главную страницу проекта."""
    content = """
    <div class="p-5 mb-4 bg-white rounded-3 app-card">
      <h1 class="display-5 fw-bold">Электронные приглашения</h1>
      <p class="lead mb-4">
        Веб-интерфейс учебного проекта: пользователи, гости, события и
        электронные приглашения.
      </p>
      <div class="d-flex flex-wrap gap-2">
        <a href="/events/" class="btn btn-primary btn-lg">События</a>
        <a href="/invitations/" class="btn btn-outline-primary btn-lg">
          Приглашения
        </a>
        <a href="/users/" class="btn btn-outline-secondary btn-lg">
          Пользователи
        </a>
        <a href="/guests/" class="btn btn-outline-secondary btn-lg">
          Гости
        </a>
      </div>
    </div>
    """
    return HttpResponse(page("Электронные приглашения", content))
