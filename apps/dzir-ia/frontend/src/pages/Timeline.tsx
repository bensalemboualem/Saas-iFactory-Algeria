import { useTimelineStore } from "../store";
import "./Timeline.css";

const EVENT_ICONS: Record<string, string> = {
  capture: "📥",
  search: "🔍",
  ask: "💬",
  sync: "🔄",
};

export default function Timeline() {
  const { events, clearEvents } = useTimelineStore();

  return (
    <div className="timeline-page">
      <header className="page-header">
        <h1>Timeline</h1>
        {events.length > 0 && (
          <button className="btn-ghost" onClick={clearEvents}>
            Clear History
          </button>
        )}
      </header>

      {events.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📍</div>
          <h2>No activity yet</h2>
          <p>Your interactions with Dzir IA will appear here.</p>
        </div>
      ) : (
        <div className="timeline">
          {events.map((event, index) => (
            <div key={event.id} className="timeline-item">
              <div className="timeline-marker">
                <span className="marker-icon">{EVENT_ICONS[event.type] || "📌"}</span>
                {index < events.length - 1 && <div className="marker-line" />}
              </div>
              <div className="timeline-content">
                <div className="event-header">
                  <span className="event-type">{event.type}</span>
                  <time className="event-time">
                    {new Date(event.timestamp).toLocaleString()}
                  </time>
                </div>
                <h3 className="event-title">{event.title}</h3>
                {event.description && (
                  <p className="event-description">{event.description}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
