"""Course phase reading plans + unique 30-MCQ quiz generation."""

from __future__ import annotations

from urllib.parse import quote_plus

from .course_resources import final_learning_profile
from .quiz_banks import QUIZ_BANK_VERSION, _shuffle_options, diversify_with_readings, pick_bank


def _contains_word(text: str, word: str) -> bool:
    parts = (
        text.replace("-", " ")
        .replace("/", " ")
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )
    return word.lower() in [p.lower() for p in parts]


def _stable_video_links(course_title: str, topic: str, videos: list[tuple[str, str]] | list[dict]) -> list[dict]:
    """
    Return resilient video links.
    We intentionally route to scoped YouTube search URLs so links don't die when specific video IDs are removed.
    """
    out: list[dict] = []
    for item in videos[:3]:
        if isinstance(item, dict):
            title = item.get("title", "Video lesson")
        else:
            title = item[0]
        query = quote_plus(f"{course_title} {topic} {title}")
        out.append(
            {
                "title": f"{title} (YouTube search)",
                "url": f"https://www.youtube.com/results?search_query={query}",
            }
        )
    # Always include one broad fallback
    broad_query = quote_plus(f"{course_title} {topic} full tutorial")
    out.append(
        {
            "title": f"{topic} full tutorial (YouTube search)",
            "url": f"https://www.youtube.com/results?search_query={broad_query}",
        }
    )
    return out


def _stable_reading_links(course_title: str, topic: str, readings: list[tuple[str, str]] | list[dict]) -> list[dict]:
    """
    Return globally trusted, topic-specific reading links.
    Includes official docs + FreeCodeCamp topic pages (search/news/learn) for self-learning.
    """
    t = topic.lower()
    c = course_title.lower()
    out: list[dict] = []

    # Add topic-accurate, high-signal global learning links.
    def add(title: str, url: str) -> None:
        out.append({"title": title, "url": url})

    q = quote_plus(f"{course_title} {topic}")
    fcc_q = quote_plus(f"{topic} {course_title} freecodecamp")

    # First link must land on the exact topic page user is currently reading.
    topic_page: tuple[str, str] | None = None
    if ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and "html" in t:
        topic_page = ("Topic page — HTML basics", "https://developer.mozilla.org/en-US/docs/Learn/HTML")
    elif ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and (
        "css" in t or "tailwind" in t or "bootstrap" in t
    ):
        topic_page = ("Topic page — CSS layout", "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout")
    elif ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and ("javascript" in t or "dom" in t):
        topic_page = ("Topic page — JavaScript guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide")
    elif ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and "react" in t:
        topic_page = ("Topic page — React Learn", "https://react.dev/learn")
    elif ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and "php" in t:
        topic_page = ("Topic page — PHP getting started", "https://www.php.net/manual/en/getting-started.php")
    elif ("web" in c or "javascript" in c or "react" in c or "typescript" in c) and "mysql" in t:
        topic_page = ("Topic page — MySQL tutorial", "https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/")
    elif ("flutter" in c) and "dart" in t:
        topic_page = ("Topic page — Dart language", "https://dart.dev/language")
    elif ("flutter" in c) and "widget" in t:
        topic_page = ("Topic page — Flutter widgets", "https://docs.flutter.dev/ui/widgets")
    elif ("flutter" in c) and "layout" in t:
        topic_page = ("Topic page — Flutter layout", "https://docs.flutter.dev/ui/layout")
    elif ("flutter" in c) and ("state management" in t or "state" in t):
        topic_page = ("Topic page — Flutter state management", "https://docs.flutter.dev/data-and-backend/state-mgmt")
    elif ("flutter" in c) and ("networking" in t or "json" in t):
        topic_page = ("Topic page — Flutter networking", "https://docs.flutter.dev/data-and-backend/networking")
    elif ("flutter" in c) and ("deployment" in t or "release" in t):
        topic_page = ("Topic page — Flutter deployment", "https://docs.flutter.dev/deployment")
    elif ("system design" in c) and ("requirements" in t or "cap theorem" in t):
        topic_page = ("Topic page — System Design Primer", "https://github.com/donnemartin/system-design-primer")
    elif ("system design" in c) and ("database" in t or "sharding" in t):
        topic_page = ("Topic page — DDIA notes", "https://dataintensive.net/")
    elif ("security" in c or "hacking" in c or "soc" in c) and "owasp" in t:
        topic_page = ("Topic page — OWASP Top 10", "https://owasp.org/www-project-top-ten/")
    elif "kubernetes" in c and "kubernetes" in t:
        topic_page = ("Topic page — Kubernetes concepts", "https://kubernetes.io/docs/concepts/")
    elif "docker" in c and ("dockerfile" in t or "container" in t):
        topic_page = ("Topic page — Docker get started", "https://docs.docker.com/get-started/")
    elif "terraform" in c and "terraform" in t:
        topic_page = ("Topic page — Terraform docs", "https://developer.hashicorp.com/terraform/docs")
    elif "python" in c and "python" in t:
        topic_page = ("Topic page — Python tutorial", "https://docs.python.org/3/tutorial/")

    if topic_page:
        add(topic_page[0], topic_page[1])

    if "python" in c or "python" in t:
        add("freeCodeCamp — Scientific Computing with Python", "https://www.freecodecamp.org/learn/scientific-computing-with-python/")
        add("freeCodeCamp — Python topic articles", f"https://www.freecodecamp.org/news/search/?query={quote_plus(topic + ' python')}")
        add("Python docs tutorial", "https://docs.python.org/3/tutorial/")
    elif "web" in c or "html" in t or "css" in t or "javascript" in t or "react" in t:
        add("freeCodeCamp — Responsive Web Design", "https://www.freecodecamp.org/learn/2022/responsive-web-design/")
        add("freeCodeCamp — JavaScript Algorithms and Data Structures", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/")
        add("MDN Web Docs", "https://developer.mozilla.org/en-US/docs/Learn")
    elif "flutter" in c or "dart" in t:
        add("Flutter official docs", "https://docs.flutter.dev/")
        add("Dart language docs", "https://dart.dev/language")
        add("freeCodeCamp — Flutter topic articles", "https://www.freecodecamp.org/news/search/?query=flutter")
    elif "react native" in c or "expo" in t:
        add("React Native official docs", "https://reactnative.dev/docs/getting-started")
        add("Expo docs", "https://docs.expo.dev/")
        add("freeCodeCamp — React Native topic articles", "https://www.freecodecamp.org/news/search/?query=react%20native")
    elif "security" in c or "owasp" in t or "soc" in c:
        add("OWASP Top 10", "https://owasp.org/www-project-top-ten/")
        add("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework")
        add("freeCodeCamp — Cybersecurity topic articles", "https://www.freecodecamp.org/news/search/?query=cybersecurity")
    elif "blockchain" in c or "web3" in c:
        add("Ethereum developer docs", "https://ethereum.org/en/developers/docs/")
        add("Solidity docs", "https://docs.soliditylang.org/")
        add("freeCodeCamp — Blockchain topic articles", "https://www.freecodecamp.org/news/search/?query=blockchain")
    elif "sql" in c or "postgres" in c or "mysql" in t:
        add("PostgreSQL docs", "https://www.postgresql.org/docs/current/")
        add("MySQL tutorial", "https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/")
        add("freeCodeCamp — SQL topic articles", "https://www.freecodecamp.org/news/search/?query=sql")
    elif "docker" in c:
        add("Docker docs", "https://docs.docker.com/get-started/")
        add("freeCodeCamp — Docker topic articles", "https://www.freecodecamp.org/news/search/?query=docker")
    elif "kubernetes" in c:
        add("Kubernetes docs", "https://kubernetes.io/docs/home/")
        add("freeCodeCamp — Kubernetes topic articles", "https://www.freecodecamp.org/news/search/?query=kubernetes")
    elif "terraform" in c:
        add("Terraform docs", "https://developer.hashicorp.com/terraform/docs")
        add("freeCodeCamp — Terraform topic articles", "https://www.freecodecamp.org/news/search/?query=terraform")
    elif "seo" in c or "marketing" in c:
        add("Google Search Central docs", "https://developers.google.com/search/docs")
        add("HubSpot marketing resources", "https://blog.hubspot.com/marketing")
        add("freeCodeCamp — SEO/marketing topic articles", "https://www.freecodecamp.org/news/search/?query=seo")
    else:
        add("freeCodeCamp — topic search", f"https://www.freecodecamp.org/news/search/?query={fcc_q}")
        add("Class Central — topic search", f"https://www.classcentral.com/search?q={q}")

    # Keep existing curated links too (official docs from course_resources).
    for item in readings[:4]:
        if isinstance(item, dict):
            title = item.get("title", "Learning resource")
            url = item.get("url", "")
        else:
            title, url = item
        if url:
            out.append({"title": title, "url": url})

    # De-duplicate while preserving order.
    dedup: list[dict] = []
    seen: set[str] = set()
    for row in out:
        url = row.get("url", "")
        if url and url not in seen:
            seen.add(url)
            dedup.append(row)
    return dedup[:6]


def generate_course_profile(course_title: str) -> dict:
    """Return detail-page sections for every course."""
    t = course_title.lower()
    if "python" in t:
        return {
            "learning_outcomes": [
                "Understand what Python is and where it is used in industry.",
                "Write and run your first Python program on your machine.",
                "Use variables, loops, conditions, and functions correctly.",
                "Read and debug beginner-level Python scripts confidently.",
                "Build small practical scripts and mini projects.",
                "Prepare for intermediate topics like OOP and frameworks.",
            ],
            "related_topics": ["Python", "Automation", "Backend Development", "Data Handling", "Problem Solving"],
            "requirements": [
                "A computer with Python 3 installed.",
                "Basic text editor or IDE (VS Code recommended).",
                "No prior coding experience required.",
            ],
        }
    if "blockchain" in t:
        return {
            "learning_outcomes": [
                "Understand blockchain fundamentals and distributed ledgers.",
                "Learn blocks, hashing, consensus, and transactions.",
                "Understand wallets, gas fees, and smart contract basics.",
                "Explore real-world Web3 use-cases and architecture.",
                "Understand security pitfalls in smart contract systems.",
            ],
            "related_topics": ["Blockchain", "Web3", "Smart Contracts", "Cryptography", "Decentralization"],
            "requirements": [
                "Basic understanding of programming concepts is helpful.",
                "Internet connection for docs and test networks.",
                "No crypto investment is required for this course.",
            ],
        }
    if "security" in t or "hacking" in t or "soc" in t:
        return {
            "learning_outcomes": [
                "Understand cybersecurity foundations and attacker mindset.",
                "Identify common web and network vulnerabilities.",
                "Use basic defensive techniques and secure configurations.",
                "Read logs and detect suspicious behavior patterns.",
                "Understand incident response and reporting workflow.",
            ],
            "related_topics": ["Cyber Security", "OWASP", "Threat Detection", "SIEM", "Incident Response"],
            "requirements": [
                "Basic computer and networking understanding.",
                "Willingness to practice in ethical/legal boundaries.",
                "No hacking experience required for beginner paths.",
            ],
        }
    if _contains_word(t, "ai") or "machine" in t or "prompt" in t:
        return {
            "learning_outcomes": [
                "Understand AI concepts and model capabilities.",
                "Create high-quality prompts for practical tasks.",
                "Evaluate AI outputs using clear quality criteria.",
                "Design AI workflows for product/business use-cases.",
                "Understand responsible AI and common limitations.",
            ],
            "related_topics": ["Artificial Intelligence", "Prompting", "LLMs", "AI Products", "Evaluation"],
            "requirements": [
                "Basic computer and internet usage.",
                "Curiosity to test prompts and iterate.",
                "No ML math background required for this track.",
            ],
        }
    if "flutter" in t or ("mobile" in t and "flutter" in t):
        return {
            "learning_outcomes": [
                "Install Flutter and use Dart for cross-platform UI code.",
                "Build layouts with core widgets and Material Design.",
                "Apply state management patterns suited to small and medium apps.",
                "Fetch data, parse JSON, and persist local data safely.",
                "Prepare builds for Android/iOS stores with performance awareness.",
            ],
            "related_topics": ["Flutter", "Dart", "Material", "Widgets", "Mobile", "APIs", "Play Store", "App Store"],
            "requirements": ["A computer with Android Studio or VS Code.", "Basic programming logic helps.", "No prior mobile experience required."],
        }
    if "react native" in t:
        return {
            "learning_outcomes": [
                "Set up Expo / React Native and understand core native-mapped components.",
                "Navigate between screens and structure app folders.",
                "Manage state with hooks and context patterns.",
                "Connect to APIs and handle offline-friendly patterns.",
                "Ship builds to testers and app stores with confidence.",
            ],
            "related_topics": ["React Native", "Expo", "JavaScript", "Mobile", "Navigation", "APIs"],
            "requirements": ["Node.js LTS installed.", "JavaScript fundamentals recommended.", "macOS or Windows with Android/iOS tooling as needed."],
        }
    if "web" in t or "react" in t or "javascript" in t or "typescript" in t:
        return {
            "learning_outcomes": [
                "Understand complete frontend foundations: HTML, CSS, JavaScript.",
                "Build responsive interfaces using Bootstrap and Tailwind CSS.",
                "Create dynamic frontend apps using React component architecture.",
                "Understand form handling, routing, and API data rendering.",
                "Build practical backend basics with PHP and MySQL integration.",
                "Connect frontend and backend into a full web development workflow.",
            ],
            "related_topics": [
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Bootstrap",
                "Tailwind CSS",
                "PHP",
                "MySQL",
                "Web Architecture",
            ],
            "requirements": [
                "A browser and code editor.",
                "Basic understanding of computer file structure.",
                "No prior framework experience required.",
            ],
        }
    return {
        "learning_outcomes": [
            "Understand core concepts and practical workflow.",
            "Apply concepts through guided hands-on tasks.",
            "Build confidence by completing phased milestones.",
            "Develop problem-solving and debugging habits.",
            "Finish with applied knowledge you can use in projects.",
        ],
        "related_topics": ["Technology", "Practical Skills", "Problem Solving", "Project Workflow"],
        "requirements": [
            "A computer with internet access.",
            "Basic willingness to practice consistently.",
        ],
    }


def generate_phase_plan(course_title: str) -> list[dict]:
    """Return 5-phase reading plan with topic-accurate resources (see course_resources)."""
    pack = final_learning_profile(course_title)
    stack = pack["stack"]
    phases_resources = pack["phases_resources"]

    phases = []
    for i in range(1, 6):
        topic = stack[i - 1]
        pr = phases_resources[i - 1]
        readings = _stable_reading_links(course_title, topic, pr["readings"])
        phase_videos = _stable_video_links(course_title, topic, pr["videos"])
        data_points = [
            f"Phase {i} workload target: 5-7 study hours/week.",
            f"Expected completion benchmark for phase {i}: 66%+ quiz score (20/30+ correct).",
            f"Recommended note count for phase {i}: 15-25 key points.",
        ]
        phases.append(
            {
                "phase_number": i,
                "title": f"Phase {i}: {topic}",
                "description": f"Study {topic} for {course_title}, then clear the phase quiz.",
                "content": (
                    f"# {course_title} — Phase {i}: {topic}\n\n"
                    f"## Reading goal\nUnderstand **{topic}** and connect it to real-world use in {course_title}.\n\n"
                    "## Topics to cover\n"
                    f"- Core concept: {topic}\n"
                    f"- Common mistakes in {topic}\n"
                    f"- Practical application task\n\n"
                    "## Weekly study plan\n"
                    "- Day 1-2: Read docs + take notes\n"
                    "- Day 3-4: Do guided practice\n"
                    "- Day 5-6: Build mini exercise\n"
                    "- Day 7: Attempt phase quiz (30 MCQs)\n\n"
                    "Use the **reading** and **video** links below — they open the official lessons and playlists for this phase.\n\n"
                    "After passing this quiz, the next phase will be unlocked."
                ),
                "resources": {
                    "reading": readings,
                    "videos": phase_videos,
                    "data_points": data_points,
                    "practice_tasks": [
                        f"Create one mini task based on {topic}.",
                        f"Write summary notes for {topic}.",
                        "Attempt self-check questions before quiz.",
                    ],
                },
                "keywords": [topic, course_title, "official documentation", "hands-on practice"],
            }
        )
    return phases


def course_domain(course_title: str) -> str:
    """Match domain keys used by phase plans and MCQ banks."""
    t = course_title.lower()
    if "flutter" in t or "react native" in t:
        return "general"
    if "blockchain" in t:
        return "blockchain"
    if "python" in t:
        return "python"
    if "web" in t or "react" in t or "javascript" in t or "typescript" in t:
        return "web"
    if "security" in t or "hacking" in t or "soc" in t:
        return "security"
    if _contains_word(t, "ai") or "machine" in t or "prompt" in t:
        return "ai_product" if "product management" in t else "ai"
    return "general"


def merge_phase_meta(course_title: str, phase_obj) -> dict:
    """Merge DB phase row with generated plan defaults for quiz generation."""
    plan = generate_phase_plan(course_title)
    row = next((p for p in plan if p["phase_number"] == getattr(phase_obj, "phase_number", 0)), plan[0])
    res = getattr(phase_obj, "resources", None) or row.get("resources") or {}
    return {
        "phase_number": getattr(phase_obj, "phase_number", row.get("phase_number")),
        "title": getattr(phase_obj, "title", None) or row.get("title", ""),
        "description": getattr(phase_obj, "description", None) or row.get("description", ""),
        "resources": res,
        "keywords": row.get("keywords") or [],
    }


def needs_quiz_refresh(questions: list | None) -> bool:
    if not questions or len(questions) != 30:
        return True
    if (questions[0] or {}).get("bank_version") != QUIZ_BANK_VERSION:
        return True
    q0 = (questions[0].get("question") or "").lower()
    if "best approach for best practices" in q0 or "best approach for common pitfalls" in q0:
        return True
    return False


def _template_bank_30(course_title: str, phase_number: int, phase_meta: dict, domain: str) -> list[dict]:
    """Fallback MCQs for general catalog courses — unique per phase via reading anchors."""
    readings = (phase_meta.get("resources") or {}).get("reading") or []
    titles = [r.get("title", "Official documentation") for r in readings if isinstance(r, dict)] or [
        "Course syllabus",
        "Hands-on practice",
        "Industry examples",
    ]
    topic = phase_meta.get("title") or f"Phase {phase_number}"
    stems = [
        (
            "While studying {topic}, what is the best use of the reading resource “{doc}”?",
            [
                "Skim headings, reproduce one documented example, and note definitions in your own words.",
                "Use it only as a bookmark without applying any steps.",
                "Assume the resource replaces all practice exercises for the phase.",
                "Copy long sections verbatim without testing or summarizing.",
            ],
            0,
        ),
        (
            "For {course_title} ({topic}), which habit best prevents gaps before the phase quiz?",
            [
                "Keep a checklist of concepts you can explain without looking at notes.",
                "Avoid writing notes to save time.",
                "Study only the night before the quiz.",
                "Skip self-check questions listed in the phase plan.",
            ],
            0,
        ),
        (
            "When a phase resource links to “{doc}”, what should you verify after reading?",
            [
                "You can restate the core idea and relate it to one deliverable in this phase.",
                "You memorized the URL string exactly.",
                "You only watched thumbnails of linked pages.",
                "You collected unrelated trivia from other domains.",
            ],
            0,
        ),
        (
            "Which workflow matches professional learning for {topic}?",
            [
                "Read → mini exercise → self-quiz → review mistakes → retry weak areas.",
                "Quiz first, then optionally read if time remains.",
                "Read once with no practice because quizzes are random.",
                "Avoid exercises because documentation is enough.",
            ],
            0,
        ),
        (
            "If instructions in “{doc}” conflict with a random blog post, what should you trust for this course?",
            [
                "Trust the official/primary resource listed in this phase first, then cross-check carefully.",
                "Always trust the newest social post.",
                "Pick whichever is shorter.",
                "Ignore documentation and follow guesses.",
            ],
            0,
        ),
        (
            "What is the purpose of the numerical checkpoints in this phase?",
            [
                "Give concrete targets (time, scores, note counts) so progress is measurable.",
                "Replace the quiz entirely.",
                "Hide the real requirements.",
                "Guarantee a job offer.",
            ],
            0,
        ),
        (
            "Before submitting all 30 answers for {topic}, what final check is most useful?",
            [
                "Re-scan questions where you hesitated and confirm the option matches the phase reading goals.",
                "Submit immediately without review.",
                "Change answers randomly to vary results.",
                "Leave several blank to save time.",
            ],
            0,
        ),
        (
            "How should you use practice tasks in {topic}?",
            [
                "Treat them as required evidence you understood the reading, not optional decoration.",
                "Skip them if the quiz feels easy.",
                "Only read task titles without doing work.",
                "Replace them with unrelated personal projects only.",
            ],
            0,
        ),
        (
            "Which note-taking approach best supports MCQ success for {course_title}?",
            [
                "Write short Q/A pairs tied to definitions and common misconceptions from the readings.",
                "Copy entire pages without summarizing.",
                "Avoid notes because memory is enough.",
                "Write only jokes unrelated to the topic.",
            ],
            0,
        ),
        (
            "If you fail the phase quiz, what is the best recovery plan?",
            [
                "Review incorrect themes, revisit the listed readings, then retake after targeted practice.",
                "Retake immediately without studying.",
                "Assume the quiz is broken and ignore feedback.",
                "Skip to the next phase anyway.",
            ],
            0,
        ),
    ]
    out: list[dict] = []
    for i in range(30):
        stem, opts, ai = stems[i % len(stems)]
        doc = titles[i % len(titles)]
        qtext = stem.format(course_title=course_title, topic=topic, doc=doc, domain=domain)
        out.append(
            {
                "question": qtext,
                "options": list(opts),
                "answer_index": ai,
                "bank_version": QUIZ_BANK_VERSION,
            }
        )
    return out


def build_phase_quiz(course_title: str, phase_number: int, phase_meta: dict | list | None = None) -> list[dict]:
    """Return 30 MCQs aligned to course domain, phase topic, and listed reading resources."""
    if isinstance(phase_meta, list):
        phase_meta = None
    if phase_meta is None:
        plan = generate_phase_plan(course_title)
        phase_meta = next((p for p in plan if p["phase_number"] == phase_number), plan[0])
    domain = course_domain(course_title)
    if domain in ("web", "python"):
        bank = pick_bank(domain, phase_number)
    else:
        bank = pick_bank(domain, phase_number)
        if not bank:
            bank = _template_bank_30(course_title, phase_number, phase_meta, domain)
    if not bank:
        bank = _template_bank_30(course_title, phase_number, phase_meta, domain)
    bank = diversify_with_readings(bank, course_title, phase_meta)
    out: list[dict] = []
    for i, q in enumerate(bank):
        seed = abs(hash(f"{course_title}|{phase_number}|{i}|v{QUIZ_BANK_VERSION}")) % (2**31)
        out.append(_shuffle_options(q, seed))
    return out


def phase_content(topic: str, phase: int) -> str:
    """Backward compatible helper used by older code paths."""
    plan = generate_phase_plan(topic)
    picked = next((p for p in plan if p["phase_number"] == phase), None)
    return picked["content"] if picked else plan[0]["content"]
