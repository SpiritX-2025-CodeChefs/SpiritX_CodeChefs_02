import React from "react";

import { ThemeSwitch } from "./theme-switch";

export default function ThemeModal() {
  return (
    <div className="fixed bottom-5 right-5 z-50">
      <div className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-900 flex items-center justify-center shadow-lg">
        <ThemeSwitch />
      </div>
    </div>
  );
}
