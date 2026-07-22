from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.test import TestCase

from .models import Teacher

User = get_user_model()


class TeacherUserCreationTests(TestCase):
    def test_creating_teacher_creates_user(self):
        teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            hire_date="2024-01-01",
        )
        self.assertIsNotNone(teacher.user)
        self.assertEqual(teacher.user.email, "john@example.com")
        self.assertEqual(teacher.user.first_name, "John")
        self.assertEqual(teacher.user.last_name, "Doe")
        self.assertTrue(teacher.user.has_usable_password() is False)

    def test_updating_teacher_does_not_create_another_user(self):
        teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            hire_date="2024-01-01",
        )
        first_user = teacher.user
        teacher.last_name = "Smith"
        teacher.save()
        teacher.refresh_from_db()
        self.assertEqual(teacher.user, first_user)
        self.assertEqual(User.objects.count(), 1)

    def test_existing_user_with_same_email_is_linked(self):
        existing = User.objects.create_user(
            username="existinguser",
            email="jane@example.com",
            password="testpass123",
        )
        teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            hire_date="2024-01-01",
        )
        self.assertEqual(teacher.user, existing)
        self.assertEqual(User.objects.count(), 1)

    def test_user_and_teacher_are_connected_via_onetoone(self):
        teacher = Teacher.objects.create(
            first_name="Alice",
            last_name="Brown",
            email="alice@example.com",
            hire_date="2024-01-01",
        )
        self.assertEqual(teacher.user.teacher_profile, teacher)

    def test_missing_email_does_not_create_user(self):
        teacher = Teacher.objects.create(
            first_name="No",
            last_name="Email",
            email="",
            hire_date="2024-01-01",
        )
        teacher.refresh_from_db()
        self.assertIsNone(teacher.user)

    def test_transaction_rollback_on_user_failure(self):
        with self.assertRaises(Exception):
            with transaction.atomic():
                teacher = Teacher(first_name="Fail", last_name="User", email="fail@example.com", hire_date="2024-01-01")
                teacher.save()
                raise RuntimeError("Force rollback")
        self.assertFalse(Teacher.objects.filter(email="fail@example.com").exists())
        self.assertFalse(User.objects.filter(email="fail@example.com").exists())

    def test_user_creation_with_duplicate_username_base(self):
        User.objects.create_user(username="test", email="other@example.com")
        teacher = Teacher.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            hire_date="2024-01-01",
        )
        self.assertIsNotNone(teacher.user)
        self.assertNotEqual(teacher.user.username, "test")
        self.assertTrue(teacher.user.username.startswith("test_"))

    def test_teacher_with_preassigned_user_skips_creation(self):
        existing_user = User.objects.create_user(
            username="preassigned", email="pre@example.com", password="testpass"
        )
        teacher = Teacher.objects.create(
            first_name="Pre",
            last_name="Assigned",
            email="pre@example.com",
            hire_date="2024-01-01",
            user=existing_user,
        )
        teacher.refresh_from_db()
        self.assertEqual(teacher.user, existing_user)
        self.assertEqual(User.objects.count(), 1)
