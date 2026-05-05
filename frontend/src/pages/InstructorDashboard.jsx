import { useQuery } from "@tanstack/react-query";
import { Bar } from "react-chartjs-2";
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import api from "../services/api";

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function InstructorDashboard() {
  const { data } = useQuery({
    queryKey: ["instructor-analytics"],
    queryFn: async () => (await api.get("/instructor/analytics/")).data,
  });

  const chartData = {
    labels: ["Courses", "Enrollments", "Revenue ($)"],
    datasets: [
      {
        label: "Stats",
        data: [data?.courses_count || 0, data?.enrollments_count || 0, (data?.revenue_cents || 0) / 100],
        backgroundColor: ["#2563eb", "#10b981", "#f59e0b"],
      },
    ],
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold">Instructor analytics</h1>
      <p className="text-slate-600 mt-1">Enrollment + revenue aggregation (paid orders).</p>
      <div className="mt-8 max-w-xl bg-white border rounded-xl p-4">
        <Bar data={chartData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
      </div>
    </div>
  );
}
