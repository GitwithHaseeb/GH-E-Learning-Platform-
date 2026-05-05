import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import api from "../services/api";
import { useAuthStore } from "../store/authStore";

const schema = z
  .object({
    email: z.string().email(),
    password: z.string().min(8),
    password_confirm: z.string().min(8),
    first_name: z.string().optional(),
    last_name: z.string().optional(),
    role: z.enum(["student", "instructor"]),
  })
  .refine((d) => d.password === d.password_confirm, { path: ["password_confirm"], message: "Passwords match nahi" });

export default function Signup() {
  const nav = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);
  const setUser = useAuthStore((s) => s.setUser);
  const { register, handleSubmit, formState } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { role: "student" },
  });

  const onSubmit = async (values) => {
    const res = await axios.post("/api/v1/auth/register/", values);
    setTokens(res.data.access, res.data.refresh);
    setUser(res.data.user);
    nav("/dashboard");
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <h1 className="text-2xl font-semibold">Signup</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-3">
        <input className="w-full border rounded-lg px-3 py-2" placeholder="Email" {...register("email")} />
        <input className="w-full border rounded-lg px-3 py-2" type="password" placeholder="Password" {...register("password")} />
        <input
          className="w-full border rounded-lg px-3 py-2"
          type="password"
          placeholder="Confirm password"
          {...register("password_confirm")}
        />
        <input className="w-full border rounded-lg px-3 py-2" placeholder="First name" {...register("first_name")} />
        <input className="w-full border rounded-lg px-3 py-2" placeholder="Last name" {...register("last_name")} />
        <select className="w-full border rounded-lg px-3 py-2" {...register("role")}>
          <option value="student">Student</option>
          <option value="instructor">Instructor</option>
        </select>
        {formState.errors.password_confirm && (
          <p className="text-sm text-red-600">{formState.errors.password_confirm.message}</p>
        )}
        <button type="submit" className="w-full rounded-lg bg-brand-600 text-white py-2 font-semibold">
          Create account
        </button>
      </form>
      <p className="text-sm text-slate-600 mt-4">
        <Link className="text-brand-700" to="/login">
          Login
        </Link>
      </p>
    </div>
  );
}
