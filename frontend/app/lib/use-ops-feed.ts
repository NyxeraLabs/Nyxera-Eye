/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import { useEffect, useState } from "react";

import { fetchOpsFeed, performFindingAction, startScanLoop, stopScanLoop, triggerScan } from "./api";
import type { OpsFeed } from "./types";

export function useOpsFeed(pollMs: number = 5000) {
  const [feed, setFeed] = useState<OpsFeed | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    const next = await fetchOpsFeed();
    if (next) {
      setFeed(next);
      setError(null);
    } else {
      setError("Unable to reach backend ops feed. Start API service and ensure token/base URL are configured.");
    }
    setIsLoading(false);
  };

  useEffect(() => {
    let mounted = true;

    const pull = async () => {
      const next = await fetchOpsFeed();
      if (!mounted) {
        return;
      }
      if (next) {
        setFeed(next);
        setError(null);
      } else {
        setError("Unable to reach backend ops feed. Start API service and ensure token/base URL are configured.");
      }
      setIsLoading(false);
    };

    pull();
    const timer = setInterval(pull, pollMs);

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, [pollMs]);

  const runScan = async (batchSize: number = 96) => {
    const ok = await triggerScan(batchSize);
    await refresh();
    return ok;
  };

  const scanLoopStart = async (batchSize: number = 96, intervalSeconds: number = 10) => {
    const ok = await startScanLoop(batchSize, intervalSeconds);
    await refresh();
    return ok;
  };

  const scanLoopStop = async () => {
    const ok = await stopScanLoop();
    await refresh();
    return ok;
  };

  const findingAction = async (findingId: string, action: string) => {
    const ok = await performFindingAction(findingId, action);
    await refresh();
    return ok;
  };

  return { feed, isLoading, error, refresh, runScan, scanLoopStart, scanLoopStop, findingAction };
}
