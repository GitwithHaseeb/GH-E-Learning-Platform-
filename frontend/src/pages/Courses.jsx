import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import api from "../services/api";

function fallbackImage(slug) {
  const s = (slug || "").toLowerCase();
  const words = s.replace(/-/g, " ").split(/\s+/);
  const hasWord = (w) => words.includes(w);
  let icon = "💻";
  let label = "Technology Course";
  if (s.includes("blockchain")) {
    icon = "⛓️";
    label = "Blockchain";
  } else if (hasWord("ai") || s.includes("prompt") || s.includes("machine-learning")) {
    icon = "🤖";
    label = "AI Course";
  } else if (s.includes("web") || s.includes("react") || s.includes("javascript") || s.includes("typescript")) {
    icon = "🌐";
    label = "Web Development";
  } else if (s.includes("security") || s.includes("hacking") || s.includes("soc")) {
    icon = "🛡️";
    label = "Cyber Security";
  } else if (s.includes("mobile") || s.includes("flutter") || s.includes("native")) {
    icon = "📱";
    label = "Mobile Development";
  } else if (s.includes("seo") || s.includes("marketing")) {
    icon = "📈";
    label = "SEO & Marketing";
  } else if (s.includes("data") || s.includes("sql")) {
    icon = "📊";
    label = "Data & Analytics";
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f172a'/></linearGradient></defs><rect width='640' height='360' fill='url(#g)'/><text x='50%' y='42%' dominant-baseline='middle' text-anchor='middle' font-size='82'>${icon}</text><text x='50%' y='62%' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='34' fill='white'>${label}</text></svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

export default function Courses() {
  const { data, isLoading } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => (await api.get("/courses/")).data,
  });

  if (isLoading) return <div className="p-8 text-center">Loading courses…</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold">All courses</h1>
      <p className="text-slate-600 mt-1">
        Choose from free, market-relevant courses with clear duration and structured learning outcomes.
      </p>
      <div className="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {(data?.results || data || []).map((c) => (
          <Link key={c.id} to={`/courses/${c.slug}`} className="rounded-xl border bg-white overflow-hidden hover:shadow">
            {c.display_image ? (
              <img
                src={c.display_image}
                alt={c.title}
                className="h-40 w-full object-cover"
                loading="lazy"
                onError={(e) => {
                  e.currentTarget.onerror = null;
                  e.currentTarget.src = fallbackImage(c.slug);
                }}
              />
            ) : (
              <div className="h-40 w-full bg-slate-100" />
            )}
            <div className="p-4">
              <div className="font-medium">{c.title}</div>
              <div className="text-sm text-slate-500 mt-1">{c.subtitle}</div>
              <div className="text-sm mt-2 flex items-center justify-between">
                <span>{c.pricing === "free" ? "Free" : `$${(c.price_cents / 100).toFixed(2)}`}</span>
                <span className="text-slate-500">{c.duration_months} month(s)</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
