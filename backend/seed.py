"""
Demo data seed — `USE_SQLITE=1 python seed.py` (backend folder se).
Yeh script Django setup karke categories, instructors, courses, lessons banata hai.
"""
import os
import random
from urllib.parse import quote_plus

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
os.environ.setdefault("USE_SQLITE", "1")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

from apps.courses.models import (  # noqa: E402
    Category,
    Course,
    CoursePhase,
    CoursePhaseQuiz,
    CourseLevel,
    CourseStatus,
    Lesson,
    LessonType,
    PricingType,
    Tag,
)
from apps.quizzes.models import Choice, Question, Quiz  # noqa: E402
from apps.courses.quizgen import build_phase_quiz, generate_course_profile, generate_phase_plan  # noqa: E402

User = get_user_model()


def course_image_prompt(title: str, hint: str) -> str:
    t = title.lower()
    words = (
        t.replace("-", " ")
        .replace("/", " ")
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )
    is_ai = "ai" in words or "prompt" in t or "machine learning" in t or "deep learning" in t
    if "blockchain" in t:
        return (
            f"{title}, blockchain network nodes, digital ledger, web3 interface illustration, "
            "professional elearning cover, no text"
        )
    if is_ai:
        return (
            f"{title}, futuristic ai chatbot interface, neural network, clean blue tech dashboard, "
            "professional elearning cover, no text"
        )
    if "web development" in t or "next.js" in t or "react" in t or "javascript" in t or "typescript" in t:
        return (
            f"{title}, modern web development workspace, code editor and website UI mockup, "
            "professional elearning cover, no text"
        )
    if "ethical hacking" in t or "cybersecurity" in t or "web application security" in t or "soc analyst" in t:
        return (
            f"{title}, cybersecurity operations center, shield lock, security dashboard, "
            "professional elearning cover, no text"
        )
    if "monitoring" in t or "grafana" in t or "prometheus" in t:
        return (
            f"{title}, monitoring analytics dashboard with charts and observability panels, "
            "professional elearning cover, no text"
        )
    if "mobile app" in t or "react native" in t or "flutter" in t:
        return (
            f"{title}, smartphone app design screens, modern mobile UI development workspace, "
            "professional elearning cover, no text"
        )
    if "dsa" in t or "system design" in t:
        return (
            f"{title}, software engineering architecture diagram, algorithms graph nodes, "
            "professional elearning cover, no text"
        )
    return f"{title} {hint}, modern technology elearning course cover, clean professional style, no text"


def main():
    # By default, preserve existing enrollments/users.
    # Set RESET_SEED=1 only when you intentionally want full reset.
    reset_seed = os.environ.get("RESET_SEED", "").lower() in ("1", "true", "yes")
    if reset_seed:
        CoursePhaseQuiz.objects.all().delete()
        CoursePhase.objects.all().delete()
        Quiz.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

    admin = User.objects.filter(email="admin@demo.com").first()
    if not admin:
        admin = User.objects.create_superuser("admin@demo.com", "Adminpass123!", role="admin")
    instructors = []
    for i in range(5):
        email = f"instructor{i}@demo.com"
        u = User.objects.filter(email=email).first()
        if not u:
            u = User.objects.create_user(
                email,
                "Teachpass123!",
                first_name=f"Instructor{i}",
                last_name="Team",
                role="instructor",
            )
        instructors.append(u)

    root, _ = Category.objects.get_or_create(name="Technology", slug="technology")
    root.description = "Engineering and software"
    root.save(update_fields=["description"])
    design, _ = Category.objects.get_or_create(name="Design", slug="design", parent=root)
    design.description = "UI/UX and product"
    design.save(update_fields=["description"])
    biz, _ = Category.objects.get_or_create(name="Marketing", slug="marketing")
    biz.description = "SEO and growth marketing"
    biz.save(update_fields=["description"])
    data, _ = Category.objects.get_or_create(name="Data", slug="data", parent=root)
    data.description = "Analytics and ML"
    data.save(update_fields=["description"])
    cloud, _ = Category.objects.get_or_create(name="Cloud & DevOps", slug="cloud-devops", parent=root)
    cloud.description = "Infra and CI/CD"
    cloud.save(update_fields=["description"])
    sec, _ = Category.objects.get_or_create(name="Cybersecurity", slug="cybersecurity", parent=root)
    sec.description = "Security engineering"
    sec.save(update_fields=["description"])

    tag_names = [
        "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Node.js", "Django",
        "SEO", "Marketing", "Product", "UI/UX", "DevOps", "Docker", "Kubernetes", "AWS",
        "Data Science", "Machine Learning", "Prompt Engineering", "Cybersecurity",
    ]
    tags = []
    for t in tag_names:
        tg, _ = Tag.objects.get_or_create(name=t, slug=t.lower().replace(" ", "-"))
        tags.append(tg)

    # 50 market-relevant free courses
    catalog = [
        ("Python for Beginners", root, CourseLevel.BEGINNER, 3, "python coding laptop ai generated artwork"),
        ("Advanced Python Automation", root, CourseLevel.EXPERT, 4, "python automation scripts dashboard"),
        ("Java Programming Foundations", root, CourseLevel.BEGINNER, 3, "java code on monitor"),
        ("Java Spring Boot APIs", root, CourseLevel.EXPERT, 4, "spring boot backend server"),
        ("C++ Fundamentals", root, CourseLevel.BEGINNER, 3, "c++ developer coding dark theme"),
        ("Modern C++ for Performance", root, CourseLevel.MASTER, 5, "high performance c++ architecture"),
        ("JavaScript Essentials", root, CourseLevel.BEGINNER, 2, "javascript frontend colorful code"),
        ("TypeScript in Practice", root, CourseLevel.INTERMEDIATE, 3, "typescript strict typing concept"),
        ("React 18 Complete Bootcamp", root, CourseLevel.INTERMEDIATE, 4, "react ui components dashboard"),
        ("Next.js Full Stack", root, CourseLevel.EXPERT, 4, "nextjs full stack web app"),
        ("Node.js Backend Engineering", root, CourseLevel.INTERMEDIATE, 4, "nodejs api microservices illustration"),
        ("Django REST API Masterclass", root, CourseLevel.EXPERT, 4, "django rest framework api server"),
        ("FastAPI and Async Python", root, CourseLevel.INTERMEDIATE, 3, "fastapi async architecture"),
        ("SQL for Developers", data, CourseLevel.BEGINNER, 2, "sql database queries dashboard"),
        ("PostgreSQL Optimization", data, CourseLevel.EXPERT, 3, "postgres query optimization chart"),
        ("Data Science with Python", data, CourseLevel.INTERMEDIATE, 4, "data science charts python"),
        ("Machine Learning Foundations", data, CourseLevel.INTERMEDIATE, 4, "machine learning neural network art"),
        ("Deep Learning Crash Course", data, CourseLevel.EXPERT, 5, "deep learning gpu visualization"),
        ("Prompt Engineering for AI", data, CourseLevel.BEGINNER, 2, "prompt engineering ai chatbot"),
        ("Generative AI Application Building", data, CourseLevel.EXPERT, 4, "generative ai app workflow"),
        ("SEO Fundamentals 2026", biz, CourseLevel.BEGINNER, 2, "seo analytics search ranking"),
        ("Technical SEO and Core Web Vitals", biz, CourseLevel.INTERMEDIATE, 3, "core web vitals performance graph"),
        ("Content Marketing Strategy", biz, CourseLevel.BEGINNER, 3, "content marketing planning board"),
        ("Social Media Marketing", biz, CourseLevel.BEGINNER, 2, "social media campaign dashboard"),
        ("Performance Marketing with Ads", biz, CourseLevel.INTERMEDIATE, 3, "digital ads optimization panel"),
        ("Growth Marketing Experiments", biz, CourseLevel.EXPERT, 4, "growth loops experiment framework"),
        ("Email Marketing Automation", biz, CourseLevel.INTERMEDIATE, 2, "email funnels automation visuals"),
        ("Product Marketing and Positioning", biz, CourseLevel.INTERMEDIATE, 3, "product positioning matrix"),
        ("UI/UX Design Basics", design, CourseLevel.BEGINNER, 2, "ui ux wireframe design system"),
        ("Figma for Product Designers", design, CourseLevel.INTERMEDIATE, 3, "figma prototype screens"),
        ("Design Systems at Scale", design, CourseLevel.EXPERT, 4, "design system components library"),
        ("UX Research Methods", design, CourseLevel.INTERMEDIATE, 3, "ux research interview journey map"),
        ("Cloud Computing with AWS", cloud, CourseLevel.INTERMEDIATE, 4, "aws cloud architecture diagram"),
        ("Docker for Developers", cloud, CourseLevel.BEGINNER, 2, "docker containers dev workflow"),
        ("Kubernetes Essentials", cloud, CourseLevel.INTERMEDIATE, 3, "kubernetes cluster nodes"),
        ("CI/CD with GitHub Actions", cloud, CourseLevel.INTERMEDIATE, 3, "ci cd pipeline automation"),
        ("Infrastructure as Code with Terraform", cloud, CourseLevel.EXPERT, 4, "terraform infrastructure modules"),
        ("Linux for DevOps", cloud, CourseLevel.BEGINNER, 2, "linux terminal server management"),
        ("Monitoring with Prometheus and Grafana", cloud, CourseLevel.EXPERT, 3, "prometheus grafana dashboards"),
        ("Cybersecurity Fundamentals", sec, CourseLevel.BEGINNER, 3, "cyber security lock network"),
        ("Web Application Security", sec, CourseLevel.INTERMEDIATE, 4, "web security shield browser"),
        ("Ethical Hacking Essentials", sec, CourseLevel.INTERMEDIATE, 4, "ethical hacking penetration testing"),
        ("SOC Analyst Starter Path", sec, CourseLevel.BEGINNER, 3, "soc analyst security operations"),
        ("Mobile App Development with Flutter", root, CourseLevel.INTERMEDIATE, 4, "flutter mobile app development"),
        ("React Native Practical", root, CourseLevel.INTERMEDIATE, 4, "react native mobile ui"),
        ("System Design for Engineers", root, CourseLevel.EXPERT, 5, "system design distributed systems"),
        ("DSA Interview Preparation", root, CourseLevel.INTERMEDIATE, 3, "data structures algorithms interview"),
        ("Blockchain Basics", root, CourseLevel.BEGINNER, 2, "blockchain decentralized network"),
        ("Web Development Intro", root, CourseLevel.INTERMEDIATE, 3, "web development modern ui coding"),
        ("AI Product Management", biz, CourseLevel.INTERMEDIATE, 3, "ai product roadmap planning"),
    ]

    # Legacy rename to keep old enrollments mapped
    legacy = Course.objects.filter(slug="web3-development-intro").first()
    if legacy and not Course.objects.filter(slug="web-development-intro").exists():
        legacy.title = "Web Development Intro"
        legacy.slug = "web-development-intro"
        legacy.save(update_fields=["title", "slug"])

    course_objs = []
    for idx, item in enumerate(catalog, start=1):
        title, cat, level, months, image_prompt = item
        slug = (
            title.lower()
            .replace("&", "and")
            .replace("/", " ")
            .replace("  ", " ")
            .replace(" ", "-")
        )
        ai_prompt = course_image_prompt(title, image_prompt)
        profile = generate_course_profile(title)
        inst = random.choice(instructors)
        c, _ = Course.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "subtitle": f"Industry-focused learning path in {months} month(s)",
                "description": (
                    f"This free course helps you learn {title} with a practical, project-first approach. "
                    "You will follow a guided 5-phase learning path with quick assessments after each phase, "
                    "and complete with a certificate."
                ),
                "learning_outcomes": profile["learning_outcomes"],
                "related_topics": profile["related_topics"],
                "requirements": profile["requirements"],
                "instructor": inst,
                "category": cat,
                "level": level,
                "pricing": PricingType.FREE,
                "price_cents": 0,
                "duration_minutes": months * 60 * 20,
                "duration_months": months,
                "thumbnail_url": "https://image.pollinations.ai/prompt/" + quote_plus(ai_prompt),
                "status": CourseStatus.PUBLISHED,
            },
        )
        c.tags.set(random.sample(tags, k=min(3, len(tags))))
        course_objs.append(c)

        # Rebuild lesson-phase content for this course only
        CoursePhaseQuiz.objects.filter(phase__course=c).delete()
        CoursePhase.objects.filter(course=c).delete()
        Lesson.objects.filter(course=c).delete()
        Quiz.objects.filter(course=c).delete()

        # 5 phases and quizzes
        plan = generate_phase_plan(title)
        for pmeta in plan:
            phase_no = pmeta["phase_number"]
            phase = CoursePhase.objects.create(
                course=c,
                phase_number=phase_no,
                title=pmeta["title"],
                description=pmeta["description"],
                content=pmeta["content"],
                resources=pmeta["resources"],
            )
            CoursePhaseQuiz.objects.create(
                phase=phase,
                questions=build_phase_quiz(title, phase_no, pmeta),
                pass_mark_percent=66,
            )

            Lesson.objects.create(
                course=c,
                title=f"{title} — Phase {phase_no} overview",
                order=phase_no,
                lesson_type=LessonType.ARTICLE,
                article_content=phase.content,
                duration_seconds=900,
                is_preview=(phase_no == 1),
            )

        qz = Quiz.objects.create(course=c, title=f"Quiz for {c.title}", pass_mark_percent=60)
        for qi in range(3):
            qu = Question.objects.create(quiz=qz, text=f"Q{qi+1}: 2+2=?", order=qi)
            Choice.objects.create(question=qu, text="3", is_correct=False)
            Choice.objects.create(question=qu, text="4", is_correct=True)

    print(f"Done. Admin: admin@demo.com / Adminpass123! | Courses: {len(course_objs)}")


if __name__ == "__main__":
    main()
