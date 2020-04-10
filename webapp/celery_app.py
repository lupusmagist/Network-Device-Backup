from webapp import init_celery, create_app

app = init_celery(create_app())
app.conf.imports = app.conf.imports + ("webapp.tasks",)
