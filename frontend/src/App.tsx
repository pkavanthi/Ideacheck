import { FormEvent, useState } from "react";
import { api, clearApiKey, hasApiKey, setApiKey } from "./api";
import AssetsPage from "./AssetsPage";
import IncidentsPage from "./IncidentsPage";

function Login({ onLogin }: { onLogin: () => void }) {
  const [key, setKey] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    setApiKey(key.trim());
    try {
      await api.listIncidents({ limit: "1" });
      onLogin();
    } catch (err) {
      clearApiKey();
      setError((err as Error).message);
      setBusy(false);
    }
  }

  return (
    <div className="login">
      <form onSubmit={submit}>
        <h1>AegisFlow</h1>
        <p className="muted">Enter the API key configured on the backend.</p>
        <input type="password" placeholder="API key" value={key} onChange={(e) => setKey(e.target.value)} required autoFocus />
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={busy}>
          Sign in
        </button>
      </form>
    </div>
  );
}

export default function App() {
  const [authed, setAuthed] = useState(hasApiKey());
  const [tab, setTab] = useState<"incidents" | "assets">("incidents");

  if (!authed) return <Login onLogin={() => setAuthed(true)} />;

  return (
    <div className="app">
      <header>
        <h1>AegisFlow</h1>
        <nav>
          <button className={tab === "incidents" ? "tab active" : "tab"} onClick={() => setTab("incidents")}>
            Incidents
          </button>
          <button className={tab === "assets" ? "tab active" : "tab"} onClick={() => setTab("assets")}>
            Assets
          </button>
        </nav>
        <button
          className="secondary"
          onClick={() => {
            clearApiKey();
            setAuthed(false);
          }}
        >
          Sign out
        </button>
      </header>
      <main>{tab === "incidents" ? <IncidentsPage /> : <AssetsPage />}</main>
    </div>
  );
}
