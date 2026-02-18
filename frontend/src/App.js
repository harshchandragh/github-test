import { useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Dashboard from "@/components/Dashboard";
import UploadData from "@/components/UploadData";
import SprintAnalysis from "@/components/SprintAnalysis";
import JiraConnect from "@/components/JiraConnect";
import { LayoutDashboard, Upload, BarChart3, Link2 } from "lucide-react";

const Sidebar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: "/", icon: LayoutDashboard, label: "Dashboard" },
    { path: "/upload", icon: Upload, label: "Upload Data" },
    { path: "/sprints", icon: BarChart3, label: "Sprint Analysis" },
  ];
  
  return (
    <div className="w-64 bg-background border-r border-border h-screen sticky top-0" data-testid="sidebar">
      <div className="p-6 border-b border-border">
        <h1 className="text-xl font-semibold text-primary flex items-center gap-2" data-testid="app-title">
          <BarChart3 className="w-6 h-6" />
          Jira Velocity Pro
        </h1>
        <p className="text-xs text-muted-foreground mt-1">Sprint Analytics & Predictions</p>
      </div>
      
      <nav className="p-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
              className={`flex items-center gap-3 px-4 py-2 rounded-sm mb-1 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-accent text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              }`}
            >
              <Icon className="w-4 h-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <div className="flex">
          <Sidebar />
          <div className="flex-1 min-h-screen bg-secondary">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<UploadData />} />
              <Route path="/sprints" element={<SprintAnalysis />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;