import { useEffect, useState } from "react";
import {
  createLeaveType,
  deleteLeaveType,
  fetchLeaveTypes,
  updateLeaveType,
} from "../services/api";

const LeaveTypesPage = () => {
  const [types, setTypes] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", annual_days: 0, requires_approval: true });
  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({ description: "", annual_days: 0, requires_approval: true });
  const [message, setMessage] = useState(null);

  const loadTypes = () => {
    fetchLeaveTypes()
      .then((response) => setTypes(response.data))
      .catch((err) => setMessage({ type: "error", message: err.message }));
  };

  useEffect(() => {
    loadTypes();
  }, []);

  const handleCreate = async (event) => {
    event.preventDefault();
    setMessage(null);
    try {
      await createLeaveType(form);
      setForm({ name: "", description: "", annual_days: 0, requires_approval: true });
      loadTypes();
      setMessage({ type: "success", message: "Leave type created." });
    } catch (err) {
      setMessage({ type: "error", message: err.response?.data?.detail || "Unable to create type." });
    }
  };

  const handleDelete = async (typeId) => {
    if (!window.confirm("Remove this leave type?")) return;
    try {
      await deleteLeaveType(typeId);
      loadTypes();
      setMessage({ type: "success", message: "Leave type removed." });
    } catch (err) {
      setMessage({ type: "error", message: err.response?.data?.detail || "Unable to remove type." });
    }
  };

  const startEdit = (type) => {
    setEditId(type.id);
    setEditForm({
      description: type.description || "",
      annual_days: type.annual_days,
      requires_approval: type.requires_approval,
    });
  };

  const handleUpdate = async (event) => {
    event.preventDefault();
    try {
      await updateLeaveType(editId, editForm);
      setEditId(null);
      loadTypes();
      setMessage({ type: "success", message: "Leave type updated." });
    } catch (err) {
      setMessage({ type: "error", message: err.response?.data?.detail || "Unable to update." });
    }
  };

  return (
    <div className="page">
      <h2>Manage leave types</h2>
      {message && <p className={message.type}>{message.message}</p>}
      <section>
        <form className="grid" onSubmit={handleCreate}>
          <label>
            Name
            <input
              value={form.name}
              required
              onChange={(event) => setForm({ ...form, name: event.target.value })}
            />
          </label>
          <label>
            Description
            <textarea
              value={form.description}
              onChange={(event) => setForm({ ...form, description: event.target.value })}
            />
          </label>
          <label>
            Annual days
            <input
              type="number"
              min={0}
              value={form.annual_days}
              onChange={(event) => setForm({ ...form, annual_days: Number(event.target.value) })}
            />
          </label>
          <label>
            Requires approval
            <select
              value={form.requires_approval ? "true" : "false"}
              onChange={(event) =>
                setForm({ ...form, requires_approval: event.target.value === "true" })
              }
            >
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </label>
          <button type="submit">Add type</button>
        </form>
      </section>
      <section>
        <h3>Existing types</h3>
        <ul className="list">
          {types.map((type) => (
            <li key={type.id}>
              <div>
                <strong>{type.name}</strong>
                <p>{type.description}</p>
                <span>{type.annual_days} days annually</span>
                <span>Requires approval: {type.requires_approval ? "Yes" : "No"}</span>
              </div>
              <div className="actions">
                <button type="button" onClick={() => startEdit(type)}>
                  Edit
                </button>
                <button type="button" onClick={() => handleDelete(type.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </section>
      {editId && (
        <section>
          <h3>Update type</h3>
          <form className="grid" onSubmit={handleUpdate}>
            <label>
              Description
              <textarea
                value={editForm.description}
                onChange={(event) => setEditForm({ ...editForm, description: event.target.value })}
              />
            </label>
            <label>
              Annual days
              <input
                type="number"
                min={0}
                value={editForm.annual_days}
                onChange={(event) =>
                  setEditForm({ ...editForm, annual_days: Number(event.target.value) })
                }
              />
            </label>
            <label>
              Requires approval
              <select
                value={editForm.requires_approval ? "true" : "false"}
                onChange={(event) =>
                  setEditForm({ ...editForm, requires_approval: event.target.value === "true" })
                }
              >
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </label>
            <div className="actions">
              <button type="button" onClick={() => setEditId(null)}>
                Cancel
              </button>
              <button type="submit">Save</button>
            </div>
          </form>
        </section>
      )}
    </div>
  );
};

export default LeaveTypesPage;
