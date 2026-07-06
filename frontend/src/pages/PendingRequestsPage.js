import { useEffect, useState } from "react";
import { fetchPendingRequests, updateRequestStatus } from "../services/api";

const PendingRequestsPage = () => {
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState(null);

  const loadRequests = () => {
    fetchPendingRequests()
      .then((response) => setRequests(response.data))
      .catch((err) => setMessage({ type: "error", message: err.message }));
  };

  useEffect(() => {
    loadRequests();
  }, []);

  const handleDecision = async (requestId, decision) => {
    const manager_comment = window.prompt("Leave a note (optional)");
    try {
      await updateRequestStatus(requestId, { status: decision, manager_comment });
      setMessage({ type: "success", message: `Request ${decision}` });
      loadRequests();
    } catch (err) {
      setMessage({ type: "error", message: err.response?.data?.detail || "Unable to update" });
    }
  };

  return (
    <div className="page">
      <h2>Pending approvals</h2>
      {message && <p className={message.type}>{message.message}</p>}
      <ul className="list">
        {requests.map((request) => (
          <li key={request.id}>
            <div>
              <strong>{request.leave_type.name}</strong>
              <span>
                {request.start_date} → {request.end_date}
              </span>
            </div>
            <p>Requested by {request.requester?.email || "—"}</p>
            <small>{request.reason}</small>
            <div className="actions">
              <button type="button" onClick={() => handleDecision(request.id, "approved")}>
                Approve
              </button>
              <button type="button" onClick={() => handleDecision(request.id, "rejected")}>
                Reject
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PendingRequestsPage;
