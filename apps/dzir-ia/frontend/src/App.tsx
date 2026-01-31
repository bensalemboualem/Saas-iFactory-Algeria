import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import {
  Home,
  Onboarding,
  Landing,
  Chat,
  Collections,
  CollectionDetail,
  Sources,
  Timeline,
  Search,
} from "./pages";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route element={<Home />} path="/" />
          <Route element={<Landing />} path="/landing" />
          <Route element={<Onboarding />} path="/onboarding" />
          <Route element={<Chat />} path="/ask" />
          <Route element={<Sources />} path="/sources" />
          <Route element={<Collections />} path="/collections" />
          <Route element={<CollectionDetail />} path="/collections/:id" />
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
