import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./styles/globals.css";
import Layout from "./components/Layout";
import DzirIAChat from "./components/dziria/DzirIAChat";
import { I18nProvider, useI18n } from "./lib/i18n";
import { ThemeProvider } from "./lib/theme";

function NotFound() {
  const { t } = useI18n();
  return (
    <div style={{ color: "var(--text-primary)", padding: 20 }}>
      <h1>404</h1>
      <p>{t('error.not_found')}</p>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <I18nProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route element={<DzirIAChat />} path="/" />
              <Route element={<DzirIAChat />} path="/chat" />
              <Route element={<NotFound />} path="*" />
            </Routes>
          </Layout>
        </BrowserRouter>
      </I18nProvider>
    </ThemeProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);