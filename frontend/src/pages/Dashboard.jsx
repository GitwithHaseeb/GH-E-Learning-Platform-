import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Dashboard() {
  const { data } = useQuery({
    queryKey: ["enrollments"],
    queryFn: async () => (await api.get("/student/enrollments/")).data,
  });
  const { data: certs } = useQuery({
    queryKey: ["certificates"],
    queryFn: async () => (await api.get("/student/certificates/")).data,
  });

  const list = data?.results || data || [];

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold">My courses</h1>
      <div className="mt-6 grid md:grid-cols-2 gap-4">
        {list.map((e) => (
          <Link key={e.id} to={`/learn/${e.course_slug}`} className="border rounded-xl p-4 bg-white hover:shadow">
            <div className="font-medium">{e.course_title}</div>
            <div className="text-sm text-slate-600 mt-2">Progress: {e.progress_percent}%</div>
          </Link>
        ))}
        {list.length === 0 && <p className="text-slate-600">No enrollments yet — explore and join a course.</p>}
      </div>
      <h2 className="text-xl font-semibold mt-10">Certificates</h2>
      <div className="mt-4 grid md:grid-cols-2 gap-4">
        {(certs?.results || certs || []).map((c) => (
          <a
            key={c.id}
            href={c.pdf_file || "#"}
            target="_blank"
            rel="noreferrer"
            className="border rounded-xl p-4 bg-white hover:shadow"
          >
            <div className="font-medium">{c.course_title}</div>
            <div className="text-sm text-slate-600 mt-1">Code: {c.code}</div>
          </a>
        ))}
        {(certs?.results || certs || []).length === 0 && (
          <p className="text-slate-600">Complete all 5 phases in a course to receive your certificate.</p>
        )}
      </div>
    </div>
  );
}
