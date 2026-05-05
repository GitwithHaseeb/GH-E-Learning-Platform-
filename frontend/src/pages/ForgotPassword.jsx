import { useState } from "react";
import api from "../services/api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const submit = async (e) => {
    e.preventDefault();
    const res = await api.post("/auth/password/reset/", { email });
    setMsg(res.data.detail);
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <h1 className="text-2xl font-semibold">Forgot password</h1>
      <form onSubmit={submit} className="mt-6 space-y-3">
        <input className="w-full border rounded-lg px-3 py-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <button className="w-full rounded-lg bg-brand-600 text-white py-2 font-semibold">Send reset link</button>
      </form>
      {msg && <p className="text-sm text-slate-600 mt-4">{msg}</p>}
    </div>
  );
}
