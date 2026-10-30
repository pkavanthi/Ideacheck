import { FormEvent, useEffect, useState } from "react";
import { api, configureApi } from "./api";
import IncidentsPage from "./components/IncidentsPage";
import ResourcesPage from "./components/ResourcesPage";

const STORAGE_KEY = "resilience_api_key";
type Tab = "incidents" | "resources";

export default function App() {
  const [key, setKey] = useState<string>(() => sessionStorage.getItem(STORAGE_KEY) ?? "");
  const [tab, setTab] = useState<Tab>("incidents");
  const [loginError, setLoginError] = useState("");
  const [busy, setBusy] = useState(false);
  const [authed, setAuthed] = useState(false);

  const logout = (message = "") => {
    sessionStorage.removeItem(STORAGE_KEY);
    setAuthed(false);
    setKey("");
    setLoginError(message);
  };

  const login = async (candidate: string) => {
    setBusy(true);
    setLoginError("");
    configureApi(candidate, () => logout("Session expired or API key invalid"));
    try {
      await api.listIncidents({ limit: 1 });
      sessionStorage.setItem(STORAGE_KEY, candidate);
      setKey(candidate);
      setAuthed(true);
    } catch (e) {
      if (!(e instanceof Error) || e.message !== "Invalid or missing API key") {
        setLoginError(e instanceof Error ? e.message : "Login failed");
      }
    } finally {
      setBusy(false);
    }
  };

  // Restore a session-stored key on first load.
  useEffect(() => {
    if (key) void login(key);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const value = String(new FormData(e.currentTarget).get("key") ?? "").trim();
    if (value) void login(value);
  };

  if (!authed) {
    return (
      <div className="login-wrap">
        <form className="card login" onSubmit={onSubmit}>
          <h1>National Resilience Intelligence Backbone</h1>
          <p className="muted">Enter your API key to continue.</p>
          <input name="key" type="password" placeholder="X-API-Key" autoFocus autoComplete="off" />
          {loginError && <div className="error" role="alert">{loginError}</div>}
          <button className="btn primary" disabled={busy}>{busy ? "Checking…" : "Sign in"}</button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1>Resilience Command</h1>
        <nav>
          <button className={tab === "incidents" ? "tab active" : "tab"} onClick={() => setTab("incidents")}>
            Incidents
          </button>
          <button className={tab === "resources" ? "tab active" : "tab"} onClick={() => setTab("resources")}>
            Resources
          </button>
        </nav>
        <button className="btn" onClick={() => logout()}>Sign out</button>
      </header>
      <main>{tab === "incidents" ? <IncidentsPage /> : <ResourcesPage />}</main>
    </div>
  );
}
