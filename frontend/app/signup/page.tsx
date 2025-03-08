"use client";
import { Button, Input, Spinner, useDisclosure } from "@heroui/react";
import { useState } from "react";
import Link from "next/link";

import AuthModal from "@/components/modal";
import ThemeModal from "@/components/theme-modal";
export default function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [body, setBody] = useState("");
  const [title, setTitle] = useState("");
  const [spinner, setSpinner] = useState(false);
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSpinner(true);
    if (password !== passwordConfirmation) {
      setSpinner(false);
      setTitle("Password Error");
      setBody("Passwords do not match.");
      onOpen();

      return;
    }

    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      setTitle("Register Error");
      setBody(error.message!);
      onOpen();
      setSpinner(false);
      return;
    } else {
      setSpinner(false);
      window.location.href = "/dashboard";
    }
  };

  return (
    <>
      <div className="flex items-center justify-center mx-auto pt-16">
        <div className="w-full max-w-md rounded-xl dark:bg-background shadow-md ring-1 ring-black/5 dark:transform-gpu dark:[border:1px_solid_rgba(255,255,255,.1)] dark:[box-shadow:0_-20px_80px_-20px_#8686f01f_inset]">
          <form className="p-7 sm:p-11" onSubmit={handleSubmit}>
            <h1 className="mt-2 text-xl font-medium">Hello There!</h1>
            <p className="mt-2 text-medium dark:text-gray-300 text-gray-600">
              Sign up to play Spirit11.
            </p>
            <div className="mt-8 space-y-3">
              <Input
                required
                label="Username"
                name="username"
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
              <Input
                required
                label="Confirm Password"
                name="password"
                type="password"
                value={passwordConfirmation}
                onChange={(e) => setPasswordConfirmation(e.target.value)}
              />
            </div>
            <div className="mt-8">
              <Button className="w-full" disabled={spinner} type="submit">
                {spinner ? <Spinner size="sm" /> : <p>Sign Up</p>}
              </Button>
            </div>
            <div className="mt-8 text-center">
              <p className="text-sm dark:text-gray-300 text-gray-600">
                Already have an account?{" "}
                <Link href="/login">
                  <p className="text-sm text-blue-500 cursor-pointer">Login!</p>
                </Link>
              </p>
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
