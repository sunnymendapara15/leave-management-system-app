import { useEffect, useState } from "react";
import { fetchLeaveTypes, submitLeaveRequest } from "../services/api";

const LeaveRequestPage = () => {
  const [types, setTypes] = useState([]);
  const [form, setForm] = useState({ leave_type_id: "", start_date: "", end_date: "", reason: "" });
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetchLeaveTypes().then((response) => setTypes(response.data));
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus(null);
    try {
      await submitLeaveRequest({
        ...form,
        leave_type_id: Number(form.leave_type_id),
      });
      setForm({ leave_type_id: "", start_date: "", end_date: "", reason: "" });
      setStatus({ type: "success", message: "Leave request submitted and awaits approval." });
    } catch (err) {
      setStatus({ type: "error", message: err.response?.data?.detail || "Unable to submit." });
    }
  };

  return (
    <div className="card">
      <h2>Request leave</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Leave type
          <select
            required
            value={form.leave_type_id}
            onChange={(event) => setForm({ ...form, leave_type_id: event.target.value })}
          >
            <option value="">Select type</option>
            {types.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Start date
          <input
            type="date"
            required
            value={form.start_date}
            onChange={(event) => setForm({ ...form, start_date: event.target.value })}
          />
        </label>
        <label>
          End date
          <input
            type="date"
            required
            value={form.end_date}
            onChange={(event) => setForm({ ...form, end_date: event.target.value })}
          />
        </label>
        <label>
          Reason
          <textarea
            value={form.reason}
            onChange={(event) => setForm({ ...form, reason: event.target.value })}
          />
        </label>
        {status && <p className={status.type}>{status.message}</p>}
        <button type="submit">Submit request</button>
      </form>
    </div>
  );
};

export default LeaveRequestPage;
