import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuthStore } from "../store/authStore";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export default function Login() {
  const nav = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);
  const setUser = useAuthStore((s) => s.setUser);
  const { register, handleSubmit, formState } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = async (values) => {
    const res = await api.post("/auth/login/", values);
    setTokens(res.data.access, res.data.refresh);
    const me = await api.get("/users/me/");
    setUser(me.data);
    nav("/dashboard");
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <h1 className="text-2xl font-semibold">Login</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-3">
        <input className="w-full border rounded-lg px-3 py-2" placeholder="Email" {...register("email")} />
        <input className="w-full border rounded-lg px-3 py-2" type="password" placeholder="Password" {...register("password")} />
        {formState.errors.email && <p className="text-sm text-red-600">{formState.errors.email.message}</p>}
        <button type="submit" className="w-full rounded-lg bg-brand-600 text-white py-2 font-semibold">
          Login
        </button>
      </form>
      <p className="text-sm text-slate-600 mt-4">
        <Link className="text-brand-700" to="/forgot-password">
          Forgot password?
        </Link>{" "}
        ·{" "}
        <Link className="text-brand-700" to="/signup">
          Signup
        </Link>
      </p>
    </div>
  );
}
