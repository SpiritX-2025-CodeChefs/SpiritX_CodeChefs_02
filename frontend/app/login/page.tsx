"use client";

import { Button, Input, Link, Spinner, useDisclosure } from "@heroui/react";
import { useState } from "react";

import AuthModal from "@/components/modal";
import ThemeModal from "@/components/theme-modal";
import { upfetch } from "@/lib/utils";
import { z } from "zod";

export default function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [body, setBody] = useState("");
  const [title, setTitle] = useState("");
  const [spinner, setSpinner] = useState(false);
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSpinner(true);

    const response = await upfetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
      schema: z.object({
        success: z.boolean(),
        role: z.string().optional().nullable(),
        detail: z.string().optional().nullable(),
      }),
    });

    if (!response.success) {
      setBody("An error occurred. Please try again later.");
      setTitle("Error");
      onOpen();
      setSpinner(false);
      return;
    }

    if (response.success) {
      window.location.href = `${window.location.origin}/dashboard`;
    } else {
      setBody(response.detail || "An error occurred. Please try again later.");
      setTitle("Login Error");
      onOpen();
    }

    setSpinner(false);
  };

  return (
    <>
      <div className="flex items-center justify-center mx-auto pt-16">
        <div className="w-full max-w-md rounded-xl dark:bg-background shadow-md ring-1 ring-black/5 dark:transform-gpu dark:[border:1px_solid_rgba(255,255,255,.1)] dark:[box-shadow:0_-20px_80px_-20px_#8686f01f_inset]">
          <form className="p-7 sm:p-11" onSubmit={handleSubmit}>
            <h1 className="mt-2 text-xl font-medium">Welcome back!</h1>
            <p className="mt-2 text-medium dark:text-gray-300 text-gray-600">
              Sign in to your account to continue.
            </p>
            <div className="mt-8 space-y-3">
              <Input
                required
                label="Username"
                name="username"
                type="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <Input
                required
                label="Password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="mt-8">
              <Button className="w-full" disabled={spinner} type="submit">
                {spinner ? <Spinner size="sm" /> : <p>Login</p>}
              </Button>
            </div>
            <div className="mt-8 text-center">
              <div className="text-sm dark:text-gray-300 text-gray-600">
                Don't have an account?{" "}
                <Link href="/signup">
                  <p className="text-sm text-blue-500 cursor-pointer">Sign up!</p>
                </Link>
              </div>
            </div>
          </form>
          <AuthModal
            body={body}
            isOpen={isOpen}
            title={title}
            onOpenChange={onOpenChange}
          />
        </div>
      </div>
      <ThemeModal />
    </>
  );
}
