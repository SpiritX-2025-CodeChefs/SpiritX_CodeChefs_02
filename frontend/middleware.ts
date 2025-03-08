import type { NextRequest } from "next/server";

import { NextResponse } from "next/server";

import {
  handleDashboardRoute,
  handleLoginRoute,
  handleAdminRoute,
  handleSignupRoute,
  handleOnboardingRoute,
  handleRegisterSuccessRoute,
} from "@/lib/utils";

export async function middleware(request: NextRequest) {
  try {
    if (request.nextUrl.pathname.startsWith("/dashboard")) {
      return (await handleDashboardRoute(request)) || NextResponse.next();
    }

    if (request.nextUrl.pathname === "/login") {
      return (await handleLoginRoute(request)) || NextResponse.next();
    }

    if (request.nextUrl.pathname === "") {
      return handleAdminRoute(request);
    }

    if (request.nextUrl.pathname.startsWith("/admin/signup")) {
      return (await handleSignupRoute(request)) || NextResponse.next();
    }

    if (request.nextUrl.pathname.startsWith("/admin/onboarding")) {
      return (await handleOnboardingRoute(request)) || NextResponse.next();
    }

    if (request.nextUrl.pathname.startsWith("/member/registration/success")) {
      return (await handleRegisterSuccessRoute(request)) || NextResponse.next();
    }

    return NextResponse.next();
  } catch {
    return NextResponse.redirect(new URL("/", request.url));
  }
}

export const config = {
  matcher: [
    {
      source: "/((?!api|_next/static|_next/image|favicon.ico).*)",
      missing: [
        { type: "header", key: "next-router-prefetch" },
        { type: "header", key: "purpose", value: "prefetch" },
      ],
    },
  ],
};
