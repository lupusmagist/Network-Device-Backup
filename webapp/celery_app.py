from webapp import init_celery

# app = init_celery(create_app())
app = init_celery()
app.conf.imports = app.conf.imports + ("webapp.tasks",)
