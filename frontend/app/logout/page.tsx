"use client";

import React, { useEffect } from "react";
import { Card, CardBody, Spinner } from "@heroui/react";

import ThemeModal from "@/components/theme-modal";
import { toast } from "sonner";

export default function LogoutPage() {
  useEffect(() => {
    const logout = async () => {
      const response = await fetch("/api/auth/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const data = await response.json();
        toast.error(data.message);
      }

      const timer = setTimeout(() => {
        window.location.href = "/login";
      }, 3000);

      return () => clearTimeout(timer);
    };

    logout();
  }, []);

  return (
    <>
      <div className="min-h-screen w-full flex items-center justify-center">
        <Card className="w-full max-w-md mx-4">
          <CardBody className="flex flex-col items-center gap-6 py-8">
            <h2 className="text-2xl font-bold">You have been logged out</h2>
            <p className="text-gray-600 text-center">
              You will be redirected to the login page shortly...
            </p>
            <Spinner color="primary" size="lg" />
          </CardBody>
        </Card>
      </div>
      <ThemeModal />
    </>
  );
}
