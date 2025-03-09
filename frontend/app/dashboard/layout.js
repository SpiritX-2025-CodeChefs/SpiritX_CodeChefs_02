"use client";
import { useState, useEffect } from "react";

import Sidebar from "@/components/sidebar";

export default function Layout({ children }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    // Mark the component as hydrated
    setIsHydrated(true);

    // Update the initial state based on localStorage and screen width
    const sidebarState =
      window.localStorage.getItem("sidebarCollapsed") === "true";
    const shouldCollapse = sidebarState || window.innerWidth < 768;

    setIsCollapsed(shouldCollapse);
  }, []);

  useEffect(() => {
    // Update localStorage whenever isCollapsed changes
    if (isHydrated) {
      window.localStorage.setItem("sidebarCollapsed", isCollapsed.toString());
    }
  }, [isCollapsed, isHydrated]);

  if (!isHydrated) {
    // Prevent rendering until hydration is complete
    return null;
  }

  return (
    <div className="flex h-full">
      <Sidebar
        isCollapsed={isCollapsed}
        setIsCollapsed={setIsCollapsed}
      />
      <main className="flex-grow container mx-auto max-w-7xl px-6">
        {children}
      </main>
    </div>
  );
}
