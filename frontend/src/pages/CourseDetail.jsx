import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";
import { useAuthStore } from "../store/authStore";
import { useState } from "react";

function fallbackImage(slug) {
  const s = (slug || "").toLowerCase();
  const words = s.replace(/-/g, " ").split(/\s+/);
  const hasWord = (w) => words.includes(w);
  let icon = "💻";
  let label = "Technology Course";
  if (s.includes("blockchain")) {
    icon = "⛓️";
    label = "Blockchain Course";
  } else if (hasWord("ai") || s.includes("prompt")) {
    icon = "🤖";
    label = "AI Course";
  } else if (s.includes("web") || s.includes("react")) {
    icon = "🌐";
    label = "Web Development";
  } else if (s.includes("security") || s.includes("hacking") || s.includes("soc")) {
    icon = "🛡️";
    label = "Cyber Security";
  } else if (s.includes("mobile") || s.includes("flutter") || s.includes("native")) {
    icon = "📱";
    label = "Mobile Development";
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='900' height='480'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f172a'/></linearGradient></defs><rect width='900' height='480' fill='url(#g)'/><text x='50%' y='42%' dominant-baseline='middle' text-anchor='middle' font-size='100'>${icon}</text><text x='50%' y='62%' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='42' fill='white'>${label}</text></svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

export default function CourseDetail() {
  const { slug } = useParams();
  const qc = useQueryClient();
  const access = useAuthStore((s) => s.access);
  const [enrollMsg, setEnrollMsg] = useState("");
  const [showPhaseChapters, setShowPhaseChapters] = useState(false);
  const [activePhase, setActivePhase] = useState(1);

  const { data: course, isLoading } = useQuery({
    queryKey: ["course", slug],
    queryFn: async () => (await api.get(`/courses/${slug}/`)).data,
  });

  const enroll = useMutation({
    mutationFn: () => api.post(`/courses/${slug}/enroll/`),
    onSuccess: () => {
      setEnrollMsg("Enrolled successfully. Start Phase 1 now.");
      qc.invalidateQueries({ queryKey: ["course", slug] });
      qc.invalidateQueries({ queryKey: ["enrollments"] });
    },
    onError: (e) => {
      const detail = e?.response?.data?.detail || "Unable to enroll right now.";
      setEnrollMsg(String(detail));
    },
  });

  if (isLoading) return <div className="p-8 text-center">Loading…</div>;
  if (!course) return <div className="p-8">Not found</div>;
  const selectedPhase = (course.phases || []).find((p) => p.phase_number === activePhase);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 grid lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2">
        <h1 className="text-3xl font-bold">{course.title}</h1>
        <p className="text-slate-600 mt-2">{course.subtitle}</p>
        {course.display_image && (
          <img
            src={course.display_image}
            alt={course.title}
            className="mt-5 w-full h-72 object-cover rounded-xl border"
            onError={(e) => {
              e.currentTarget.onerror = null;
              e.currentTarget.src = fallbackImage(course.slug);
            }}
          />
        )}
        <div className="prose prose-slate mt-6 whitespace-pre-wrap">{course.description}</div>
        <div className="mt-8 rounded-xl border bg-white p-6">
          <h2 className="text-3xl font-semibold">What you'll learn</h2>
          <div className="mt-4 grid md:grid-cols-2 gap-3">
            {(course.learning_outcomes || []).map((item, idx) => (
              <div key={idx} className="text-slate-700 flex items-start gap-2">
                <span className="mt-1 text-brand-700">✓</span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-8">
          <h2 className="text-3xl font-semibold">Explore related topics</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {(course.related_topics || []).map((t, idx) => (
              <span key={idx} className="px-3 py-2 rounded-xl border bg-white text-sm font-medium">
                {t}
              </span>
            ))}
          </div>
        </div>
        <div className="mt-8">
          <h2 className="text-3xl font-semibold">Requirements</h2>
          <ul className="mt-3 list-disc ml-6 space-y-2 text-slate-700">
            {(course.requirements || []).map((r, idx) => (
              <li key={idx}>{r}</li>
            ))}
          </ul>
        </div>
        <div className="mt-8">
          <button
            type="button"
            onClick={() => setShowPhaseChapters((v) => !v)}
            className="rounded-lg bg-brand-600 text-white px-4 py-2 font-medium"
          >
            {showPhaseChapters ? "Hide chapter details" : "View phase chapter details"}
          </button>
        </div>
        {showPhaseChapters && (
          <div className="mt-6 rounded-xl border bg-white p-5">
            <div className="flex flex-wrap gap-2 mb-4">
              {(course.phases || []).map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setActivePhase(p.phase_number)}
                  className={`px-3 py-2 rounded-md border text-sm ${
                    activePhase === p.phase_number ? "bg-brand-50 border-brand-600 text-brand-700" : "bg-white"
                  }`}
                >
                  Phase {p.phase_number}
                </button>
              ))}
            </div>
            {selectedPhase ? (
              <>
                <h3 className="text-lg font-semibold">{selectedPhase.title}</h3>
                <p className="text-slate-600 mt-1">{selectedPhase.description}</p>
                <div className="mt-3 prose prose-slate whitespace-pre-wrap">{selectedPhase.content}</div>
                <div className="mt-4">
                  <h4 className="font-medium">Reading resources</h4>
                  <ul className="mt-2 space-y-1">
                    {(selectedPhase.resources?.reading || []).map((r, idx) => (
                      <li key={idx}>
                        <a href={r.url} target="_blank" rel="noreferrer" className="text-brand-700 underline">
                          {r.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="mt-4">
                  <h4 className="font-medium">Video lectures</h4>
                  <ul className="mt-2 space-y-1">
                    {(selectedPhase.resources?.videos || []).map((r, idx) => (
                      <li key={idx}>
                        <a href={r.url} target="_blank" rel="noreferrer" className="text-brand-700 underline">
                          {r.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="mt-4">
                  <h4 className="font-medium">Numerical checkpoints</h4>
                  <ul className="mt-2 list-disc ml-6 text-slate-700 space-y-1">
                    {(selectedPhase.resources?.data_points || []).map((p, idx) => (
                      <li key={idx}>{p}</li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <p className="text-slate-500">No phase data available.</p>
            )}
          </div>
        )}
        <h2 className="text-xl font-semibold mt-10">Curriculum</h2>
        <ol className="mt-3 space-y-2">
          {(course.lessons || []).map((l) => (
            <li key={l.id} className="border rounded-lg p-3 bg-white">
              {l.order}. {l.title}{" "}
              <span className="text-xs text-slate-500">({l.lesson_type})</span>
            </li>
          ))}
        </ol>
        <h2 className="text-xl font-semibold mt-10">5 Learning Phases</h2>
        <div className="mt-3 grid sm:grid-cols-2 gap-3">
          {(course.phases || []).map((p) => (
            <Link
              key={p.id}
              to={`/learn/${slug}?phase=${p.phase_number}`}
              className="border rounded-lg p-4 bg-white hover:border-brand-600 hover:bg-brand-50 transition"
            >
              <div className="font-medium">
                Phase {p.phase_number}: {p.title}
              </div>
              <p className="text-sm text-slate-600 mt-1">
                {p.description || "Click to start this phase and take the 30-MCQ checkpoint quiz."}
              </p>
            </Link>
          ))}
        </div>
      </div>
      <aside className="space-y-4">
        <div className="rounded-xl border bg-white p-4 shadow-sm">
          <div className="text-2xl font-bold">
            {course.pricing === "free" ? "Free" : `$${(course.price_cents / 100).toFixed(2)}`}
          </div>
          <div className="text-sm text-emerald-700 mt-1 font-medium">100% free access</div>
          <div className="text-sm text-slate-600 mt-1">Level: {course.level}</div>
          <div className="text-sm text-slate-600">Duration: {course.duration_months} month(s)</div>
          <div className="text-sm text-slate-600">Rating: ★ {course.average_rating}</div>
          {access ? (
            <div className="mt-4 flex flex-col gap-2">
              {!course.is_enrolled ? (
                <button
                  type="button"
                  onClick={() => enroll.mutate()}
                  className="w-full rounded-lg bg-brand-600 text-white py-2 font-medium"
                  disabled={enroll.isPending}
                >
                  {enroll.isPending ? "Enrolling..." : "Enroll"}
                </button>
              ) : (
                <div className="w-full rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-700 py-2 text-center font-medium">
                  Enrolled
                </div>
              )}
              {enrollMsg && <p className="text-xs text-slate-600 text-center">{enrollMsg}</p>}
              <Link to={`/learn/${slug}`} className="text-center text-brand-700 font-medium">
                Continue learning
              </Link>
            </div>
          ) : (
            <Link to="/login" className="mt-4 block text-center rounded-lg bg-brand-600 text-white py-2 font-medium">
              Sign up / Login to enroll
            </Link>
          )}
        </div>
      </aside>
    </div>
  );
}
