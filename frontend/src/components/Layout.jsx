import { Outlet, Link, NavLink } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function Layout() {
  const { access, user, logout } = useAuthStore();
  const link = "px-3 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-100";
  const active = ({ isActive }) =>
    `${link} ${isActive ? "bg-brand-50 text-brand-700" : ""}`;

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-white/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3">
          <Link to="/" className="font-semibold text-brand-700 flex items-center gap-2">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-brand-700 text-white text-xs font-bold">
              GH
            </span>
            E‑Learn
          </Link>
          <nav className="flex flex-wrap items-center gap-1">
            <NavLink to="/courses" className={active}>
              Courses
            </NavLink>
            {access ? (
              <>
                <NavLink to="/dashboard" className={active}>
                  Dashboard
                </NavLink>
                {(user?.role === "instructor" || user?.role === "admin") && (
                  <NavLink to="/instructor" className={active}>
                    Instructor
                  </NavLink>
                )}
                {user?.role === "admin" && (
                  <NavLink to="/admin" className={active}>
                    Admin
                  </NavLink>
                )}
                <NavLink to="/profile" className={active}>
                  Profile
                </NavLink>
                <button type="button" className={link} onClick={() => logout()}>
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" className={active}>
                  Login
                </NavLink>
                <NavLink to="/signup" className={active}>
                  Signup
                </NavLink>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
      <footer className="border-t bg-white py-6 text-center text-sm text-slate-600">
        <p>Designed by Ghania Tanveer and Muhammad Haseeb</p>
        <div className="mt-2 flex items-center justify-center gap-4">
          <a
            href="https://www.linkedin.com/in/ghania-tanveer-894625311/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 hover:text-brand-700"
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current" aria-hidden="true">
              <path d="M20.45 20.45H16.9v-5.57c0-1.33-.03-3.05-1.86-3.05-1.86 0-2.14 1.45-2.14 2.95v5.67H9.35V9h3.4v1.56h.05c.47-.9 1.64-1.86 3.38-1.86 3.61 0 4.27 2.38 4.27 5.47v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.72V1.72C24 .77 23.21 0 22.23 0z" />
            </svg>
            Ghania Tanveer
          </a>
          <a
            href="https://www.linkedin.com/in/muhammad-haseeb-5a73bb317"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 hover:text-brand-700"
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current" aria-hidden="true">
              <path d="M20.45 20.45H16.9v-5.57c0-1.33-.03-3.05-1.86-3.05-1.86 0-2.14 1.45-2.14 2.95v5.67H9.35V9h3.4v1.56h.05c.47-.9 1.64-1.86 3.38-1.86 3.61 0 4.27 2.38 4.27 5.47v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.72V1.72C24 .77 23.21 0 22.23 0z" />
            </svg>
            Muhammad Haseeb
          </a>
        </div>
      </footer>
    </div>
  );
}
