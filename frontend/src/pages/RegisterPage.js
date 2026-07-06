import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const RegisterPage = () => {
  const navigate = useNavigate();
  const { signUp } = useAuth();
  const [form, setForm] = useState({ email: "", password: "", full_name: "" });
  const [error, setError] = useState(null);

  const onSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    try {
      await signUp(form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to register.");
    }
  };

  return (
    <div className="card">
      <h2>Create an account</h2>
      <form onSubmit={onSubmit}>
        <label>
          Full name
          <input
            type="text"
            value={form.full_name}
            onChange={(event) => setForm({ ...form, full_name: event.target.value })}
          />
        </label>
        <label>
          Email
          <input
            type="email"
            required
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
          />
        </label>
        <label>
          Password
          <input
            type="password"
            required
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit">Create account</button>
      </form>
    </div>
  );
};

export default RegisterPage;
