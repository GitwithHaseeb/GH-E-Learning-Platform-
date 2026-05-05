import { useForm } from "react-hook-form";
import { useAuthStore } from "../store/authStore";
import api from "../services/api";

export default function Profile() {
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const { register, handleSubmit } = useForm({
    defaultValues: { first_name: user?.first_name || "", last_name: user?.last_name || "" },
  });

  const onSave = async (values) => {
    const res = await api.patch("/users/me/", values);
    setUser(res.data);
  };

  const onPass = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    await api.post("/users/me/password/", {
      old_password: fd.get("old_password"),
      new_password: fd.get("new_password"),
      new_password_confirm: fd.get("new_password_confirm"),
    });
    alert("Password update ho gaya");
    e.target.reset();
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-10 space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">Profile</h1>
        <p className="text-slate-600 text-sm mt-1">{user?.email}</p>
      </div>
      <form onSubmit={handleSubmit(onSave)} className="space-y-3 border rounded-xl p-4 bg-white">
        <h2 className="font-medium">Edit name</h2>
        <input className="w-full border rounded-lg px-3 py-2" placeholder="First name" {...register("first_name")} />
        <input className="w-full border rounded-lg px-3 py-2" placeholder="Last name" {...register("last_name")} />
        <button className="rounded-lg bg-brand-600 text-white px-4 py-2">Save</button>
      </form>
      <form onSubmit={onPass} className="space-y-3 border rounded-xl p-4 bg-white">
        <h2 className="font-medium">Change password</h2>
        <input className="w-full border rounded-lg px-3 py-2" name="old_password" type="password" placeholder="Old password" />
        <input className="w-full border rounded-lg px-3 py-2" name="new_password" type="password" placeholder="New password" />
        <input
          className="w-full border rounded-lg px-3 py-2"
          name="new_password_confirm"
          type="password"
          placeholder="Confirm new password"
        />
        <button className="rounded-lg bg-slate-900 text-white px-4 py-2">Update password</button>
      </form>
    </div>
  );
}
