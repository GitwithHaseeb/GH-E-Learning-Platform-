import { useState } from "react";
import { useLocation } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import api from "../services/api";

export default function Checkout() {
  const { state } = useLocation();
  const [slug, setSlug] = useState(state?.slug || "");
  const [coupon, setCoupon] = useState("");
  const m = useMutation({
    mutationFn: async () => {
      const res = await api.post("/checkout/create/", { course_slug: slug, coupon_code: coupon });
      return res.data;
    },
  });

  return (
    <div className="max-w-xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold">Checkout</h1>
      <p className="text-slate-600 mt-2">Stripe test mode — backend `STRIPE_SECRET_KEY` set karein.</p>
      <div className="mt-6 space-y-3">
        <label className="block text-sm font-medium">Course slug</label>
        <input
          className="w-full border rounded-lg px-3 py-2"
          value={slug}
          onChange={(e) => setSlug(e.target.value)}
          placeholder="e.g. python-101"
        />
        <label className="block text-sm font-medium">Coupon (optional)</label>
        <input className="w-full border rounded-lg px-3 py-2" value={coupon} onChange={(e) => setCoupon(e.target.value)} />
        <button
          type="button"
          disabled={!slug || m.isPending}
          onClick={() => m.mutate()}
          className="w-full rounded-lg bg-brand-600 text-white py-2 font-semibold disabled:opacity-50"
        >
          Pay with Stripe
        </button>
        {m.data?.checkout_url && (
          <a className="block text-center text-brand-700 underline" href={m.data.checkout_url}>
            Stripe checkout page open karein
          </a>
        )}
        {m.data?.detail && <p className="text-sm text-slate-600">{m.data.detail}</p>}
        {m.data?.order && (
          <pre className="text-xs bg-slate-100 p-2 rounded overflow-auto">{JSON.stringify(m.data.order, null, 2)}</pre>
        )}
      </div>
    </div>
  );
}
