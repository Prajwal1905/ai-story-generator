import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const GENRES = ["drama", "comedy", "thriller", "romance", "horror"];

export default function App() {
  const [topic, setTopic] = useState("");
  const [genre, setGenre] = useState("drama");
  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState(null);
  const [error, setError] = useState(null);
  const [stories, setStories] = useState([]);
  const [activeTab, setActiveTab] = useState("generate");

  const generateStory = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError(null);
    setStory(null);
    try {
      const res = await axios.post(`${API_URL}/generate-story`, {
        topic,
        genre,
      });
      setStory(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const fetchStories = async () => {
    try {
      const res = await axios.get(`${API_URL}/stories`);
      setStories(res.data);
      setActiveTab("history");
    } catch (err) {
      setError("Failed to fetch stories");
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.logo}>🎭 AI Story Generator</h1>
        <p style={styles.subtitle}>Powered by LangGraph + RAG + OpenAI</p>
      </div>

      {/* Tabs */}
      <div style={styles.tabs}>
        <button
          style={{
            ...styles.tab,
            ...(activeTab === "generate" ? styles.activeTab : {}),
          }}
          onClick={() => setActiveTab("generate")}
        >
          Generate
        </button>
        <button
          style={{
            ...styles.tab,
            ...(activeTab === "history" ? styles.activeTab : {}),
          }}
          onClick={fetchStories}
        >
          History
        </button>
      </div>

      {/* Generate Tab */}
      {activeTab === "generate" && (
        <div style={styles.card}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Topic</label>
            <input
              style={styles.input}
              placeholder="e.g. heartbreak, ambition, friendship..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && generateStory()}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>Genre</label>
            <div style={styles.genreRow}>
              {GENRES.map((g) => (
                <button
                  key={g}
                  style={{
                    ...styles.genreBtn,
                    ...(genre === g ? styles.activeGenre : {}),
                  }}
                  onClick={() => setGenre(g)}
                >
                  {g}
                </button>
              ))}
            </div>
          </div>

          <button
            style={{
              ...styles.generateBtn,
              ...(loading ? styles.disabledBtn : {}),
            }}
            onClick={generateStory}
            disabled={loading}
          >
            {loading ? "✍️ Writing your story..." : "🎬 Generate Story"}
          </button>

          {loading && (
            <div style={styles.loadingBox}>
              <p style={styles.loadingText}>🔍 Researching topic...</p>
              <p style={styles.loadingText}>📚 Retrieving similar stories...</p>
              <p style={styles.loadingText}>✍️ Generating microdrama...</p>
              <p style={styles.loadingText}>🔄 Reflecting and improving...</p>
            </div>
          )}

          {error && <div style={styles.errorBox}>{error}</div>}

          {story && (
            <div style={styles.storyBox}>
              <div style={styles.storyMeta}>
                <span style={styles.badge}>{story.genre}</span>
                <span style={styles.storyTopic}>#{story.topic}</span>
                <span style={styles.storyDate}>
                  {new Date(story.created_at).toLocaleString()}
                </span>
              </div>
              <pre style={styles.script}>{story.script}</pre>
            </div>
          )}
        </div>
      )}

      {/* History Tab */}
      {activeTab === "history" && (
        <div style={styles.card}>
          <h2 style={styles.sectionTitle}>Generated Stories</h2>
          {stories.length === 0 ? (
            <p style={styles.emptyText}>No stories yet. Generate one!</p>
          ) : (
            stories.map((s) => (
              <div key={s.id} style={styles.historyItem}>
                <div style={styles.storyMeta}>
                  <span style={styles.badge}>{s.genre}</span>
                  <span style={styles.storyTopic}>#{s.topic}</span>
                  <span style={styles.storyDate}>
                    {new Date(s.created_at).toLocaleString()}
                  </span>
                </div>
                <pre style={styles.scriptSmall}>{s.script}</pre>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "24px 16px",
  },
  header: {
    textAlign: "center",
    marginBottom: "32px",
  },
  logo: {
    fontSize: "2rem",
    fontWeight: "700",
    background: "linear-gradient(90deg, #a78bfa, #60a5fa)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  subtitle: {
    color: "#888",
    marginTop: "8px",
    fontSize: "0.9rem",
  },
  tabs: {
    display: "flex",
    gap: "8px",
    marginBottom: "24px",
  },
  tab: {
    padding: "10px 24px",
    borderRadius: "8px",
    border: "1px solid #333",
    background: "transparent",
    color: "#888",
    cursor: "pointer",
    fontSize: "0.95rem",
  },
  activeTab: {
    background: "#1e1e2e",
    color: "#a78bfa",
    borderColor: "#a78bfa",
  },
  card: {
    background: "#1a1a2e",
    borderRadius: "16px",
    padding: "24px",
    border: "1px solid #2a2a3e",
  },
  inputGroup: {
    marginBottom: "20px",
  },
  label: {
    display: "block",
    marginBottom: "8px",
    color: "#aaa",
    fontSize: "0.9rem",
  },
  input: {
    width: "100%",
    padding: "12px 16px",
    borderRadius: "10px",
    border: "1px solid #333",
    background: "#0f0f1a",
    color: "#fff",
    fontSize: "1rem",
    outline: "none",
  },
  genreRow: {
    display: "flex",
    gap: "8px",
    flexWrap: "wrap",
  },
  genreBtn: {
    padding: "8px 16px",
    borderRadius: "20px",
    border: "1px solid #333",
    background: "transparent",
    color: "#888",
    cursor: "pointer",
    fontSize: "0.85rem",
    textTransform: "capitalize",
  },
  activeGenre: {
    background: "#2d1b69",
    color: "#a78bfa",
    borderColor: "#a78bfa",
  },
  generateBtn: {
    width: "100%",
    padding: "14px",
    borderRadius: "10px",
    border: "none",
    background: "linear-gradient(90deg, #7c3aed, #2563eb)",
    color: "#fff",
    fontSize: "1rem",
    fontWeight: "600",
    cursor: "pointer",
    marginBottom: "20px",
  },
  disabledBtn: {
    opacity: "0.6",
    cursor: "not-allowed",
  },
  loadingBox: {
    background: "#0f0f1a",
    borderRadius: "10px",
    padding: "16px",
    marginBottom: "20px",
  },
  loadingText: {
    color: "#888",
    fontSize: "0.85rem",
    marginBottom: "6px",
  },
  errorBox: {
    background: "#2a0a0a",
    border: "1px solid #ff4444",
    borderRadius: "10px",
    padding: "16px",
    color: "#ff6666",
    marginBottom: "20px",
  },
  storyBox: {
    background: "#0f0f1a",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #2a2a3e",
  },
  storyMeta: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "16px",
    flexWrap: "wrap",
  },
  badge: {
    background: "#2d1b69",
    color: "#a78bfa",
    padding: "4px 12px",
    borderRadius: "20px",
    fontSize: "0.8rem",
    textTransform: "capitalize",
  },
  storyTopic: {
    color: "#60a5fa",
    fontSize: "0.9rem",
  },
  storyDate: {
    color: "#555",
    fontSize: "0.8rem",
    marginLeft: "auto",
  },
  script: {
    color: "#e2e8f0",
    fontFamily: "'Segoe UI', sans-serif",
    fontSize: "0.95rem",
    lineHeight: "1.8",
    whiteSpace: "pre-wrap",
  },
  sectionTitle: {
    fontSize: "1.2rem",
    marginBottom: "20px",
    color: "#a78bfa",
  },
  emptyText: {
    color: "#555",
    textAlign: "center",
    padding: "40px",
  },
  historyItem: {
    background: "#0f0f1a",
    borderRadius: "12px",
    padding: "16px",
    marginBottom: "16px",
    border: "1px solid #2a2a3e",
  },
  scriptSmall: {
    color: "#aaa",
    fontFamily: "'Segoe UI', sans-serif",
    fontSize: "0.85rem",
    lineHeight: "1.6",
    whiteSpace: "pre-wrap",
    maxHeight: "150px",
    overflow: "hidden",
  },
};
