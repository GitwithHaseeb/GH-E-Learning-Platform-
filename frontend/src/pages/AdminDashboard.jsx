import { useQuery } from "@tanstack/react-query";
import api from "../services/api";

export default function AdminDashboard() {
  const { data } = useQuery({
    queryKey: ["admin-stats"],
    queryFn: async () => (await api.get("/admin/platform-stats/")).data,
  });

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold">Admin dashboard</h1>
      <div className="mt-6 grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          ["Users", data?.users],
          ["Courses", data?.courses],
          ["Enrollments", data?.enrollments],
          ["Paid orders", data?.paid_orders],
        ].map(([k, v]) => (
          <div key={k} className="rounded-xl border bg-white p-4">
            <div className="text-sm text-slate-500">{k}</div>
            <div className="text-3xl font-bold mt-1">{v ?? "—"}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
