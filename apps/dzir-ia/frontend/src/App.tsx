import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import { Chat, Collections, Timeline, Search } from "./pages";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route element={<Chat />} path="/" />
          <Route element={<Chat />} path="/chat" />
          <Route element={<Collections />} path="/collections" />
          <Route element={<Timeline />} path="/timeline" />
          <Route element={<Search />} path="/search" />
          <Route
            element={
              <div style={{ padding: 24 }}>
                <h1>Graph View</h1>
                <p>Coming soon...</p>
              </div>
            }
            path="/graph"
          />
          <Route
            element={
              <div style={{ padding: 24 }}>
                <h1>404</h1>
                <p>Page not found</p>
              </div>
            }
            path="*"
          />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
