"use client";

import { useEffect, useState } from "react";

import { fetchOpsFeed } from "./api";
import type { OpsFeed } from "./types";

export function useOpsFeed(pollMs: number = 15000) {
  const [feed, setFeed] = useState<OpsFeed | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const pull = async () => {
      const next = await fetchOpsFeed();
      if (mounted) {
        setFeed(next);
        setIsLoading(false);
      }
    };

    pull();
    const timer = setInterval(pull, pollMs);

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, [pollMs]);

  return { feed, isLoading };
}
