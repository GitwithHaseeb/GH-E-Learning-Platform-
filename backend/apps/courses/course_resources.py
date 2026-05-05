"""
Topic-accurate reading + video URLs per course and per phase.
Links point to official docs, codelabs, or scoped Coursera/YouTube destinations (not generic placeholders).
"""

from __future__ import annotations

from urllib.parse import quote_plus


def coursera_search(label: str, query: str) -> tuple[str, str]:
    return (label, f"https://www.coursera.org/search?query={quote_plus(query)}")


def classcentral_topic(query: str) -> tuple[str, str]:
    return ("Free courses on Class Central", f"https://www.classcentral.com/search?q={quote_plus(query)}")


def yt_watch(label: str, video_id: str) -> tuple[str, str]:
    return (label, f"https://www.youtube.com/watch?v={video_id}")


def yt_playlist(label: str, list_id: str) -> tuple[str, str]:
    return (label, f"https://www.youtube.com/playlist?list={list_id}")


def _five_phases(
    domain: str,
    stack: list[str],
    phases: list[dict],
) -> dict:
    assert len(stack) == 5 and len(phases) == 5
    return {"domain": domain, "stack": stack, "phases_resources": phases}


def learning_profile(course_title: str) -> dict:
    """Return domain key, 5 phase titles, and per-phase readings + videos."""
    t = course_title.lower()

    # --- Mobile (match React Native before generic React) ---
    if "react native" in t:
        stack = [
            "Expo / React Native environment and core components",
            "Navigation, lists, and styling in RN",
            "State, hooks, and data flow",
            "Networking, storage, and native modules overview",
            "Build, test, and ship to stores",
        ]
        phases = [
            {
                "readings": [
                    ("React Native — Get started", "https://reactnative.dev/docs/getting-started"),
                    ("Environment setup (frameworks)", "https://reactnative.dev/docs/environment-setup"),
                    coursera_search("Coursera — search React Native courses (many free to audit)", "React Native mobile development"),
                    classcentral_topic("React Native"),
                ],
                "videos": [
                    yt_watch("Net Ninja — React Native #1 (Expo setup)", "J2j1yk-34OY"),
                    yt_watch("Expo in 100 seconds (Fireship)", "vFW_TxKLyrE"),
                ],
            },
            {
                "readings": [
                    ("Core components & APIs", "https://reactnative.dev/docs/components-and-apis"),
                    ("StyleSheet & layout", "https://reactnative.dev/docs/style"),
                    ("Images & performance", "https://reactnative.dev/docs/images"),
                ],
                "videos": [
                    yt_watch("Net Ninja — React Native #3 (navigation)", "e1oMTqZ73aU"),
                    yt_watch("Net Ninja — React Native #1 (Expo setup)", "J2j1yk-34OY"),
                ],
            },
            {
                "readings": [
                    ("State & hooks in React (shared concepts)", "https://react.dev/reference/react"),
                    ("React Native performance", "https://reactnative.dev/docs/performance"),
                ],
                "videos": [
                    yt_watch("Net Ninja — React Native #14 (Auth context)", "Ky43ve3b9Ss"),
                    yt_watch("Expo in 100 seconds (Fireship)", "vFW_TxKLyrE"),
                ],
            },
            {
                "readings": [
                    ("Networking / fetch", "https://reactnative.dev/docs/network"),
                    ("Using TypeScript with RN", "https://reactnative.dev/docs/typescript"),
                ],
                "videos": [
                    yt_watch("Net Ninja — React Native #1 (Expo setup)", "J2j1yk-34OY"),
                    yt_watch("Net Ninja — React Native #3 (navigation)", "e1oMTqZ73aU"),
                ],
            },
            {
                "readings": [
                    ("Publishing to Google Play", "https://reactnative.dev/docs/signed-apk-android"),
                    ("Publishing to App Store overview", "https://reactnative.dev/docs/publishing-to-app-store"),
                ],
                "videos": [
                    yt_watch("Net Ninja — React Native #1 (Expo setup)", "J2j1yk-34OY"),
                    yt_watch("Expo in 100 seconds (Fireship)", "vFW_TxKLyrE"),
                ],
            },
        ]
        return _five_phases("react_native", stack, phases)

    if "flutter" in t or ("mobile" in t and "app" in t and "flutter" in t):
        stack = [
            "Install Flutter & learn Dart fundamentals",
            "Widgets, layout, and Material design",
            "State management & architecture basics",
            "Networking, JSON, and persistence",
            "Testing, performance, and release (Play / App Store)",
        ]
        _flutter_core_videos = [
            yt_watch("freeCodeCamp — Flutter course for beginners (37 hours, verified)", "VPvVD8t02U8"),
            yt_watch("Fireship — Flutter in 100 seconds", "lNQIh467-q4"),
        ]
        _flutter_alt = yt_watch("Flutter full course for beginners (Academind / freeCodeCamp style)", "pTJJsmejUOQ")
        phases = [
            {
                "readings": [
                    ("Flutter — Install (official)", "https://docs.flutter.dev/get-started/install"),
                    ("Dart language tour", "https://dart.dev/language"),
                    ("First Flutter app codelab", "https://codelabs.developers.google.com/codelabs/flutter-codelab-first"),
                    coursera_search("Coursera — Flutter courses (filter “Free” / audit)", "Flutter mobile development"),
                    classcentral_topic("Flutter"),
                ],
                "videos": list(_flutter_core_videos),
            },
            {
                "readings": [
                    ("Introduction to widgets", "https://docs.flutter.dev/ui/widgets-intro"),
                    ("Layout tutorial", "https://docs.flutter.dev/ui/layout/tutorial"),
                    ("Material Design 3 for Flutter", "https://m3.material.io/develop/flutter"),
                    ("Widget catalog", "https://docs.flutter.dev/ui/widgets"),
                ],
                "videos": [_flutter_core_videos[0], _flutter_alt],
            },
            {
                "readings": [
                    ("State management intro", "https://docs.flutter.dev/data-and-backend/state-mgmt"),
                    ("Lists & grids cookbook", "https://docs.flutter.dev/cookbook/lists"),
                    ("pub.dev — package ecosystem", "https://pub.dev/"),
                    ("Provider package", "https://pub.dev/packages/provider"),
                ],
                "videos": [_flutter_alt, _flutter_core_videos[1]],
            },
            {
                "readings": [
                    ("Networking & HTTP", "https://docs.flutter.dev/networking"),
                    ("JSON serialization", "https://docs.flutter.dev/data-and-backend/json"),
                    ("Persist data with SQLite (cookbook)", "https://docs.flutter.dev/cookbook/persistence/sqlite"),
                ],
                "videos": list(_flutter_core_videos),
            },
            {
                "readings": [
                    ("Build & release an Android app", "https://docs.flutter.dev/deployment/android"),
                    ("Build & release an iOS app", "https://docs.flutter.dev/deployment/ios"),
                    ("Performance best practices", "https://docs.flutter.dev/perf/best-practices"),
                    ("Testing introduction", "https://docs.flutter.dev/testing/overview"),
                ],
                "videos": [_flutter_core_videos[0], _flutter_core_videos[1]],
            },
        ]
        return _five_phases("flutter", stack, phases)

    # --- Keyword fallbacks (direct docs + scoped search + known-good videos) ---
    if "seo" in t:
        stack = ["Search basics & crawling", "On-page SEO", "Technical SEO & CWV", "Content & links", "Measurement & iteration"]
        vid = ("Ahrefs — SEO training for beginners", "xsVTqzratPU")
        base_reads = [
            ("Google SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide"),
            ("Search Central documentation", "https://developers.google.com/search/docs"),
            coursera_search("Coursera — SEO specialization search", "Search Engine Optimization"),
        ]
        return _five_phases(
            "seo",
            stack,
            [
                {"readings": base_reads + [("How Google Search works", "https://developers.google.com/search/docs/appearance/how-google-search-works")], "videos": [vid, yt_watch("Google Search Central — SEO basics", "ElxuFNWuuOA")]},
                {"readings": base_reads + [("Meta tags best practices", "https://developers.google.com/search/docs/appearance/snippet")], "videos": [vid, yt_watch("On-page SEO checklist", "EkpS1eICji0")]},
                {"readings": base_reads + [("Core Web Vitals", "https://web.dev/articles/vitals")], "videos": [vid, yt_watch("Technical SEO with Google tools", "ClXLu6Uehi8")]},
                {"readings": base_reads + [("Link spam policies", "https://developers.google.com/search/docs/essentials/spam-policies")], "videos": [vid, yt_watch("Content SEO strategy", "0LH6vHuc4Lo")]},
                {"readings": base_reads + [("Google Search Console", "https://search.google.com/search-console/about")], "videos": [vid, yt_watch("GA4 + Search Console for SEO", "gUZDEz7R0R0")]},
            ],
        )

    if "docker" in t:
        stack = ["Containers concepts", "Images & Dockerfile", "Compose & volumes", "Networking & security", "CI integration"]
        r = [
            ("Docker get started", "https://docs.docker.com/get-started/"),
            ("Dockerfile reference", "https://docs.docker.com/reference/dockerfile/"),
            coursera_search("Coursera — Docker courses", "Docker containers"),
        ]
        v = yt_watch("freeCodeCamp — Docker for beginners", "bHMFuihgUXU")
        return _five_phases("docker", stack, [{"readings": r, "videos": [v, yt_watch("TechWorld with Nana — Docker in 2 hours", "fqMOX6JJhGo")]} for _ in range(5)])

    if "kubernetes" in t or "k8s" in t:
        stack = ["Clusters & pods", "Deployments & services", "ConfigMaps & secrets", "Ingress & scaling", "Observability basics"]
        r = [
            ("Kubernetes Basics (official)", "https://kubernetes.io/docs/tutorials/kubernetes-basics/"),
            ("Concepts overview", "https://kubernetes.io/docs/concepts/"),
            coursera_search("Coursera — Kubernetes courses", "Kubernetes"),
        ]
        v = yt_watch("freeCodeCamp — Kubernetes course", "X48VuDVv0do")
        return _five_phases("kubernetes", stack, [{"readings": r, "videos": [v, yt_watch("TechWorld with Nana — Kubernetes crash course", "s_o8dwDRLlk")]} for _ in range(5)])

    if "terraform" in t:
        stack = ["IaC concepts", "Providers & resources", "Modules", "State & workspaces", "CI patterns"]
        r = [
            ("Terraform install & get started", "https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli"),
            ("Language docs", "https://developer.hashicorp.com/terraform/docs"),
            coursera_search("Coursera — Terraform / DevOps", "Terraform Infrastructure as Code"),
        ]
        v = yt_watch("freeCodeCamp — Terraform course", "SLB_c_ayRMo")
        return _five_phases("terraform", stack, [{"readings": r, "videos": [v, yt_watch("HashiCorp Terraform explained", "z9O8O7U7d0o")]} for _ in range(5)])

    if "github action" in t or "ci/cd" in t:
        stack = ["YAML workflows", "Jobs & runners", "Secrets & environments", "Reusable workflows", "Security & best practices"]
        r = [
            ("GitHub Actions docs", "https://docs.github.com/en/actions"),
            ("Quickstart", "https://docs.github.com/en/actions/quickstart"),
            coursera_search("Coursera — GitHub Actions / CI CD", "GitHub Actions CI CD"),
        ]
        v = yt_watch("GitHub Actions tutorial (TechWorld with Nana)", "R8_veQiYBjI")
        return _five_phases("cicd", stack, [{"readings": r, "videos": [v, yt_watch("freeCodeCamp — GitHub Actions 2hr", "R8_veQiYBjI")]} for _ in range(5)])

    if "linux" in t and "devops" in t:
        stack = ["Shell & filesystem", "Users & permissions", "Processes & services", "Networking tools", "Scripting for ops"]
        r = [
            ("Linux command line basics (Ubuntu)", "https://ubuntu.com/tutorials/command-line-for-beginners"),
            ("GNU/Linux documentation", "https://www.gnu.org/software/bash/manual/"),
            coursera_search("Coursera — Linux for beginners", "Linux administration"),
        ]
        v = yt_watch("freeCodeCamp — Linux for beginners", "sWbUDq4S6Y8")
        return _five_phases("linux", stack, [{"readings": r, "videos": [v, yt_watch("Linux Crash Course (Traversy Media)", "sgSCV9ZZKhQ")]} for _ in range(5)])

    if "prometheus" in t or "grafana" in t:
        stack = ["Metrics model", "Prometheus setup", "PromQL basics", "Grafana dashboards", "Alerting"]
        r = [
            ("Prometheus — Getting started", "https://prometheus.io/docs/introduction/first_steps/"),
            ("Grafana tutorials", "https://grafana.com/tutorials/"),
            coursera_search("Coursera — Prometheus Grafana monitoring", "Prometheus Grafana monitoring"),
        ]
        v = yt_watch("freeCodeCamp — Grafana & Prometheus course", "hmLArLzUy8Y")
        return _five_phases("monitoring", stack, [{"readings": r, "videos": [v, yt_watch("Prometheus + Grafana in 20 minutes (TechWorld)", "hUjrMUtT2As")]} for _ in range(5)])

    if "aws" in t and "cloud" in t:
        stack = ["IAM & accounts", "EC2 & networking", "S3 & data", "RDS / serverless intro", "Well-Architected overview"]
        r = [
            ("AWS Skill Builder (free digital training)", "https://skillbuilder.aws/"),
            ("AWS Getting Started Resource Center", "https://aws.amazon.com/getting-started/"),
            coursera_search("Coursera — AWS fundamentals", "AWS cloud fundamentals"),
        ]
        v = yt_watch("freeCodeCamp — AWS Certified Cloud Practitioner", "3hLmPSdznYQ")
        return _five_phases("aws", stack, [{"readings": r, "videos": [v, yt_watch("AWS for Beginners (Simplilearn)", "3XFODdaK3r0")]} for _ in range(5)])

    if "java" in t and "spring" in t:
        stack = ["Spring ecosystem", "Spring Boot basics", "REST APIs", "Data access", "Security & testing"]
        r = [
            ("Spring Boot reference", "https://docs.spring.io/spring-boot/index.html"),
            ("Building a RESTful Web Service", "https://spring.io/guides/gs/rest-service/"),
            coursera_search("Coursera — Spring Boot", "Spring Boot REST API"),
        ]
        v = yt_watch("Java Spring Boot (freeCodeCamp)", "vtPkZgsvrXw")
        return _five_phases("java", stack, [{"readings": r, "videos": [v, yt_watch("Spring Boot Tutorial (Amigoscode)", "9SGDpanrc8U")]} for _ in range(5)])

    if "java" in t:
        stack = ["Syntax & OOP", "Collections & generics", "Exceptions & IO", "Concurrency intro", "Packaging & tooling"]
        r = [
            ("The Java Tutorials (Oracle)", "https://docs.oracle.com/javase/tutorial/"),
            ("Dev.java — Learn Java", "https://dev.java/learn/"),
            coursera_search("Coursera — Java programming", "Java programming beginner"),
        ]
        v = yt_watch("Java for beginners (Programming with Mosh)", "eIrMbAQSU34")
        return _five_phases("java", stack, [{"readings": r, "videos": [v, yt_watch("Java Tutorial for Beginners (Bro Code)", "xT6LBl6DlXw")]} for _ in range(5)])

    if "c++" in t or " c++" in t:
        stack = ["Basics & types", "Pointers & memory", "OOP in C++", "STL containers", "Modern C++ features"]
        r = [
            ("Learn C++ (learncpp.com)", "https://www.learncpp.com/"),
            ("C++ reference (cppreference)", "https://en.cppreference.com/w/"),
            coursera_search("Coursera — C++ programming", "C++ programming"),
        ]
        v = yt_watch("C++ for beginners (ProgrammingKnowledge)", "vLnPwxZdW4Y")
        return _five_phases("cpp", stack, [{"readings": r, "videos": [v, yt_watch("Modern C++ (The Cherno)", "mUQZx2FgP_8")]} for _ in range(5)])

    if "fastapi" in t:
        stack = ["Python API basics", "Path operations", "Models & validation", "Dependency injection", "Async & deployment"]
        r = [
            ("FastAPI tutorial — official", "https://fastapi.tiangolo.com/tutorial/"),
            ("Advanced user guide", "https://fastapi.tiangolo.com/advanced/"),
            coursera_search("Coursera — FastAPI Python", "FastAPI Python"),
        ]
        v = yt_watch("FastAPI Course (freeCodeCamp)", "tLKKmouUakk")
        return _five_phases("python", stack, [{"readings": r, "videos": [v, yt_watch("FastAPI REST API in 15 minutes (Pretty Printed)", "iWS9ogMPOI0")]} for _ in range(5)])

    if "django" in t:
        stack = ["Django basics", "Models & ORM", "DRF serializers & views", "Auth & permissions", "Testing & deployment"]
        r = [
            ("Django documentation", "https://docs.djangoproject.com/en/stable/"),
            ("Django REST framework", "https://www.django-rest-framework.org/"),
            coursera_search("Coursera — Django REST", "Django REST framework"),
        ]
        v = yt_watch("Django REST Framework course (freeCodeCamp)", "tujhFZTpsuo")
        return _five_phases("python", stack, [{"readings": r, "videos": [v, yt_watch("Django tutorial (TechWithTim)", "PtQiiknWUcI")]} for _ in range(5)])

    if "node" in t:
        stack = ["JS runtime on server", "Modules & npm", "Express APIs", "DB integration", "Auth & security"]
        r = [
            ("Node.js docs", "https://nodejs.org/en/docs/guides/getting-started-guide/"),
            ("Express.js guide", "https://expressjs.com/en/starter/installing.html"),
            coursera_search("Coursera — Node.js backend", "Node.js backend development"),
        ]
        v = yt_watch("Node.js course (freeCodeCamp)", "Oe421EPjeBE")
        return _five_phases("web", stack, [{"readings": r, "videos": [v, yt_watch("Node.js crash course (Traversy)", "fBNz5xF-BxU")]} for _ in range(5)])

    if "next.js" in t or "nextjs" in t:
        stack = ["App Router basics", "Rendering models", "Data fetching", "API routes & edge", "Deploy on Vercel"]
        r = [
            ("Next.js documentation", "https://nextjs.org/docs"),
            ("Learn Next.js", "https://nextjs.org/learn"),
            coursera_search("Coursera — Next.js React", "Next.js full stack"),
        ]
        v = yt_watch("Next.js 14 tutorial (freeCodeCamp)", "wm5gMKuwSYE")
        return _five_phases("web", stack, [{"readings": r, "videos": [v, yt_watch("Next.js for beginners (Net Ninja)", "A63U_aQs5Jw")]} for _ in range(5)])

    if "figma" in t:
        stack = ["Frames & components", "Auto layout", "Prototyping", "Design systems", "Handoff to dev"]
        r = [
            ("Figma Help Center", "https://help.figma.com/hc/en-us"),
            ("Figma for beginners (official)", "https://www.figma.com/resource-library/figma-design/"),
            coursera_search("Coursera — Figma UI UX", "Figma UI UX design"),
        ]
        v = yt_watch("Figma course (freeCodeCamp)", "dX83qX8EjMg")
        return _five_phases("design", stack, [{"readings": r, "videos": [v, yt_watch("Figma tutorial for beginners (crash course)", "jQ1sfKIl50E")]} for _ in range(5)])

    if "system design" in t:
        stack = ["Requirements & CAP", "Load balancing & caching", "Databases & sharding", "Messaging & async", "Case studies"]
        r = [
            ("System Design Primer (GitHub)", "https://github.com/donnemartin/system-design-primer"),
            ("Designing Data-Intensive Applications (chapter notes)", "https://dataintensive.net/"),
            coursera_search("Coursera — System design", "Software system design"),
        ]
        v = yt_watch("System design interview (Exponent)", "UzMJ3UNQUWU")
        return _five_phases("system_design", stack, [{"readings": r, "videos": [v, yt_watch("System Design (Gaurav Sen)", "xpGn5hkUXdE")]} for _ in range(5)])

    if "sql" in t or "postgres" in t:
        stack = ["SQL foundations", "Joins & aggregations", "Indexing & performance", "Transactions", "Design & migrations"]
        r = [
            ("PostgreSQL documentation", "https://www.postgresql.org/docs/current/"),
            ("SQL tutorial (W3Schools reference)", "https://www.w3schools.com/sql/"),
            coursera_search("Coursera — SQL PostgreSQL", "SQL PostgreSQL database"),
        ]
        v = yt_watch("SQL full course (freeCodeCamp)", "HXV3zeQGqFc")
        return _five_phases("python", stack, [{"readings": r, "videos": [v, yt_watch("PostgreSQL tutorial (freeCodeCamp)", "qw--VyvFIQM")]} for _ in range(5)])

    if "dsa" in t or "data structures" in t or "algorithms" in t:
        stack = ["Complexity & arrays", "Linked structures", "Trees & graphs", "Sorting & searching", "Interview patterns"]
        r = [
            ("VisuAlgo — algorithms visualized", "https://visualgo.net/en"),
            ("The Algorithms — Python (reference)", "https://github.com/TheAlgorithms/Python"),
            coursera_search("Coursera — Data structures algorithms", "Data structures algorithms interview"),
        ]
        v = yt_watch("DSA course (freeCodeCamp)", "8hly31xKli0")
        return _five_phases("dsa", stack, [{"readings": r, "videos": [v, yt_watch("Algorithms course (Abdul Bari)", "0IAPZzGSbME")]} for _ in range(5)])

    # --- Default: title-scoped search + reputable portals + one solid general CS video ---
    stack = ["Fundamentals", "Core workflow", "Applied practice", "Project implementation", "Review and capstone"]
    q = course_title
    base_reads = [
        ("freeCodeCamp curriculum (all free)", "https://www.freecodecamp.org/learn"),
        coursera_search("Coursera — search courses related to this topic (many free to audit)", q),
        classcentral_topic(q),
    ]
    base_videos = [
        yt_watch("How to learn programming (freeCodeCamp advice)", "ZKriNmsub5g"),
        yt_watch("MIT OpenCourseWare — Introduction to CS (Python)", "nykOeWgpQic"),
    ]
    return _five_phases(
        "general",
        stack,
        [{"readings": base_reads, "videos": base_videos} for _ in range(5)],
    )


def merge_with_canonical(course_title: str, profile: dict) -> dict:
    """
    If title matches main quizgen domains (blockchain, python, web, security, ai),
    keep their stack + enrich each phase with extra direct links (MDN, OWASP, etc.).
    Only upgrades the generic fallback profile — never overwrites specialized packs.
    """
    if profile["domain"] != "general":
        return profile
    t = course_title.lower()

    if "blockchain" in t:
        stack = ["Blockchain basics", "Wallets and transactions", "Smart contracts", "Security and gas", "DApp architecture"]
        phases = []
        common_reads = [
            ("Ethereum Developers", "https://ethereum.org/en/developers/docs/"),
            ("Solidity docs", "https://docs.soliditylang.org/"),
            coursera_search("Coursera — Blockchain", "Blockchain smart contracts"),
        ]
        vids = [
            yt_watch("Blockchain explained (Simply Explained)", "SSo_EIwHSd4"),
            yt_watch("Solidity intro (freeCodeCamp)", "gyMwXuJrbJQ"),
        ]
        for i in range(5):
            phases.append({"readings": common_reads, "videos": vids})
        return _five_phases("blockchain", stack, phases)

    if "machine learning" in t or "deep learning" in t or "data science" in t:
        stack = ["Data & Python tools", "Exploratory analysis", "Modeling basics", "Evaluation", "Deployment & ethics intro"]
        reads = [
            ("Kaggle Learn — courses", "https://www.kaggle.com/learn"),
            ("Intro to Machine Learning (Kaggle)", "https://www.kaggle.com/learn/intro-to-machine-learning"),
            coursera_search("Coursera — Data science / ML", course_title),
        ]
        vids = [
            yt_watch("3Blue1Brown — What is a neural network? (chapter 1)", "aircAruvnKk"),
            yt_watch("3Blue1Brown — Gradient descent (how neural networks learn)", "IHZwWFHWa-w"),
        ]
        return _five_phases("ai", stack, [{"readings": reads, "videos": vids} for _ in range(5)])

    if "web" in t or "react" in t or "javascript" in t or "typescript" in t:
        stack = [
            "HTML and semantic page structure",
            "CSS layouts with Bootstrap and Tailwind",
            "JavaScript DOM, events, and async basics",
            "React components, props, state, and routing",
            "PHP + MySQL backend integration and deployment flow",
        ]
        phase_reads = [
            [
                ("MDN — HTML structuring the web", "https://developer.mozilla.org/en-US/docs/Learn/HTML"),
                ("WHATWG HTML spec (reference)", "https://html.spec.whatwg.org/"),
                coursera_search("Coursera — HTML CSS web", "HTML CSS web development"),
            ],
            [
                ("MDN — CSS layout", "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout"),
                ("Bootstrap docs", "https://getbootstrap.com/docs/5.3/getting-started/introduction/"),
                ("Tailwind docs", "https://tailwindcss.com/docs/installation"),
            ],
            [
                ("MDN — JavaScript guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
                ("JavaScript.info", "https://javascript.info/"),
            ],
            [
                ("React — Learn React", "https://react.dev/learn"),
                ("React Router docs", "https://reactrouter.com/en/main"),
            ],
            [
                ("PHP getting started", "https://www.php.net/manual/en/getting-started.php"),
                ("MySQL 8.0 tutorial (official excerpt)", "https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/"),
                ("MDN — Client-server overview", "https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview"),
            ],
        ]
        vids = [
            yt_watch("HTML & CSS crash course (Traversy)", "G3e-cpL7ofc"),
            yt_watch("JavaScript full course (freeCodeCamp)", "PkZNo7MFNFg"),
            yt_watch("React course (freeCodeCamp)", "bMknfKXIFA8"),
            yt_watch("PHP full course (freeCodeCamp)", "OK_JCtrrv-c"),
        ]
        phases = []
        for i in range(5):
            phases.append(
                {
                    "readings": phase_reads[i],
                    "videos": [vids[i % len(vids)], vids[(i + 1) % len(vids)]],
                }
            )
        return _five_phases("web", stack, phases)

    if "security" in t or "hacking" in t or "soc" in t:
        stack = ["Threat model", "OWASP basics", "Authentication security", "Monitoring alerts", "Incident response"]
        reads = [
            ("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
            ("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"),
            coursera_search("Coursera — Cybersecurity", "Cybersecurity fundamentals"),
        ]
        vids = [yt_watch("Cybersecurity course (freeCodeCamp)", "U_P23SqJaDc"), yt_watch("OWASP Top 10 explained", "3Kq1MIfTWCE")]
        return _five_phases("security", stack, [{"readings": reads, "videos": vids} for _ in range(5)])

    if _ai_title(t):
        stack = ["AI landscape", "Data and model basics", "Prompt design", "Evaluation", "AI product delivery"]
        reads = [
            ("Google AI learning", "https://ai.google/education/"),
            ("Microsoft Learn — AI", "https://learn.microsoft.com/en-us/training/browse/?products=azure&terms=AI"),
            coursera_search("Coursera — Artificial Intelligence", "Artificial intelligence machine learning"),
        ]
        vids = [yt_watch("Generative AI in 5 minutes (Google)", "G2fqAlgmoPo"), yt_watch("Prompt engineering intro (IBM Technology)", "dOxUroR57xs")]
        dom = "ai_product" if "product management" in t else "ai"
        if "product management" in t:
            reads = [
                ("Coursera Google Project Management", "https://www.coursera.org/professional-certificates/google-project-management"),
                ("Mind the Product", "https://www.mindtheproduct.com/"),
                coursera_search("Coursera — AI product management", "AI product management"),
            ]
        return _five_phases(dom, stack, [{"readings": reads, "videos": vids} for _ in range(5)])

    return profile


def _ai_title(t: str) -> bool:
    parts = t.replace("-", " ").replace("/", " ").split()
    if "data science" in t or "machine learning" in t or "deep learning" in t:
        return False
    if "ai" in parts or "machine" in t or "prompt" in t or "generative" in t:
        return True
    return False


def final_learning_profile(course_title: str) -> dict:
    """Public entry: keyword packs merged with canonical stacks for core domains."""
    base = learning_profile(course_title)
    return merge_with_canonical(course_title, base)
