import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, make_m2m=True, **kwargs)
    return factory
    

@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory()

    response = client.get('/api/v1/courses/1/')
    assert response.status_code == 200

    data = response.json()
    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    courses = course_factory(_quantity=5)

    response = client.get('/api/v1/courses/')
    assert response.status_code == 200

    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_of_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[0]
    id_target_course = target_course.id

    response = client.get(f'/api/v1/courses/?id={id_target_course}')
    assert response.status_code == 200

    data = response.json()
    for course in data:
        assert course['id'] == id_target_course

    
@pytest.mark.django_db
def test_filter_of_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[0]
    name_target_course = target_course.name

    response = client.get(f'/api/v1/courses/?name={name_target_course}')
    assert response.status_code == 200

    data = response.json()
    for course in data:
        assert course['name'] == name_target_course


@pytest.mark.django_db
def test_post_course(client, student_factory):
    student_id = student_factory().id
    course = {
        'id': 1,
        'name': 'text',
        'students': student_id
    }

    response = client.post('/api/v1/courses/', course)
    assert response.status_code == 201

@pytest.mark.django_db
def test_patch_course(client, course_factory, student_factory):
    student_id = student_factory().id
    course = course_factory()
    data_for_update = {
        'name': 'testing update',
        'students': student_id
    }

    response = client.patch(f'/api/v1/courses/{course.id}/', data_for_update)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[0]

    response = client.delete(f'/api/v1/courses/{target_course.id}/')
    assert response.status_code == 204

    response = client.delete(f'/api/v1/courses/{target_course.id}/')
    assert response.status_code == 404

   