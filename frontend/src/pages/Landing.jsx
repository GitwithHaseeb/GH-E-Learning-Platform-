import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";

function fallbackImage(slug) {
  const s = (slug || "").toLowerCase();
  const words = s.replace(/-/g, " ").split(/\s+/);
  const hasWord = (w) => words.includes(w);
  let icon = "💻";
  let label = "Tech";
  if (s.includes("blockchain")) {
    icon = "⛓️";
    label = "Blockchain";
  } else if (hasWord("ai") || s.includes("prompt")) {
    icon = "🤖";
    label = "AI";
  } else if (s.includes("web") || s.includes("react")) {
    icon = "🌐";
    label = "Web";
  } else if (s.includes("security") || s.includes("hacking") || s.includes("soc")) {
    icon = "🛡️";
    label = "Security";
  } else if (s.includes("marketing") || s.includes("seo")) {
    icon = "📈";
    label = "Marketing";
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f172a'/></linearGradient></defs><rect width='640' height='360' fill='url(#g)'/><text x='50%' y='42%' dominant-baseline='middle' text-anchor='middle' font-size='82'>${icon}</text><text x='50%' y='62%' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='34' fill='white'>${label}</text></svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

export default function Landing() {
  const { data: featured } = useQuery({
    queryKey: ["featured"],
    queryFn: async () => (await api.get("/courses/featured/")).data,
  });

  return (
    <div>
      <section className="bg-gradient-to-br from-brand-900 via-brand-700 to-brand-600 text-white">
        <div className="max-w-6xl mx-auto px-4 py-20">
          <motion.h1
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-bold tracking-tight"
          >
            Learn high-demand skills at your pace.
          </motion.h1>
          <p className="mt-4 text-lg text-blue-100 max-w-2xl">
            Free professional courses across SEO, Marketing, Python, Java, C++, AI, Data, DevOps, and more.
            Follow a structured 5-phase learning path with quizzes and completion certificates.
          </p>
          <div className="mt-8 flex gap-3">
            <Link
              to="/courses"
              className="inline-flex items-center rounded-lg bg-white px-5 py-3 text-brand-700 font-semibold shadow"
            >
              Explore courses
            </Link>
            <Link to="/signup" className="inline-flex items-center rounded-lg border border-white/40 px-5 py-3">
              Start free
            </Link>
          </div>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-2xl font-semibold">Featured programs</h2>
        <div className="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {(featured || []).map((c) => (
            <Link
              key={c.id}
              to={`/courses/${c.slug}`}
              className="rounded-xl border bg-white p-4 shadow-sm hover:shadow-md transition"
            >
              {c.display_image ? (
                <img
                  src={c.display_image}
                  alt={c.title}
                  className="h-36 w-full object-cover rounded-lg mb-3"
                  loading="lazy"
                  onError={(e) => {
                    e.currentTarget.onerror = null;
                    e.currentTarget.src = fallbackImage(c.slug);
                  }}
                />
              ) : (
                <div className="h-36 w-full rounded-lg bg-slate-100 mb-3" />
              )}
              <div className="font-medium">{c.title}</div>
              <div className="text-sm text-slate-500 mt-1">
                {c.pricing === "free" ? "Free" : `$${(c.price_cents / 100).toFixed(2)}`} · {c.duration_months} month(s)
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="bg-slate-100 py-16">
        <div className="max-w-6xl mx-auto px-4 grid md:grid-cols-3 gap-8">
          {[
            { t: "Structured learning", d: "Every course follows a complete 5-phase roadmap." },
            { t: "Phase quizzes", d: "After each phase, take a 30-question quick quiz to unlock the next one." },
            { t: "Certificates", d: "Complete all 5 phases and receive your course completion certificate." },
          ].map((x) => (
            <div key={x.t} className="rounded-xl bg-white p-6 border">
              <h3 className="font-semibold">{x.t}</h3>
              <p className="text-slate-600 mt-2 text-sm">{x.d}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
