from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminCourseViewSet,
    AnnouncementViewSet,
    CategoryViewSet,
    CertificateViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    InstructorAnalyticsAPI,
    RequestCertificateAPI,
    LessonBookmarkViewSet,
    LessonNoteViewSet,
    LessonProgressViewSet,
    LessonViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("tags", TagViewSet)
router.register("courses", CourseViewSet)
router.register("admin/course-approvals", AdminCourseViewSet, basename="admin-course-approval")
router.register("lessons", LessonViewSet)
router.register("student/enrollments", EnrollmentViewSet, basename="student-enrollment")
router.register("student/progress", LessonProgressViewSet, basename="student-progress")
router.register("student/bookmarks", LessonBookmarkViewSet, basename="student-bookmark")
router.register("student/notes", LessonNoteViewSet, basename="student-note")
router.register("announcements", AnnouncementViewSet)
router.register("student/certificates", CertificateViewSet, basename="student-certificate")

urlpatterns = [
    path("", include(router.urls)),
    path("instructor/analytics/", InstructorAnalyticsAPI.as_view(), name="instructor-analytics"),
    path("student/certificates/request/", RequestCertificateAPI.as_view(), name="student-certificate-request"),
]
