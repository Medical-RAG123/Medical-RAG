import React, { useEffect, useState } from "react";

export default function App() {
  const [overview, setOverview] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/admin/overview")
      .then((res) => res.json())
      .then((data) => {
        setOverview(data);
        setLoading(false);
      })
      .catch((err) => console.error("Error fetching analytics:", err));
  }, []);

  if (loading) return <div style={{ padding: 20 }}>Loading Admin Dashboard...</div>;

  return (
    <div style={{ padding: 30, fontFamily: "sans-serif" }}>
      <h1>Phase 21: Admin Analytics & Observability Dashboard</h1>
      <div style={{ display: "flex", gap: 20, marginTop: 20 }}>
        <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8 }}>
          <h3>Document Stats</h3>
          <p>Total Documents: {overview?.documents?.total ?? 0}</p>
          <p>Indexed: {overview?.documents?.indexed ?? 0}</p>
          <p>Chunks: {overview?.documents?.total_chunks ?? 0}</p>
        </div>
        <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8 }}>
          <h3>Evaluation Status</h3>
          <p>Latest Status: {overview?.retrieval?.status ?? "N/A"}</p>
          <p>Recall @ 5: {overview?.retrieval?.recall_at_5 ?? "N/A"}</p>
        </div>
      </div>
    </div>
  );
}