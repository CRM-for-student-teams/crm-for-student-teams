from conftest import (
    api_client,
    auth_client_client,
    auth_client_student_captain,
    auth_client_student_member,
    user_client,
    user_student_captain,
    user_student_member,
)


from apps.projects.models import Project, Task
from apps.teams.models import CustomUser
from apps.projects.conftest import project, task

def test_project_list():
    pass

def test_project_fetch():
    pass

def test_project_create(user_student_captain, auth_client_student_captain):
    pass

def test_project_update(user_student_captain, auth_client_student_captain, project):
    pass

def test_project_delete(user_student_captain, auth_client_student_captain, project):
    pass


def test_task_list():
    pass

def test_task_fetch():
    pass

def test_task_create(user_student_member, auth_client_student_member):
    pass

def test_task_update(user_student_member, auth_client_student_member, task):
    pass

def test_task_delete(user_student_member, auth_client_student_member, task):
    pass


