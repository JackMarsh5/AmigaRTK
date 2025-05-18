import React, { useEffect, useState } from "react";

export function App() {
  const [pose, setPose] = useState<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8042/subscribe/track_follower/pose_local");
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.pose) {
        setPose({ x: msg.pose.x, y: msg.pose.y });
      }
    };
    return () => ws.close();
  }, []);

  return (
    <div className="p-4 text-xl font-mono">
      <h1 className="text-2xl font-bold mb-4">RTK Local Position</h1>
      {pose ? (
        <div>
          X: {(pose.x * 100).toFixed(1)} cm<br />
          Y: {(pose.y * 100).toFixed(1)} cm
        </div>
      ) : (
        <p>Waiting for data...</p>
      )}
    </div>
  );
}
