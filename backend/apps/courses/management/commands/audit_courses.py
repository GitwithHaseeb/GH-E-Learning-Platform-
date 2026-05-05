from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand

from apps.courses.models import Course, CoursePhase, CoursePhaseQuiz, CourseStatus
from apps.courses.quizgen import course_domain, generate_phase_plan


STOP_WORDS = {
    "and",
    "for",
    "the",
    "with",
    "intro",
    "course",
    "phase",
    "basics",
    "advanced",
    "development",
    "engineering",
}


@dataclass
class AuditIssue:
    level: str
    slug: str
    phase: int | str
    kind: str
    detail: str


def _tokens(text: str) -> set[str]:
    words = (
        text.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(",", " ")
        .replace(".", " ")
        .split()
    )
    return {w for w in words if len(w) > 2 and w not in STOP_WORDS}


def _domain_from_url(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def _is_http(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def _url_ok(url: str, timeout_s: float = 6.0) -> tuple[bool, str]:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 course-audit-bot"})
    try:
        with urlopen(req, timeout=timeout_s) as resp:
            code = int(getattr(resp, "status", 200))
            if 200 <= code < 400:
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except Exception as exc:  # noqa: BLE001
        return False, type(exc).__name__


def _expected_domains(domain_key: str) -> set[str]:
    table = {
        "python": {"python.org", "freecodecamp.org", "realpython.com"},
        "web": {"developer.mozilla.org", "react.dev", "freecodecamp.org", "php.net"},
        "security": {"owasp.org", "nist.gov", "freecodecamp.org"},
        "blockchain": {"ethereum.org", "soliditylang.org", "freecodecamp.org"},
        "ai": {"ai.google", "microsoft.com", "coursera.org"},
        "ai_product": {"coursera.org", "mindtheproduct.com"},
        "general": {"freecodecamp.org", "classcentral.com", "coursera.org"},
    }
    return table.get(domain_key, table["general"])


class Command(BaseCommand):
    help = "Audit courses for links, topic matching, phases, and quiz quality."

    def add_arguments(self, parser):
        parser.add_argument(
            "--all-status",
            action="store_true",
            help="Audit all courses, not just published.",
        )
        parser.add_argument(
            "--no-network",
            action="store_true",
            help="Skip live URL health checks (faster).",
        )
        parser.add_argument(
            "--max-print",
            type=int,
            default=80,
            help="Maximum number of issues to print in detail.",
        )
        parser.add_argument(
            "--max-network-urls",
            type=int,
            default=60,
            help="Maximum unique URLs to live-check when network checks are enabled.",
        )

    def handle(self, *args, **options):
        all_status = bool(options["all_status"])
        no_network = bool(options["no_network"])
        max_print = int(options["max_print"])
        max_network_urls = int(options["max_network_urls"])

        qs = Course.objects.all().order_by("slug")
        if not all_status:
            qs = qs.filter(status=CourseStatus.PUBLISHED)

        issues: list[AuditIssue] = []
        checked_urls: dict[str, tuple[bool, str]] = {}

        for course in qs:
            expected_plan = generate_phase_plan(course.title)
            if len(expected_plan) != 5:
                issues.append(AuditIssue("error", course.slug, "-", "phase_count", "generated phase plan is not 5"))
                continue

            phase_rows = list(CoursePhase.objects.filter(course=course).order_by("phase_number"))
            if len(phase_rows) != 5:
                issues.append(
                    AuditIssue(
                        "warn",
                        course.slug,
                        "-",
                        "db_phase_count",
                        f"database has {len(phase_rows)} phases (expected 5)",
                    )
                )

            dom_key = course_domain(course.title)
            must_domains = _expected_domains(dom_key)

            for phase in expected_plan:
                phase_no = phase["phase_number"]
                topic = phase["title"]
                resources = phase.get("resources") or {}
                reading = resources.get("reading") or []
                videos = resources.get("videos") or []
                if not reading:
                    issues.append(AuditIssue("error", course.slug, phase_no, "reading_missing", "reading list empty"))
                if not videos:
                    issues.append(AuditIssue("warn", course.slug, phase_no, "video_missing", "video list empty"))

                # Validate URL format + relevance + health
                topic_tokens = _tokens(f"{course.title} {topic}")
                found_expected_domain = False
                for group_name, links in (("reading", reading), ("videos", videos)):
                    for row in links:
                        url = str((row or {}).get("url", ""))
                        title = str((row or {}).get("title", ""))
                        if not _is_http(url):
                            issues.append(AuditIssue("error", course.slug, phase_no, f"{group_name}_url", f"invalid url: {url!r}"))
                            continue

                        link_domain = _domain_from_url(url)
                        if any(d in link_domain for d in must_domains):
                            found_expected_domain = True

                        text_blob = f"{title} {url}".lower()
                        domain_hit = any(d in link_domain for d in must_domains)
                        if topic_tokens and (not any(tok in text_blob for tok in topic_tokens)) and (not domain_hit):
                            issues.append(
                                AuditIssue(
                                    "warn",
                                    course.slug,
                                    phase_no,
                                    f"{group_name}_relevance",
                                    f"weak topic match for '{title}'",
                                )
                            )

                        if not no_network:
                            if url not in checked_urls:
                                if len(checked_urls) >= max_network_urls:
                                    checked_urls[url] = (True, "SKIPPED_BY_CAP")
                                else:
                                    checked_urls[url] = _url_ok(url)
                            ok, msg = checked_urls[url]
                            if not ok:
                                issues.append(
                                    AuditIssue(
                                        "warn",
                                        course.slug,
                                        phase_no,
                                        f"{group_name}_health",
                                        f"{title}: {msg}",
                                    )
                                )

                if not found_expected_domain:
                    issues.append(
                        AuditIssue(
                            "warn",
                            course.slug,
                            phase_no,
                            "domain_match",
                            f"no expected domain matched for course domain '{dom_key}'",
                        )
                    )

                # Quiz quality checks from DB quiz row where available
                db_phase = next((p for p in phase_rows if p.phase_number == phase_no), None)
                if db_phase:
                    quiz = CoursePhaseQuiz.objects.filter(phase=db_phase).first()
                    if not quiz:
                        issues.append(AuditIssue("error", course.slug, phase_no, "quiz_missing", "quiz row missing"))
                        continue
                    qrows = quiz.questions or []
                    if len(qrows) != 30:
                        issues.append(AuditIssue("error", course.slug, phase_no, "quiz_count", f"{len(qrows)} questions (expected 30)"))
                    texts = [str(q.get("question", "")).strip().lower() for q in qrows]
                    unique_count = len(set(texts))
                    if unique_count < 24:
                        issues.append(
                            AuditIssue(
                                "warn",
                                course.slug,
                                phase_no,
                                "quiz_uniqueness",
                                f"only {unique_count}/30 unique question texts",
                            )
                        )
                    for i, q in enumerate(qrows, start=1):
                        opts = q.get("options") or []
                        ans = q.get("answer_index", -1)
                        if len(opts) != 4:
                            issues.append(AuditIssue("error", course.slug, phase_no, "quiz_options", f"Q{i} options={len(opts)}"))
                        if not isinstance(ans, int) or ans < 0 or ans > 3:
                            issues.append(AuditIssue("error", course.slug, phase_no, "quiz_answer_index", f"Q{i} answer_index={ans}"))

        err_count = sum(1 for x in issues if x.level == "error")
        warn_count = sum(1 for x in issues if x.level == "warn")
        total_courses = qs.count()

        self.stdout.write(self.style.SUCCESS(f"Audited courses: {total_courses}"))
        self.stdout.write(self.style.SUCCESS(f"Issues: {len(issues)} (errors={err_count}, warnings={warn_count})"))
        self.stdout.write(f"Network checks: {'disabled' if no_network else f'{len(checked_urls)} unique URLs checked'}")

        for row in issues[:max_print]:
            prefix = "ERROR" if row.level == "error" else "WARN "
            self.stdout.write(f"{prefix} | {row.slug} | phase={row.phase} | {row.kind} | {row.detail}")

        if len(issues) > max_print:
            self.stdout.write(f"... {len(issues) - max_print} more issues omitted")

        if err_count:
            raise SystemExit(1)
