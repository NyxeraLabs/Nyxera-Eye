/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import { createContext, useContext, useMemo, useState } from "react";
import type { Finding } from "../lib/types";

type FindingContextValue = {
  selected: Finding | null;
  setSelected: (finding: Finding | null) => void;
};

const FindingContext = createContext<FindingContextValue | undefined>(undefined);

export function FindingProvider({ children }: { children: React.ReactNode }) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const value = useMemo(() => ({ selected, setSelected }), [selected]);
  return <FindingContext.Provider value={value}>{children}</FindingContext.Provider>;
}

export function useFinding() {
  const context = useContext(FindingContext);
  if (!context) {
    throw new Error("useFinding must be used within FindingProvider");
  }
  return context;
}
