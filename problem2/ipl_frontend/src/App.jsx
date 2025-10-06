// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar.jsx';
import HomePage from './pages/Homepage.jsx';
import ExtraRunsPage from './pages/ExtraRunsPage.jsx';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/extra-runs" element={<ExtraRunsPage />} />
      </Routes>
    </Router>
  );
}

export default App;