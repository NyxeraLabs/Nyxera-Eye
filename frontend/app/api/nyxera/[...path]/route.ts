/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NYXERA_BACKEND_URL || "http://127.0.0.1:18080";

async function proxy(request: NextRequest, path: string[]): Promise<NextResponse> {
  const target = new URL(`${BACKEND_URL}/${path.join("/")}`);
  const source = new URL(request.url);
  source.searchParams.forEach((value, key) => {
    target.searchParams.set(key, value);
  });

  const outgoingHeaders = new Headers();
  const incomingType = request.headers.get("content-type");
  if (incomingType) {
    outgoingHeaders.set("Content-Type", incomingType);
  }
  const incomingToken = request.headers.get("x-api-token");
  if (incomingToken) {
    outgoingHeaders.set("X-API-Token", incomingToken);
  } else if (process.env.NEXT_PUBLIC_NYXERA_API_TOKEN) {
    outgoingHeaders.set("X-API-Token", process.env.NEXT_PUBLIC_NYXERA_API_TOKEN);
  }

  const response = await fetch(target, {
    method: request.method,
    headers: outgoingHeaders,
    body: request.method === "GET" || request.method === "HEAD" ? undefined : await request.text(),
    cache: "no-store",
  });

  return new NextResponse(await response.text(), {
    status: response.status,
    headers: { "Content-Type": response.headers.get("content-type") || "application/json" },
  });
}

export async function GET(request: NextRequest, context: { params: { path: string[] } }) {
  return proxy(request, context.params.path);
}

export async function POST(request: NextRequest, context: { params: { path: string[] } }) {
  return proxy(request, context.params.path);
}

export async function PUT(request: NextRequest, context: { params: { path: string[] } }) {
  return proxy(request, context.params.path);
}

export async function PATCH(request: NextRequest, context: { params: { path: string[] } }) {
  return proxy(request, context.params.path);
}

export async function DELETE(request: NextRequest, context: { params: { path: string[] } }) {
  return proxy(request, context.params.path);
}
