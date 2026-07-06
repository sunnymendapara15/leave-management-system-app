import { useEffect, useState } from "react";
import { fetchEntitlements, fetchLeaveRequests, fetchPendingRequests } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

const normalizeArray = (value) => {
  if (Array.isArray(value)) {
    return value;
  }
  console.warn("Expected an array but received", value);
  return [];
};

const DashboardPage = () => {
  const { user } = useAuth();
  const [entitlements, setEntitlements] = useState([]);
  const [requests, setRequests] = useState([]);
  const [pendingRequests, setPendingRequests] = useState([]);
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    setLoading(true);
    try {
      const [entRes, reqRes] = await Promise.all([
        fetchEntitlements(),
        fetchLeaveRequests(),
      ]);
      setEntitlements(normalizeArray(entRes.data));
      setRequests(normalizeArray(reqRes.data));
      if (user?.role === "manager" || user?.role === "admin") {
        const pending = await fetchPendingRequests();
        setPendingRequests(normalizeArray(pending.data));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [user]);

  return (
    <div className="page">
      <h2>My dashboard</h2>
      {loading && <p>Refreshing...</p>}
      <section>
        <h3>Leave balances</h3>
        <div className="grid">
          {entitlements.map((ent) => (
            <article key={ent.leave_type.id}>
              <h4>{ent.leave_type.name}</h4>
              <p>{ent.leave_type.description}</p>
              <p>
                Available: <strong>{ent.total_days - ent.used_days - ent.reserved_days}</strong>
              </p>
              <p>Used: {ent.used_days}</p>
              <p>Reserved: {ent.reserved_days}</p>
            </article>
          ))}
        </div>
      </section>
      <section>
        <h3>My leave history</h3>
        <ul className="list">
          {requests.map((item) => (
            <li key={item.id}>
              <div>
                <strong>{item.leave_type.name}</strong>
                <span>
                  {item.start_date} → {item.end_date}
                </span>
              </div>
              <p>{item.reason}</p>
              <small>
                {item.status} · {item.requested_days} days
              </small>
              {item.manager_comment && <p className="muted">Manager note: {item.manager_comment}</p>}
            </li>
          ))}
        </ul>
      </section>
      {(user?.role === "manager" || user?.role === "admin") && (
        <section>
          <h3>Pending approvals</h3>
          <ul className="list">
            {pendingRequests.map((item) => (
              <li key={item.id}>
                <div>
                  <strong>{item.leave_type.name}</strong>
                  <span>
                    {item.start_date} → {item.end_date}
                  </span>
                </div>
                <p>Requested by {item.requester?.email || "—"}</p>
                <small>
                  {item.requested_days} days • {item.reason}
                </small>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
};

export default DashboardPage;
