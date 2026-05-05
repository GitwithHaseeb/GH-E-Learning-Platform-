import { lazy, Suspense } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import { useAuthStore } from "./store/authStore";
import Layout from "./components/Layout.jsx";
import ErrorBoundary from "./components/ErrorBoundary.jsx";

const Landing = lazy(() => import("./pages/Landing.jsx"));
const Courses = lazy(() => import("./pages/Courses.jsx"));
const CourseDetail = lazy(() => import("./pages/CourseDetail.jsx"));
const Player = lazy(() => import("./pages/Player.jsx"));
const Dashboard = lazy(() => import("./pages/Dashboard.jsx"));
const InstructorDashboard = lazy(() => import("./pages/InstructorDashboard.jsx"));
const AdminDashboard = lazy(() => import("./pages/AdminDashboard.jsx"));
const Checkout = lazy(() => import("./pages/Checkout.jsx"));
const Login = lazy(() => import("./pages/Login.jsx"));
const Signup = lazy(() => import("./pages/Signup.jsx"));
const ForgotPassword = lazy(() => import("./pages/ForgotPassword.jsx"));
const Profile = lazy(() => import("./pages/Profile.jsx"));

function Protected({ children, roles }) {
  const { access, user } = useAuthStore();
  if (!access) return <Navigate to="/login" replace />;
  if (roles && user && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <ErrorBoundary>
      <Suspense fallback={<div className="p-8 text-center text-slate-600">Loading…</div>}>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Landing />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/courses/:slug" element={<CourseDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route
              path="/learn/:slug"
              element={
                <Protected>
                  <Player />
                </Protected>
              }
            />
            <Route
              path="/dashboard"
              element={
                <Protected>
                  <Dashboard />
                </Protected>
              }
            />
            <Route
              path="/instructor"
              element={
                <Protected roles={["instructor", "admin"]}>
                  <InstructorDashboard />
                </Protected>
              }
            />
            <Route
              path="/admin"
              element={
                <Protected roles={["admin"]}>
                  <AdminDashboard />
                </Protected>
              }
            />
            <Route
              path="/checkout"
              element={
                <Protected>
                  <Checkout />
                </Protected>
              }
            />
            <Route
              path="/profile"
              element={
                <Protected>
                  <Profile />
                </Protected>
              }
            />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}
