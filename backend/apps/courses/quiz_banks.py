"""Curated MCQ banks for phase quizzes (bank_version 2)."""

QUIZ_BANK_VERSION = 2


def _q(question: str, options: list[str], answer_index: int) -> dict:
    return {
        "question": question,
        "options": list(options),
        "answer_index": int(answer_index) % 4,
        "bank_version": QUIZ_BANK_VERSION,
    }


# --- Web development: 30 distinct MCQs per phase (HTML → CSS frameworks → JS → React → PHP/MySQL) ---

WEB_PHASE_1 = [
    _q("What is the primary purpose of the <!DOCTYPE html> declaration?", ["Tells the browser which HTML parsing mode to use", "Loads external CSS automatically", "Defines the page charset only", "Creates a server session"], 0),
    _q("Which element should wrap the main unique content of a page (one per document)?", ["<main>", "<div id='wrapper'>", "<section> only", "<article> only"], 0),
    _q("Which tag is most appropriate for site navigation links?", ["<nav>", "<menu> only", "<footer>", "<span>"], 0),
    _q("What does the lang attribute on <html> help with?", ["Accessibility and correct pronunciation/translation hints", "CSS color scheme", "JavaScript minification", "Database collation"], 0),
    _q("Which element is best for contact information about the page author?", ["<address>", "<contact>", "<aside>", "<blockquote>"], 0),
    _q("What is the difference between <strong> and <b> in modern HTML semantics?", ["<strong> indicates importance; <b> is stylistic bold without extra meaning", "They are identical in meaning", "<b> is deprecated", "<strong> only works inside <p>"], 0),
    _q("Which input type is appropriate for an email address field with basic browser validation?", ['type="email"', 'type="text" only', 'type="mail"', 'type="string"'], 0),
    _q("What is the correct way to associate a <label> with an input using id?", ['<label for="user">', '<label to="user">', '<label ref="user">', '<label input="user">'], 0),
    _q("Which attribute provides a text alternative for images (accessibility + SEO)?", ["alt", "title only", "src", "href"], 0),
    _q("Which element should be used for a self-contained syndicate-able composition (blog post)?", ["<article>", "<div>", "<fragment>", "<panel>"], 0),
    _q("What is a correct use of heading levels?", ["Use <h1>–<h6> in meaningful order without skipping levels arbitrarily", "Use only <h1> everywhere", "Headings are purely visual", "Skip from h1 to h4 always"], 0),
    _q("Which meta tag is commonly used for responsive viewport scaling?", ['<meta name="viewport" ...>', '<meta name="screen" ...>', "<viewport>", "<scale>"], 0),
    _q("What does the defer attribute on <script> do?", ["Downloads in parallel and runs after HTML parsing", "Blocks parsing until downloaded", "Deletes the script", "Runs before HTML is parsed always"], 0),
    _q("Which list is appropriate for ordered steps?", ["<ol>", "<ul>", "<dl>", "<list>"], 0),
    _q("What is <figure> typically paired with?", ["<figcaption>", "<caption> only in tables", "<legend>", "<label>"], 0),
    _q("Which element represents tangential content (side notes) related to nearby content?", ["<aside>", "<sidebar> (native)", "<tangential>", "<note>"], 0),
    _q("What is the role of the charset meta tag (UTF-8)?", ["Ensures correct character encoding for text", "Sets CSS units", "Defines API auth", "Compresses images"], 0),
    _q("Which tag defines metadata not shown directly on the page?", ["<head>", "<body>", "<display:none>", "<meta> only without head"], 0),
    _q("For tabular data, which structure is correct?", ["<table><thead><tbody>...", "<grid><row>...", "<table><tr> only always forbidden", "<excel>"], 0),
    _q("What is scope on <th> used for?", ["Associates header cells with rows/columns for accessibility", "CSS z-index", "JavaScript scope", "Database scope"], 0),
    _q("Which global attribute is used to hide an element from accessibility tree when appropriate?", ["aria-hidden='true'", "hidden='visual'", "invisible='1'", "a11y='off'"], 0),
    _q("What does <details>/<summary> provide without JavaScript?", ["A native disclosure widget", "A modal dialog", "Routing", "Animations"], 0),
    _q("Which element wraps introductory content or hero for a sectioning root?", ["<header>", "<intro>", "<hero>", "<top>"], 0),
    _q("What is the correct MIME mindset for HTML5?", ["HTML is a living standard; validate and test in browsers", "HTML is XHTML-only now", "HTML requires PHP", "HTML cannot include forms"], 0),
    _q("Which practice improves keyboard navigation?", ["Use focusable native elements and visible focus styles", "Remove all outlines always", "Use only mouseover handlers", "Use divs for every button"], 0),
    _q("What is a relative URL?", ["A path resolved against the current document URL", "Always https://google.com", "A database foreign key", "An absolute path only"], 0),
    _q("Which attribute prevents a form field from being edited?", ["readonly (or disabled depending on use-case)", "static", "lock", "freeze"], 0),
    _q("What is the purpose of required on an input?", ["Client-side constraint: must be filled before submit", "Server-only validation", "CSS required", "Database NOT NULL auto"], 0),
    _q("Which element defines clickable button behavior semantically?", ["<button type='button|submit|reset'>", "<div onclick> always preferred", "<span href>", "<a type='button'>"], 0),
    _q("Why avoid <div> soup?", ["Semantic elements improve accessibility, SEO, and maintainability", "Divs are banned", "Semantic tags are slower", "Browsers reject divs"], 0),
]

WEB_PHASE_2 = [
    _q("In CSS, what does box-sizing: border-box do?", ["Width/height include padding and border", "Ignores padding in layout", "Removes borders", "Forces inline layout only"], 0),
    _q("Which layout is best for one-dimensional distribution (row OR column)?", ["Flexbox", "Floats only", "Tables only", "position:absolute for all children"], 0),
    _q("Which layout is designed for two-dimensional grids?", ["CSS Grid", "Flexbox only", "z-index", "float:left"], 0),
    _q("What does rem unit size depend on?", ["Root element font-size", "Parent width only", "Viewport height only", "Browser tab count"], 0),
    _q("Media queries are primarily used to:", ["Apply styles based on device/viewport conditions", "Query SQL databases", "Import PHP", "Compile TypeScript"], 0),
    _q("What is mobile-first CSS strategy?", ["Start with base styles for small screens, enhance for larger breakpoints", "Start with desktop only", "Use only !important", "Avoid responsive design"], 0),
    _q("Bootstrap is primarily:", ["A CSS framework for responsive components and utilities", "A JavaScript database", "A PHP server", "A React replacement"], 0),
    _q("In Bootstrap 5, which class prefix is used for responsive column widths?", ["col-*", "grid-*", "row-* only", "flex-* only"], 0),
    _q("What is Tailwind CSS's core approach?", ["Utility-first classes composed in markup", "Only inline styles forbidden", "Semantic-only no classes", "Server-side rendering only"], 0),
    _q("Which Tailwind pattern maps to responsive breakpoints?", ["sm:, md:, lg: prefixes", "@iphone only", "break:320", "rwd:true"], 0),
    _q("CSS specificity: which typically wins?", ["More specific selector or !important (use sparingly)", "Whatever comes first always", "Inline styles never win", "Universal * beats IDs"], 0),
    _q("What does position: sticky do?", ["Scrolls until a threshold then behaves like fixed within its container", "Same as static", "Removes element", "Only for tables"], 0),
    _q("Which property controls stacking order of positioned elements?", ["z-index", "x-index", "stack:", "layer-count"], 0),
    _q("What is a CSS reset/normalize for?", ["Reduce cross-browser default style differences", "Delete all CSS", "Minify images", "Add animations"], 0),
    _q("Which unit is relative to viewport width?", ["vw", "px always relative", "em always vw", "pt"], 0),
    _q("What does gap do in Flexbox/Grid?", ["Sets spacing between items", "Sets border width", "Sets font gap", "Hides overflow"], 0),
    _q("Bootstrap utility class for margin-top 3 spacing scale is typically:", ["mt-3", "margin-top-3px", "m3t", "spacer-top"], 0),
    _q("Tailwind JIT mode mainly improves:", ["Build performance and smaller generated CSS", "Database queries", "PHP execution", "JWT signing"], 0),
    _q("Which CSS feature creates smooth transitions between states?", ["transition", "transform only without transition", "animation:none always", "keyframes only without properties"], 0),
    _q("What is clamp() useful for?", ["Fluid typography/spacing between min and preferred and max", "Clamping audio volume only", "SQL limits", "React state"], 0),
    _q("Which pseudo-class styles an element when focused via keyboard?", [":focus-visible", ":hover only", ":tap", ":mouse"], 0),
    _q("What does object-fit: cover do on an image?", ["Fills box while preserving aspect ratio, cropping overflow", "Stretches ignoring ratio", "Hides image", "Converts to WebP always"], 0),
    _q("CSS variables are declared with:", ["--name: value;", "$name: value; (SCSS in browser)", "@var name;", "var name ="], 0),
    _q("Which layout keeps footer at bottom on short pages (common pattern)?", ["Flex column on body with flex-grow on main", "position fixed footer always overlapping", "table layout only", "iframe"], 0),
    _q("What is the purpose of min-width in responsive design?", ["Prevent layout from breaking below a usable width", "Force maximum zoom", "Set database column", "PHP session width"], 0),
    _q("Dark mode in modern sites is often toggled using:", ["prefers-color-scheme media feature or class strategy", "cookies only", "server IP", "mysql theme"], 0),
    _q("Which Bootstrap component provides a responsive navigation bar?", ["navbar", "navrow", "topbar-fixed-html", "menubar"], 0),
    _q("Tailwind @apply is used to:", ["Extract repeated utility patterns into custom CSS classes", "Apply database migrations", "Import React", "Start PHP"], 0),
    _q("What does overflow: auto do?", ["Adds scrollbars only when needed", "Always hides overflow", "Deletes children", "Forces print"], 0),
    _q("Why prefer rem over px for font sizes in accessible designs?", ["Respects user root font scaling preferences better", "px is illegal", "rem is faster CPU", "px breaks HTTPS"], 0),
]

WEB_PHASE_3 = [
    _q("What is the event loop in JavaScript (browser) responsible for?", ["Scheduling async callbacks after stack clears", "Parsing HTML only", "CSS cascade order", "SQL transactions"], 0),
    _q("What does document.querySelector return?", ["First matching element or null", "NodeList always", "Array always", "Shadow root always"], 0),
    _q("In modern JavaScript, what is the main scoping difference between let and var?", ["let is block-scoped; var is function-scoped", "var is block-scoped; let is function-scoped", "Both are always global", "Both are hoisted identically with no temporal dead zone"], 0),
    _q("What is a Promise?", ["An object representing eventual completion/failure of async work", "A browser popup", "A CSS feature", "A PHP datatype"], 0),
    _q("async/await is syntactic sugar over:", ["Promises", "Callbacks only without promises", "Threads", "Goroutines"], 0),
    _q("What does JSON.parse do?", ["Converts JSON string to JS value", "Converts object to JSON", "Minifies CSS", "Loads images"], 0),
    _q("What does addEventListener third argument {passive: true} imply?", ["Cannot call preventDefault on touch/wheel listeners (performance)", "Always captures", "Removes listener", "Runs in worker"], 0),
    _q("How do you prevent form default submit to validate first?", ["event.preventDefault() in submit handler", "return false only in HTML", "type='stop'", "disable form"], 0),
    _q("What is strict mode ('use strict') primarily for?", ["Safer JS semantics and catching common mistakes", "Faster CSS", "PHP compatibility", "SQL mode"], 0),
    _q("Array.map returns:", ["A new array", "The same array mutated always", "A single number", "A Promise only"], 0),
    _q("What is closure?", ["Function remembering lexical scope variables", "Closing browser tab", "CSS display:none", "MySQL join"], 0),
    _q("fetch returns:", ["A Promise resolving to Response", "XMLHttpRequest object", "string always", "DOM node"], 0),
    _q("What HTTP method is idempotent for reads?", ["GET", "POST always", "PATCH always", "CONNECT"], 0),
    _q("localStorage stores:", ["String key/value in browser", "Server session in SQL", "Binary only", "JWT signed cookies only"], 0),
    _q("What is CORS?", ["Browser security model for cross-origin HTTP requests", "A React hook", "CSS grid mode", "PHP extension"], 0),
    _q("What does === compare?", ["Value and type without coercion", "Value with coercion only", "References only", "DOM position"], 0),
    _q("Debouncing an input handler helps:", ["Reduce expensive calls while typing", "Increase calls", "Disable input", "Encrypt passwords"], 0),
    _q("What is the DOM?", ["Tree representation of HTML nodes", "A database", "A CSS file", "Linux daemon"], 0),
    _q("Which method removes a child node?", ["element.remove() or removeChild", "deleteChild", "unlink()", "detachHTML"], 0),
    _q("What is template literal syntax?", ["Backticks with ${expr}", "Quotes with @{}", "Here-doc PHP", "HTML template tag only"], 0),
    _q("What does Array.filter return?", ["New array with elements passing predicate", "Single boolean", "Original array cleared", "Promise"], 0),
    _q("What is event bubbling?", ["Events propagate from target up ancestors", "Events never propagate", "Only capture phase exists", "CSS bubble"], 0),
    _q("try/catch is for:", ["Handling exceptions in synchronous code paths (and async with try/await)", "CSS errors", "SQL indexes", "JWT refresh"], 0),
    _q("What is nullish coalescing (??)?", ["Falls back only for null/undefined", "Same as || always", "Bitwise OR", "SQL COALESCE in browser"], 0),
    _q("Module import/export in ES modules enables:", ["Explicit dependency graph and static analysis", "Global variables only", "PHP includes", "Inline styles"], 0),
    _q("What is the purpose of Content-Type application/json?", ["Tells receiver body is JSON", "Sets CORS", "Caches images", "Starts websocket"], 0),
    _q("setTimeout(fn, 0) typically schedules:", ["Callback after current stack clears (macrotask)", "Immediate synchronous call", "Infinite loop", "Paint before parse"], 0),
    _q("What does optional chaining (?.) do?", ["Short-circuit access if intermediate is nullish", "Force non-null", "SQL join", "CSS nesting"], 0),
    _q("Why avoid inline onclick in large apps?", ["Harder to maintain/test; prefer addEventListener separation", "It is faster always", "Browsers ban it", "Security is perfect inline"], 0),
    _q("What is JSON.stringify used for?", ["Serialize JS value to JSON string", "Parse JSON", "Validate HTML", "Compile React"], 0),
]

WEB_PHASE_4 = [
    _q("What is a React component?", ["A reusable UI piece returning JSX (or createElement)", "A MySQL table", "A CSS file", "A PHP template only"], 0),
    _q("What are props in React?", ["Inputs passed from parent to child (read-only for child)", "Internal state always", "CSS variables", "Routes only"], 0),
    _q("What does useState return?", ["A state value and setter function", "Only value", "A Promise", "DOM ref"], 0),
    _q("What is JSX?", ["Syntax extension describing UI tree compiled by React", "A database language", "Server template engine", "Browser native only"], 0),
    _q("Why use keys in lists?", ["Help React reconcile identity of items efficiently", "SEO only", "Encryption", "CSS specificity"], 0),
    _q("What is useEffect mainly for?", ["Side effects: data fetch, subscriptions, syncing with systems", "Derived render logic that could run in render", "Styling", "SQL migrations"], 0),
    _q("What is controlled input?", ["Input value driven by React state", "Uncontrolled random", "Browser-only state always", "PHP $_POST"], 0),
    _q("What does React Router provide?", ["Client-side routing for SPA navigation", "Database routing", "Email routing", "DNS"], 0),
    _q("What is lifting state up?", ["Moving shared state to closest common ancestor", "Deleting state", "Using localStorage only", "Redux only"], 0),
    _q("What is conditional rendering?", ["Rendering different UI based on state/props", "Always same UI", "Server-only", "CSS @if"], 0),
    _q("Fragments (<></>) let you:", ["Group children without extra DOM nodes", "Create portals always", "Query SQL", "Define routes"], 0),
    _q("What is React.memo for?", ["Skip re-render if props shallow-equal (optimization)", "Encrypt components", "Add CSS", "Replace hooks"], 0),
    _q("useCallback memoizes:", ["Function identity between renders", "Values like useMemo always same", "DOM nodes", "Routes"], 0),
    _q("useMemo memoizes:", ["Computed values across renders", "Event handlers always", "Components mount", "HTTP cache"], 0),
    _q("What is context API used for?", ["Avoid prop drilling for broadly needed data", "Replace hooks", "Server sessions", "Webpack config"], 0),
    _q("StrictMode in dev helps with:", ["Highlighting unsafe lifecycles/double-invoke checks", "Production speed boost", "CSS strict", "SQL strict"], 0),
    _q("What is a ref (useRef) commonly used for?", ["Mutable box or accessing DOM elements", "Storing UI state that triggers re-render always", "Routing tables", "JWT storage only"], 0),
    _q("Error boundaries catch errors in:", ["Child component tree rendering/lifecycle", "Async event handlers always", "fetch failures always", "CSS parse errors"], 0),
    _q("What does lazy + Suspense enable?", ["Code-splitting component loading with fallback UI", "SQL lazy joins", "Slower loads", "PHP includes"], 0),
    _q("What is reconciliation?", ["React's diffing virtual DOM vs previous render", "DNS reconciliation", "Git merge", "CORS"], 0),
    _q("Why avoid mutating state directly?", ["React may not detect changes; use setter to schedule updates", "It is faster", "It is required by law", "It improves SEO"], 0),
    _q("What is children prop?", ["Content passed between component tags", "Only text nodes forbidden", "Router param", "CSS child selector"], 0),
    _q("What is default export vs named export?", ["Default: one primary export; named: multiple symbols", "Same thing", "Only CommonJS", "PHP namespaces"], 0),
    _q("useEffect cleanup function runs:", ["Before effect re-runs and on unmount", "Never", "Only on mount", "Before JSX parse"], 0),
    _q("What is prop drilling problem?", ["Passing props through many intermediate layers", "Too few props", "Using context always bad", "CSS issue"], 0),
    _q("What does useReducer help with?", ["Complex state transitions with explicit actions", "Only API caching", "DOM measurements", "SQL reducers"], 0),
    _q("Portal renders into:", ["A different DOM subtree while keeping React context", "iframe only", "MySQL", "Service worker only"], 0),
    _q("What is hydration (SSR context)?", ["Attaching event listeners to server-rendered HTML", "Deleting HTML", "CSS animation", "PHP opcache"], 0),
    _q("Why keys must be stable among siblings?", ["Unstable keys cause state bugs and poor performance", "Keys are optional always", "Keys are for CSS", "Keys encrypt props"], 0),
    _q("What is composition pattern?", ["Build complex UIs from smaller components", "Use one giant component", "Compose SQL only", "Compose emails"], 0),
]

WEB_PHASE_5 = [
    _q("In PHP, what does $ denote?", ["Variable names", "Constants only", "Comments", "Pointers like C"], 0),
    _q("Which superglobal holds HTTP POST fields in PHP?", ["$_POST", "$GET", "$HTTP_BODY", "$FORM"], 0),
    _q("What does mysqli_real_escape_string / prepared statements help prevent?", ["SQL injection", "XSS only", "CSRF only", "DNS leaks"], 0),
    _q("What is PDO in PHP?", ["Database abstraction layer with prepared statements", "A templating engine", "A JS framework", "Linux daemon"], 0),
    _q("Which HTTP method is often used for creating resources in REST-ish APIs?", ["POST", "GET for create", "HEAD", "TRACE"], 0),
    _q("What is session_start() used for?", ["Begin/resume a server-side session", "Start browser", "Start CSS", "Start cron"], 0),
    _q("What does password_hash in PHP provide?", ["Strong password hashing (e.g., bcrypt)", "MD5 always", "Plain storage", "JWT signing"], 0),
    _q("Why validate input on the server too (not only client)?", ["Clients can be bypassed; server is source of truth", "Client is enough always", "Server validation is slower so skip", "Browsers validate SQL"], 0),
    _q("What is CSRF protection goal?", ["Prevent unauthorized commands from another site using cookies", "Prevent SQL injection", "Compress responses", "Cache images"], 0),
    _q("What does Content-Type: application/x-www-form-urlencoded describe?", ["HTML form encoding for POST bodies", "JSON always", "Binary upload", "WebSocket"], 0),
    _q("In MySQL, PRIMARY KEY implies:", ["Unique + not null identifier for rows", "Optional duplicate", "Foreign key always", "Index on images"], 0),
    _q("What is a FOREIGN KEY constraint?", ["Enforces relationship integrity between tables", "Speeds queries only always", "Encrypts column", "Creates views only"], 0),
    _q("What does INNER JOIN return?", ["Rows matching join condition in both tables", "All rows left only", "Cartesian always", "Distinct always"], 0),
    _q("What is normalization in databases?", ["Structuring tables to reduce redundancy/anomalies", "Making all columns JSON", "Denormalize always", "Add duplicate keys"], 0),
    _q("Which SQL clause filters rows before grouping?", ["WHERE", "HAVING before GROUP BY always wrong", "ORDER BY", "LIMIT only"], 0),
    _q("Which SQL clause filters aggregated results?", ["HAVING", "WHERE on SUM always same stage", "JOIN", "INDEX"], 0),
    _q("What is an index used for?", ["Speed up lookups (trade-offs on writes/storage)", "Guarantee uniqueness always", "Replace primary key", "Encrypt"], 0),
    _q("What does HTTP 404 mean?", ["Resource not found", "Unauthorized", "Server error", "Created"], 0),
    _q("What does HTTP 500 typically mean?", ["Server encountered an error", "Client syntax error", "Not found", "Redirect"], 0),
    _q("What is .env used for in deployments?", ["Store secrets/config outside code", "Store HTML", "Store images", "Replace database"], 0),
    _q("Why use HTTPS?", ["Encrypts data in transit and enables integrity/trust", "Faster CPU always", "Required for <div>", "Disables forms"], 0),
    _q("What is MIME type for JSON responses from APIs?", ["application/json", "text/html", "application/sql", "image/php"], 0),
    _q("What is basic idea of MVC in web apps?", ["Separate Model, View, Controller responsibilities", "One file only", "No separation", "Only CSS pattern"], 0),
    _q("What does php -l do?", ["Lint PHP file for syntax errors", "Start server always", "Install packages", "Run migrations"], 0),
    _q("What is autoloading (Composer) mainly for?", ["Loading classes without manual requires", "Loading images", "Caching DNS", "JWT refresh"], 0),
    _q("Why parameterize SQL queries?", ["Separate SQL structure from user data to mitigate injection", "Speed only", "Pretty printing", "CSS separation"], 0),
    _q("What is an API route vs page route?", ["API returns data (often JSON); page returns HTML UI", "Same always", "API cannot use HTTP", "Page routes are SQL"], 0),
    _q("What is deployment in this course context?", ["Publishing app to a server/cloud so users can access", "Deleting code", "Writing HTML email", "phpMyAdmin only"], 0),
    _q("What is environment parity goal?", ["Dev/stage/prod behave similarly to reduce surprises", "Make prod slower", "Different secrets same code always unsafe note—still use secrets per env", "Ignore configs"], 0),
    _q("What is a health check endpoint used for?", ["Tell load balancers/orchestrators if app is alive", "User profile", "CSS reset", "SQL explain"], 0),
]

WEB_BANKS = {1: WEB_PHASE_1, 2: WEB_PHASE_2, 3: WEB_PHASE_3, 4: WEB_PHASE_4, 5: WEB_PHASE_5}


# --- Python (5 phases aligned with generate_phase_plan stack) ---

PYTHON_PHASE_1 = [
    _q("What is CPython commonly referring to?", ["The standard Python implementation written in C", "A C++ compiler", "A JS package", "A database"], 0),
    _q("Which symbol starts a comment in Python?", ["#", "//", "--", "<!--"], 0),
    _q("What is indentation used for in Python?", ["Defining blocks (if/for/functions)", "Only formatting ignored", "String literals", "Imports only"], 0),
    _q("Which type represents whole numbers?", ["int", "float", "str", "list"], 0),
    _q("What does type(3.14) typically return?", ["float", "int", "decimal", "real"], 0),
    _q("Which is a mutable built-in sequence?", ["list", "tuple", "str", "frozenset"], 0),
    _q("Which is immutable?", ["tuple", "list", "dict", "set"], 0),
    _q("What does len([1,2,3]) return?", ["3", "2", "6", "None"], 0),
    _q("Which operator concatenates strings?", ["+", "* on strings repeats", "-", "/"], 0),
    _q("What is None in Python?", ["A singleton representing absence of value", "Null pointer crash", "False always", "0"], 0),
    _q("Which keyword defines a function?", ["def", "function", "fn", "lambda only"], 0),
    _q("What does return without an expression return?", ["None implicitly", "0", "False", "Error always"], 0),
    _q("What is a module in Python?", ["A file containing Python definitions/statements", "A loop", "A GUI widget", "A SQL table"], 0),
    _q("Which import brings a module under an alias?", ["import numpy as np", "include numpy", "using numpy", "require numpy"], 0),
    _q("What does if __name__ == '__main__' commonly enable?", ["Script entry point when executed directly", "Package install only", "Async loop", "GC"], 0),
    _q("Which collection preserves insertion order (3.7+ dict behavior)?", ["dict (language spec insertion order)", "set", "frozenset", "defaultdict unordered myth—ordered dict"], 0),
    _q("What does range(3) produce?", ["A range object representing 0..2", "A list always", "A tuple always", "Decimals"], 0),
    _q("Which raises an exception intentionally?", ["raise ValueError('msg')", "throw Error", "panic()", "except raise"], 0),
    _q("What is PEP 8 primarily?", ["Style guide for Python code", "Package installer", "Interpreter patch", "Testing tool"], 0),
    _q("Which is truthy in Python: [] ?", ["Falsy (empty list)", "Truthy", "Syntax error", "Undefined"], 0),
    _q("What does is compare?", ["Object identity", "Value equality always", "String contents always", "Types only"], 0),
    _q("What does == compare?", ["Value equality (may call __eq__)", "Identity always", "Memory addresses only", "Imports"], 0),
    _q("Which creates a virtual environment (common tool)?", ["python -m venv .venv", "pip env create", "npm init", "docker only"], 0),
    _q("What is pip used for?", ["Installing Python packages", "Formatting code", "Running tests", "Bundling JS"], 0),
    _q("Which statement reads a line from stdin in scripts?", ["input()", "read()", "scanf()", "gets()"], 0),
    _q("What does enumerate(iterable) provide?", ["Index-value pairs", "Only values", "Sorted iterable", "Length only"], 0),
    _q("Which keyword skips current loop iteration?", ["continue", "skip", "next", "pass"], 0),
    _q("Which keyword is a no-op placeholder?", ["pass", "noop", "idle", "nil"], 0),
    _q("What does break do in a loop?", ["Exit the loop", "Skip one iteration", "Pause thread", "Restart program"], 0),
    _q("Which literal creates an empty dict?", ["{}", "[]", "()", "set()"], 0),
]

PYTHON_PHASE_2 = [
    _q("What does elif mean?", ["Else-if chain in conditional logic", "Else loop", "Exception type", "Import alias"], 0),
    _q("Which loop iterates over a sequence?", ["for", "repeat", "foreach (keyword)", "loop"], 0),
    _q("while True: is:", ["An infinite loop unless broken", "Invalid syntax", "Runs once", "Compiler error"], 0),
    _q("What is slicing s[1:4]?", ["Elements from index 1 up to (not including) 4", "Includes 4 always", "Deletes items", "Sorts"], 0),
    _q("What does s[::-1] do for a sequence s?", ["Reverses a copy", "Sorts ascending", "Removes duplicates", "Raises"], 0),
    _q("What is a list comprehension?", ["Compact syntax to build lists from iterables", "A debugger", "A SQL query", "A type hint"], 0),
    _q("What does zip(a,b) do?", ["Pairs elements from iterables", "Compress files", "Encrypt", "Sort dict"], 0),
    _q("What is a generator expression?", ["Like list comp but lazy with parentheses", "Always returns list", "SQL generator", "Regex"], 0),
    _q("What does with open(...) as f manage?", ["Context manager closing resources", "Imports", "Threads", "Sockets only"], 0),
    _q("Which exception covers file-not-found scenarios?", ["FileNotFoundError", "ValueError", "KeyError", "OSError only never"], 0),
    _q("What does try/except/else mean?", ["else runs if no exception occurred in try", "else always runs", "else runs on exception", "invalid"], 0),
    _q("What does finally execute?", ["Always after try/except (cleanup)", "Only on errors", "Never", "Before try"], 0),
    _q("What is assert used for?", ["Debug checks that can be disabled with -O", "Production auth", "SQL constraints", "I/O"], 0),
    _q("Which matches multiple cases in Python 3.10+?", ["match/case", "switch", "caseof", "select"], 0),
    _q("What is an iterator?", ["Object implementing __iter__/__next__", "A list only", "A file path", "A decorator"], 0),
    _q("What does next(it) do?", ["Advance iterator or raise StopIteration", "Sort iterator", "Clone iterator", "Reset DB"], 0),
    _q("What is a decorator?", ["A function wrapping another function to extend behavior", "A comment", "A GUI style", "A SQL view"], 0),
    _q("What does *args allow?", ["Variable positional arguments", "Keyword-only args", "Globals", "Types"], 0),
    _q("What does **kwargs capture?", ["Keyword arguments as a dict", "Positional tuple", "Exceptions", "Imports"], 0),
    _q("What is a docstring?", ["String literal documenting module/class/function", "A comment with #", "A type", "A test"], 0),
    _q("Which is faster policy: EAFP vs LBYL in Python culture?", ["Often EAFP (try) vs checks—context dependent", "Always LBYL", "Never try/except", "Only in C"], 0),
    _q("What does collections.defaultdict help with?", ["Auto default values for missing keys", "Sorting keys", "Immutable dicts", "SQL joins"], 0),
    _q("What does Counter do?", ["Count hashable objects", "Count CPU cores", "Count pixels", "Count tokens in LLM only"], 0),
    _q("What is heapq module used for?", ["Heap queue algorithms", "HTTP heaps", "Graphics", "Audio"], 0),
    _q("What does itertools.groupby require?", ["Typically sorted iterable by key first", "Nothing", "SQL GROUP BY", "Random order"], 0),
    _q("Which statement imports names from a module directly?", ["from math import sqrt", "import sqrt", "include sqrt", "using sqrt"], 0),
    _q("What is slicing step s[::2]?", ["Every second item", "Sort by 2", "Delete 2", "Duplicate"], 0),
    _q("What does del lst[0] do?", ["Removes index 0 in place", "Returns new list", "Clears all variables", "Copies list"], 0),
    _q("What is walrus operator := used for?", ["Assignment inside expressions", "Bitwise OR", "Regex anchors", "Type unions"], 0),
    _q("Which comprehension builds a set?", ["{x for x in ...}", "(x for x in ...)", "[x for x in ...]", "{x: x} always dict"], 0),
]

PYTHON_PHASE_3 = [
    _q("What does def f(x, y=1) mean?", ["y has a default parameter value", "y is required", "y is global", "y is keyword-only"], 0),
    _q("What is * in def f(a, *, b) ?", ["b is keyword-only", "b is positional-only", "varargs only", "invalid"], 0),
    _q("What does return multiple values actually return?", ["A tuple", "A list always", "Two stacks", "JSON"], 0),
    _q("What is recursion base case?", ["Condition stopping recursion", "Fastest case", "Error case", "Import case"], 0),
    _q("What is a lambda?", ["Small anonymous function", "Database lambda", "AWS lambda only", "JS arrow function"], 0),
    _q("What does map(func, iterable) return in Python 3?", ["An iterator", "A list always", "A string", "A dict"], 0),
    _q("What does filter(func, iterable) return?", ["Iterator of items where func is truthy", "Sorted list", "SQL rows", "Bytes"], 0),
    _q("What is functools.partial?", ["Freeze some arguments of a callable", "Partial classes", "Partial imports", "Partial HTML"], 0),
    _q("What does yield make?", ["A generator function", "A thread", "A SQL view", "A constant"], 0),
    _q("What is sent to consumer via generator.send?", ["A value becomes yield result", "TCP packet", "HTTP body", "Exception only"], 0),
    _q("What is closure capturing?", ["Free variables from enclosing scope", "CPU cache lines", "Docker layers", "Git"], 0),
    _q("What does nonlocal do?", ["Assigns outer (non-global) enclosing variable", "Creates global", "Creates local only", "Deletes variable"], 0),
    _q("What does global x declare?", ["x refers to module-level global", "x is constant", "x is local always", "x is deleted"], 0),
    _q("What is a higher-order function?", ["Accepts/returns functions", "High CPU function", "Recursive only", "Built-in only"], 0),
    _q("What does @wraps from functools help preserve?", ["Metadata of wrapped function (name/doc)", "TCP wraps", "CSS wraps", "JWT"], 0),
    _q("What is a pure function?", ["Same inputs -> same output without side effects (ideal)", "Random output", "Prints always", "Uses DB always"], 0),
    _q("What does itertools.chain do?", ["Flatten iterables sequentially", "Sort chained lists", "SQL joins", "Async gather"], 0),
    _q("What is memoization?", ["Cache expensive function results", "Delete memory", "Garbage collect manually", "Encrypt"], 0),
    _q("What does callable(x) check?", ["Whether x can be called like a function", "Whether x is str", "Whether x is None", "Whether x is import"], 0),
    _q("What is typing.Optional[int] equivalent to?", ["Union[int, None]", "int only", "Any", "Never"], 0),
    _q("What does * unpacking do in function calls?", ["Expands iterable into positional args", "Keyword unpack", "Creates dict", "SQL explode"], 0),
    _q("What does ** unpacking do in dict literals/calls?", ["Expands mapping into keywords", "Bitwise", "Exponent", "Regex"], 0),
    _q("What is a factory function?", ["Returns configured objects/functions", "Builds factories in SQL", "GUI only", "Dockerfile parser"], 0),
    _q("What is tail recursion optimization in Python?", ["CPython generally does not guarantee TCO", "Always optimized", "Forbidden", "Only in asyncio"], 0),
    _q("What does inspect.signature help with?", ["Introspecting call signatures", "Signing JWT", "TLS", "Image signing"], 0),
    _q("What is id(obj)?", ["Integer identity (implementation detail)", "Hash always", "Memory address guaranteed stable", "UUID"], 0),
    _q("What does operator.itemgetter(1) create?", ["A callable fetching index 1", "A sorting algorithm", "A SQL getter", "A pandas series"], 0),
    _q("What is functools.reduce?", ["Fold iterable with binary function", "Reduce image size", "Reduce SQL rows only", "Reduce HTTP"], 0),
    _q("What does any(iterable) return?", ["True if any item truthy", "Count", "First item", "Sum"], 0),
    _q("For a non-empty iterable, what does all(iterable) return when every element is truthy?", ["True", "False", "The first falsy element", "The length of the iterable"], 0),
]

PYTHON_PHASE_4 = [
    _q("What is __init__ in a class?", ["Initializer method", "Destructor", "Static method always", "Module init file"], 0),
    _q("What is self in instance methods?", ["Instance reference passed explicitly", "Global object", "Class name", "Keyword only in Java"], 0),
    _q("What does @staticmethod mean?", ["Method doesn't receive instance or class automatically", "Requires self", "Requires cls", "Java static import"], 0),
    _q("What does @classmethod pass as first arg?", ["cls (the class)", "self", "None", "module"], 0),
    _q("What is inheritance for?", ["Reuse/extend behavior of a base class", "Encrypt classes", "Speed up CPU", "SQL only"], 0),
    _q("What does super() help call?", ["Parent implementations", "Private only", "Global functions", "Imports"], 0),
    _q("What is encapsulation?", ["Hiding internal state behind methods/properties", "Making everything public", "CSS technique", "Docker"], 0),
    _q("What is polymorphism?", ["Same interface, different concrete behaviors", "Many CPU cores", "Many files", "Many SQL tables"], 0),
    _q("What is dunder method __str__?", ["Human-readable string representation", "Secret string", "SQL str", "Static type"], 0),
    _q("What is __repr__ aimed at?", ["Unambiguous/developer representation", "Pretty UI", "JSON", "HTML"], 0),
    _q("What is a property decorator used for?", ["Getter/setter computed attributes", "Private keyword", "Constants", "Imports"], 0),
    _q("What is dataclasses module for?", ["Boilerplate reduction for simple classes", "ORM only", "HTTP clients", "Testing only"], 0),
    _q("What does __slots__ reduce?", ["Per-instance __dict__ overhead (trade-offs)", "CPU cores", "Security", "Imports"], 0),
    _q("What is MRO?", ["Method Resolution Order for inheritance", "Max request output", "SQL order", "Memory random order"], 0),
    _q("What is an abstract base class (abc) for?", ["Define required methods for subclasses", "Speed", "JSON", "HTTP"], 0),
    _q("What is composition over inheritance?", ["Build behavior by containing objects vs deep hierarchies", "Always inherit 10 levels", "Use only functions", "SQL composition"], 0),
    _q("What is a mixin?", ["Class meant to be multiply inherited for reusable behavior", "A drink", "A SQL join", "A React hook"], 0),
    _q("What does isinstance(x, T) check?", ["Instance/subclass relationship", "Exact type identity only", "None checks only", "Imports"], 0),
    _q("What does issubclass(A, B) check?", ["Whether A is subclass of B", "Instance check", "Module check", "File exists"], 0),
    _q("What is enum.Enum used for?", ["Symbolic named constants", "Enumerating SQL rows only", "Regex", "JSON"], 0),
    _q("What is __dict__ of an instance?", ["Namespace mapping attributes", "SQL dict", "Immutable", "C pointers"], 0),
    _q("What is operator overloading?", ["Defining dunder behaviors like + for objects", "CPU overload", "Too many methods illegal", "Docker overload"], 0),
    _q("What does __enter__/__exit__ implement?", ["Context manager protocol", "Iterator protocol", "Descriptor only", "Hashing"], 0),
    _q("What is a descriptor?", ["Defines attribute access via __get__/__set__", "A comment", "A SQL index", "A JWT"], 0),
    _q("What is @functools.total_ordering?", ["Generate comparison methods from a subset", "Sort files", "SQL ordering", "HTTP ordering"], 0),
    _q("What is a frozen dataclass?", ["Immutable instances (good for value objects)", "Frozen CPU", "Frozen dependencies bad", "Frozen SQL"], 0),
    _q("What does __post_init__ in dataclass run?", ["After __init__ generated fields assigned", "Before class definition", "Never", "On import only"], 0),
    _q("What is class variable vs instance variable?", ["Shared on class vs stored per instance", "Same", "Opposite names", "SQL vars"], 0),
    _q("What is Liskov substitution principle about?", ["Subtypes should be substitutable for base types", "SQL substitution", "JWT substitution", "CSS"], 0),
    _q("Why avoid circular imports?", ["Can cause partial initialization/import errors", "They are faster", "They are required", "They improve security"], 0),
]

PYTHON_PHASE_5 = [
    _q("What is __init__.py used for in packages?", ["Marks directories as Python packages (namespace packages aside)", "Runs GC", "Starts Django", "Contains SQL"], 0),
    _q("What is PYTHONPATH?", ["Env var adding module search paths", "Path to interpreter only", "pip config", "Node path"], 0),
    _q("What does if __name__ == '__main__' prevent when importing?", ["Running module script code unintentionally", "Imports entirely", "Circular refs", "Speed"], 0),
    _q("What is setuptools used for?", ["Packaging/distribution metadata and building", "Set theory", "SQL setup", "JWT"], 0),
    _q("What is pyproject.toml commonly used for?", ["Modern project configuration (PEP 621 etc.)", "Django templates", "Docker", "K8s"], 0),
    _q("What does pip install -e . do?", ["Editable install for local development", "Install email", "Install encryption", "Install editor"], 0),
    _q("What is a virtualenv benefit?", ["Isolated dependencies per project", "Faster CPU", "Smaller source files", "Better fonts"], 0),
    _q("What is semantic versioning?", ["MAJOR.MINOR.PATCH meaning for compatibility expectations", "Version by date only", "Random versions", "Git commit count only"], 0),
    _q("What is a wheel (.whl)?", ["Built distribution format", "Source-only .py", "Docker image", "SQL dump"], 0),
    _q("What does python -m compileall do?", ["Byte-compile files", "Delete pyc", "Run tests", "Format code"], 0),
    _q("What is __pycache__?", ["Directory storing bytecode caches", "Secret cache", "SQL cache", "HTTP cache"], 0),
    _q("What is a namespace package (PEP 420)?", ["Package split across multiple directories on sys.path", "Single folder only", "JS feature", "Docker namespace"], 0),
    _q("What does importlib.import_module do?", ["Programmatic import by string name", "Static import only", "SQL import", "C import"], 0),
    _q("What is runtime vs import time?", ["Code runs at import vs later calls", "Same always", "Only JS has", "Only C++"], 0),
    _q("Why pin dependency versions?", ["Reproducible builds and fewer surprises", "Always use latest breaking", "Security worse", "Speed worse"], 0),
    _q("What is a console script entry point?", ["CLI command installed with package", "GUI script", "SQL console", "Docker entry"], 0),
    _q("What does tox automate?", ["Testing across environments", "Deploy only", "Format only", "DB migrations only"], 0),
    _q("What is coverage.py for?", ["Measuring test code coverage", "Network coverage", "Disk usage", "CPU usage"], 0),
    _q("What is pytest compared to unittest?", ["Popular third-party testing framework with fixtures", "Standard only no choice", "Linter", "Formatter"], 0),
    _q("What is a monorepo?", ["Multiple projects in one repository", "One file repo", "GitHub only feature", "SQL repo"], 0),
    _q("What is pre-commit for?", ["Run hooks before commits (format/lint)", "Commit without checks", "Deploy hooks", "DB hooks"], 0),
    _q("What does black do?", ["Opinionated Python formatter", "Type checker", "Test runner", "Package builder"], 0),
    _q("What does ruff do?", ["Fast linter (and more) in Rust ecosystem", "Browser", "ORM", "Queue"], 0),
    _q("What is mypy?", ["Static type checker for Python", "Package manager", "Server", "Formatter"], 0),
    _q("What is a lock file in dependency management?", ["Resolved transitive versions for reproducibility", "Locks git", "Locks DB rows", "Locks UI"], 0),
    _q("What is __all__ in modules?", ["Controls from module import * exports", "CPU all cores", "SQL select *", "JWT audience"], 0),
    _q("What does zipapp create?", ["Executable python application archive", "Docker zip", "SQL zip", "React bundle"], 0),
    _q("What is PEP 440 about?", ["Version identification and parsing", "HTTP 440", "GPU", "Docker"], 0),
    _q("Why split code into packages?", ["Modularity, reuse, clearer boundaries", "Make imports slower", "One file always better", "Security worse"], 0),
    _q("What is a breaking change in libraries?", ["Change requiring client code updates", "Any bugfix", "Any new feature", "Formatting"], 0),
]

PYTHON_BANKS = {1: PYTHON_PHASE_1, 2: PYTHON_PHASE_2, 3: PYTHON_PHASE_3, 4: PYTHON_PHASE_4, 5: PYTHON_PHASE_5}


# --- Security ---

SEC_PHASE_1 = [
    _q("What is the CIA triad?", ["Confidentiality, Integrity, Availability", "Cipher, Index, Auth", "Cloud, IoT, AI", "Cert, IP, ACL"], 0),
    _q("What is threat modeling?", ["Systematic identification/prioritization of threats", "Deleting logs", "Pen test only", "Marketing"], 0),
    _q("What is phishing?", ["Social engineering to steal secrets via deceptive messages", "Firewall technique", "Encryption mode", "SQL join"], 0),
    _q("What is least privilege?", ["Grant minimum permissions needed", "Grant admin to all", "Disable MFA", "Public buckets"], 0),
    _q("What is MFA?", ["Multi-factor authentication", "Multi-file archive", "Mainframe access", "Memory fault avoidance"], 0),
    _q("What is malware?", ["Malicious software", "Mallware shopping", "Hardware bug", "Backup software"], 0),
    _q("What is ransomware?", ["Malware encrypting/extorting for decryption/payment", "Random ware", "Firewall", "IDS signature"], 0),
    _q("What is vulnerability vs exploit?", ["Weakness vs method to leverage it", "Same", "Opposite unrelated", "Only hardware"], 0),
    _q("What is patch management?", ["Applying updates to fix vulnerabilities", "Patch cables", "Git patch only", "DNS"], 0),
    _q("What is zero trust principle?", ["Never trust, always verify (continuous)", "Trust intranet always", "No encryption", "No logs"], 0),
    _q("What is SOC?", ["Security Operations Center monitoring/responding", "System on chip only", "Server object cache", "Subject oriented coding"], 0),
    _q("What is SIEM?", ["Security info/event management correlation", "Simple internet email", "Symmetric integration encryption mode", "SQL index engine"], 0),
    _q("What is an IOC?", ["Indicator of compromise", "International Olympic Committee in security always", "Input output controller only", "Inline object cache"], 0),
    _q("What is defense in depth?", ["Layered controls so failure of one doesn't fail all", "One firewall only", "No monitoring", "Open RDP"], 0),
    _q("What is risk = ?", ["Typically impact * likelihood (conceptually)", "Only impact", "Only CVE count", "Password length"], 0),
    _q("What is spear phishing?", ["Targeted phishing against specific org/person", "Random spam", "DDoS", "SQLi"], 0),
    _q("What is insider threat?", ["Risk from employees/contractors", "Only external hackers", "Cloud only", "TLS"], 0),
    _q("What is data classification?", ["Labeling sensitivity to apply controls", "Deleting data", "Compression", "Sharding"], 0),
    _q("What is secure SDLC?", ["Integrating security throughout development lifecycle", "Security after breach only", "No testing", "No code review"], 0),
    _q("What is hardening?", ["Reducing attack surface/configuring securely", "Adding more services", "Disabling logs", "Weaker passwords"], 0),
    _q("What is separation of duties?", ["Split responsibilities to reduce fraud/errors", "One admin does all", "Shared passwords", "Root everywhere"], 0),
    _q("What is an asset inventory?", ["Knowing what you must protect", "Deleting assets", "Buying assets only", "GPU list only"], 0),
    _q("What is supply chain risk in software?", ["Compromise via dependencies/build pipelines", "CPU supply", "Office supplies", "UPS power"], 0),
    _q("What is logging best practice for security?", ["Centralize, protect integrity, retain appropriately", "Log secrets", "Disable logs", "Public log buckets"], 0),
    _q("What is incident response?", ["Detect/contain/eradicate/recover/learn from incidents", "Only prevention", "Only sales", "Only backups"], 0),
    _q("What is tabletop exercise?", ["Simulated discussion of incident scenarios", "Gaming", "Pen test always", "Firewall config"], 0),
    _q("What is governance in security programs?", ["Policies, accountability, compliance alignment", "Only tools", "Only pentesting", "Only marketing"], 0),
    _q("What is privacy vs security?", ["Privacy focuses on personal data rights/use; security on protection", "Same word", "Unrelated", "Opposite"], 0),
    _q("What is red team?", ["Simulated attackers testing defenses", "Firewall vendor", "SOC tier 1 only", "Backup team"], 0),
    _q("What is blue team?", ["Defenders improving detection/response", "Attackers", "Sales", "HR"], 0),
]

SEC_BANKS = {1: SEC_PHASE_1, 2: SEC_PHASE_1, 3: SEC_PHASE_1, 4: SEC_PHASE_1, 5: SEC_PHASE_1}


# --- Blockchain ---

BC_PHASE_1 = [
    _q("What is a blockchain at a high level?", ["Append-only distributed ledger of ordered blocks", "Central SQL table", "A React component", "A compression algorithm"], 0),
    _q("What is a block typically linked by?", ["Cryptographic hash of previous block", "UUID", "Random numbers", "Email"], 0),
    _q("What is immutability in blockchain context?", ["Changing history is computationally/practically infeasible", "Data can never be read", "No encryption", "Mutable always"], 0),
    _q("What is a node?", ["Participant running blockchain software validating/relaying", "Only wallet", "Only miner UI", "DNS server"], 0),
    _q("What is consensus?", ["Agreement rules for valid chain state/order", "SQL consensus", "HTTPS handshake", "JWT"], 0),
    _q("What is PoW?", ["Proof of Work mining puzzle", "Proof of Web", "Power over WiFi", "Package of Words"], 0),
    _q("What is PoS?", ["Proof of Stake validator selection/staking", "Proof of Storage only", "Position of Sale", "Post of Sender"], 0),
    _q("What is a transaction?", ["Signed message changing state (e.g., transfer)", "HTTP GET", "CSS rule", "SQL select"], 0),
    _q("What is a wallet private key?", ["Secret controlling funds/signatures", "Public address", "Block hash", "Gas limit"], 0),
    _q("What is a public address derived from?", ["Public key material (depending on chain)", "Private browsing", "DNS", "SQL id"], 0),
    _q("What is gas (Ethereum concept)?", ["Unit measuring computation cost for transactions", "Fuel for servers", "CPU GHz", "RAM"], 0),
    _q("What is mempool?", ["Pending transactions waiting to be included", "Memory pool in OS only", "MySQL pool", "CDN cache"], 0),
    _q("What is double spending problem?", ["Spending same funds twice—blockchain aims to prevent", "Buying twice", "Two GPUs", "Two domains"], 0),
    _q("What is merkle tree used for?", ["Efficient proofs of inclusion in block data", "Graphics tree", "DOM tree", "BST only"], 0),
    _q("What is hashing property needed?", [" preimage resistance / collision resistance (concepts)", "Reversible always", "Sortable always", "Compressing video"], 0),
    _q("What is finality?", ["Confidence that transactions won't be reverted", "Infinite pending", "Gas refunds only", "SQL commit"], 0),
    _q("What is fork?", ["Chain split due to rule changes or competing blocks", "Git only", "TCP fork", "Thread fork only"], 0),
    _q("What is smart contract?", ["Code deployed on-chain defining rules automatically", "Legal PDF", "Cloud function always offchain", "CRON"], 0),
    _q("What is Solidity primarily?", ["Smart contract language on Ethereum ecosystem", "CSS preprocessor", "SQL dialect", "Shell"], 0),
    _q("What is EVM?", ["Ethereum Virtual Machine execution environment", "Edge VM", "Elastic VM", "Env variable map"], 0),
    _q("What is oracle problem?", ["Getting trustworthy off-chain data on-chain", "SQL oracle db", "DNS oracle", "Random number always easy"], 0),
    _q("What is Layer 2?", ["Scaling solutions settling to L1 (rollups/channels)", "DNS layer", "OSI L2 switches only", "CDN"], 0),
    _q("What is rollup?", ["L2 posting compressed txs/state roots to L1", "Roll-up banners", "Log rotation", "Image rollup"], 0),
    _q("What is bridge risk?", ["Smart contract trust/bugs between chains", "No risk", "HTTPS bridge", "VPN only"], 0),
    _q("What is token vs coin loosely?", ["Coin native chain asset vs token contract asset (loose usage)", "Same always", "Coin is SQL", "Token is DNS"], 0),
    _q("What is NFT?", ["Non-fungible token—unique asset id on-chain", "Not for trade", "National File Transfer", "Network FTP token"], 0),
    _q("What is DAO?", ["Decentralized autonomous organization via rules/tokens", "Data access object only in Java", "DNS authority org", "Database admin object"], 0),
    _q("What is slashing (PoS)?", ["Penalty destroying stake for misbehavior", "Slashdot website", "Cutting gas", "Deleting blocks freely"], 0),
    _q("What is 51% attack concept?", ["Controlling majority consensus power to rewrite/reorg", "51 firewalls", "51 SQL injections", "51% discount"], 0),
    _q("Why are private keys critical to protect?", ["They authorize spending and contract actions", "They are public", "They are optional", "They speed mining"], 0),
]

BC_BANKS = {1: BC_PHASE_1, 2: BC_PHASE_1, 3: BC_PHASE_1, 4: BC_PHASE_1, 5: BC_PHASE_1}


# --- AI (general) ---

AI_PHASE_1 = [
    _q("What is supervised learning?", ["Learn mapping from labeled inputs to outputs", "No labels", "Only reinforcement", "Only clustering always"], 0),
    _q("What is overfitting?", ["Model memorizes training, poor generalization", "Model too simple", "Too little data always good", "Underfitting same"], 0),
    _q("What is a feature in ML?", ["Input signal used by model", "Output only", "Hyperparameter only", "Loss only"], 0),
    _q("What is a label?", ["Target output for supervised training", "Input only", "Model weight", "Dataset filename"], 0),
    _q("What is train/validation split for?", ["Tune/evaluate without peeking at test", "Duplicate data", "Delete labels", "Increase leakage"], 0),
    _q("What is data leakage?", ["Information from outside training improperly influences", "Water cooling", "TCP leak", "GDPR export"], 0),
    _q("What is precision/recall tradeoff?", ["Different thresholds balance false positives vs false negatives", "Same metric", "Only accuracy matters always", "Only ROC"], 0),
    _q("What is an LLM?", ["Large language model predicting text tokens", "Linear logistic model", "Long latent map", "Local link manager"], 0),
    _q("What is a prompt?", ["Instruction/context text guiding model output", "A database query only", "A CSS class", "A GPU driver"], 0),
    _q("What is tokenization?", ["Splitting text into model tokens", "Encrypting tokens JWT", "SQL tokenizer", "HTML parser only"], 0),
    _q("What is hallucination in LLMs?", ["Confident but incorrect/fabricated content", "GPU overheat", "Cache miss", "Training"], 0),
    _q("What is temperature in sampling?", ["Controls randomness/creativity vs determinism", "CPU temp", "Learning rate same", "Batch size"], 0),
    _q("What is grounding?", ["Anchoring answers to retrieved/verified sources", "Electrical ground only", "GND pin", "Database ground"], 0),
    _q("What is RAG?", ["Retrieval-augmented generation combining search + LLM", "Random answer generator", "Redis as GPU", "Regex AI Gateway"], 0),
    _q("What is fine-tuning?", ["Continue training on domain-specific data", "Same as prompting always", "Same as quantization always", "Deleting weights"], 0),
    _q("What is evaluation harness for?", ["Systematic benchmarking of model behavior", "Hardware harness", "CI only not models", "DNS"], 0),
    _q("What is bias in AI ethics context?", ["Systematic unfairness/harm risk", "Model weights always unbiased", "Variance", "Noise"], 0),
    _q("What is PII handling concern with LLMs?", ["Sensitive personal data in prompts/logs", "Public data only", "GPU memory", "Tokenizer speed"], 0),
    _q("What is model card?", ["Document describing intended use, limits, metrics", "SIM card", "SD card for models", "JWT card"], 0),
    _q("What is zero-shot prompting?", ["Task without examples in prompt", "No model weights", "No GPU", "No dataset exists"], 0),
    _q("What is few-shot prompting?", ["Provide examples in prompt to steer behavior", "Always 1000 examples", "Only fine-tune", "Only RL"], 0),
    _q("What is chain-of-thought prompting?", ["Ask model to show reasoning steps", "Blockchain thoughts", "Linked list prompt", "SQL joins"], 0),
    _q("What is guardrail?", ["Policy checks/filters on inputs/outputs", "Railway guard", "Firewall only", "CSS border"], 0),
    _q("What is latency vs throughput for LLM APIs?", ["Time to first token vs tokens/sec (roughly)", "Same", "Only cost", "Only accuracy"], 0),
    _q("What is embedding vector?", ["Numeric representation of meaning/similarity", "Encrypting vector", "3D mesh", "JPEG vector"], 0),
    _q("What is clustering?", ["Unsupervised grouping by similarity", "Supervised always", "SQL cluster index", "K8s only"], 0),
    _q("What is regularization?", ["Techniques to reduce overfitting", "Increase overfitting", "Speed up only", "Add noise only always"], 0),
    _q("What is cross-validation?", ["Multiple splits to estimate performance stability", "Validate CSS", "CORS validation", "SQL cross join"], 0),
    _q("What is baseline model?", ["Simple reference to beat (e.g., majority class)", "Best possible model", "GPU baseline", "Power draw"], 0),
    _q("What is responsible AI practice?", ["Safety, privacy, monitoring, human oversight", "Ship fast ignore risks", "No logging", "No testing"], 0),
]

AI_BANKS = {1: AI_PHASE_1, 2: AI_PHASE_1, 3: AI_PHASE_1, 4: AI_PHASE_1, 5: AI_PHASE_1}


def _shuffle_options(q: dict, seed: int) -> dict:
    """Shuffle options deterministically so correct index moves."""
    import random

    rng = random.Random(seed)
    opts = list(q["options"])
    correct_text = opts[q["answer_index"]]
    rng.shuffle(opts)
    new_index = opts.index(correct_text)
    return {**q, "options": opts, "answer_index": new_index}


def rotate_bank(bank: list[dict], phase: int, stride: int = 7) -> list[dict]:
    """Return 30 questions permuted per phase so phases are not identical."""
    if not bank:
        return []
    n = len(bank)
    off = ((phase - 1) * stride) % n
    out = []
    for i in range(30):
        out.append(dict(bank[(off + i) % n]))
    return out


def pick_bank(domain: str, phase: int) -> list[dict]:
    if domain == "web":
        bank = WEB_BANKS.get(phase, WEB_PHASE_1)
    elif domain == "python":
        bank = PYTHON_BANKS.get(phase, PYTHON_PHASE_1)
    elif domain == "security":
        bank = rotate_bank(SEC_PHASE_1, phase)
    elif domain == "blockchain":
        bank = rotate_bank(BC_PHASE_1, phase)
    elif domain in ("ai", "ai_product"):
        bank = rotate_bank(AI_PHASE_1, phase)
    else:
        bank = []
    return [dict(x) for x in bank]


def diversify_with_readings(bank: list[dict], course_title: str, phase_meta: dict) -> list[dict]:
    """Prefix questions with course/phase context; lightly vary text using reading titles."""
    readings = (phase_meta.get("resources") or {}).get("reading") or []
    titles = [r.get("title", "Official documentation") for r in readings if isinstance(r, dict)] or ["Study materials"]
    phase_title = phase_meta.get("title") or "This phase"
    out = []
    for i, q in enumerate(bank):
        anchor = titles[i % len(titles)]
        qq = dict(q)
        qq["question"] = f"[{course_title} · {phase_title}] Q{i+1}: {qq['question']} (See also: {anchor}.)"
        out.append(qq)
    return out
