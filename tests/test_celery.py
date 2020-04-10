import pytest

from webapp.tasks.celery_tasks import dummy_task
# from webapp.celery_app import dummy_task


@pytest.mark.usefixtures('celery_session_app')
@pytest.mark.usefixtures('celery_session_worker')
def test_example():
    """Simply test our dummy task using celery"""
    res = dummy_task.delay()
    assert res.get() == "OK"
