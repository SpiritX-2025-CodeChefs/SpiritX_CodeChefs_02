import type { NextRequest } from "next/server";

import { NextResponse } from "next/server";
import { upfetch } from "./upfetch";
import { z } from "zod";

export async function makeAuthRequest(
  request: NextRequest,
) {
  try {
    const response = await upfetch(`${request.nextUrl.origin}/api/auth/validate-session`, {
      method: "POST",
      headers: {
        cookie: request.headers.get("cookie") || "",
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      schema: z.object({
        success: z.boolean(),
        role: z.string().optional().nullable(),
      })
    });

    return response
  } catch {
    return null;
  }
}

export async function handleDashboardRoute(
  request: NextRequest,
): Promise<NextResponse | null> {
  const session = (await makeAuthRequest(request))?.success;

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (
    request.nextUrl.pathname === "/dashboard/invite" &&
    process.env.INVITE_SIGNUP
  ) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export async function handleLoginRoute(
  request: NextRequest,
): Promise<NextResponse | null> {
  const session = (await makeAuthRequest(request))?.success;

  if (session) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export function handleAdminRoute(request: NextRequest): NextResponse {
  return NextResponse.redirect(new URL("/login", request.url));
}

export async function handleSignupRoute(
  request: NextRequest,
): Promise<NextResponse | null> {
  const token = new URL(request.nextUrl.href).searchParams.get("token");

  if (!token || process.env.INVITE_SIGNUP !== "true") {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  const verifyToken = await fetch(
    `${request.nextUrl.origin}/api/invites/verify`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    },
  );

  if (!verifyToken.ok) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  const expires = new Date();

  expires.setHours(expires.getHours() + 24);

  const response = NextResponse.next();

  response.cookies.set("onboarding_tok", token, {
    expires,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    path: "/",
  });

  return response;
}

export async function handleOnboardingRoute(
  request: NextRequest,
): Promise<NextResponse | null> {
  const session = (await makeAuthRequest(request))?.success;
  const onboardingToken = request.cookies.get("onboarding_tok");

  if (!session || !onboardingToken) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export async function handleRegisterSuccessRoute(
  request: NextRequest,
): Promise<NextResponse | null> {
  const token = request.nextUrl.pathname.split("/").pop();

  if (!token) return NextResponse.redirect(new URL("/", request.url));

  const response = await fetch(
    `${request.nextUrl.origin}/api/member/register/success`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    },
  );

  if (!response.ok) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}
