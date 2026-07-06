import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";
const client = axios.create({ baseURL: BASE_URL });

export const setAuthHeader = (token) => {
  if (token) {
    client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete client.defaults.headers.common["Authorization"];
  }
};

export const registerUser = (data) => client.post("/auth/register", data);
export const loginUser = (data) => client.post("/auth/login", data);
export const fetchProfile = () => client.get("/users/me");

export const fetchLeaveTypes = () => client.get("/leave-types/");
export const createLeaveType = (payload) => client.post("/leave-types/", payload);
export const updateLeaveType = (id, payload) => client.put(`/leave-types/${id}`, payload);
export const deleteLeaveType = (id) => client.delete(`/leave-types/${id}`);

export const fetchEntitlements = () => client.get("/entitlements/");
export const fetchLeaveRequests = (params) => client.get("/leave-requests/", { params });
export const submitLeaveRequest = (payload) => client.post("/leave-requests/", payload);
export const fetchPendingRequests = () => client.get("/leave-requests/pending");
export const updateRequestStatus = (id, payload) => client.patch(`/leave-requests/${id}/status`, payload);
