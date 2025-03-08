"use client";

import React from "react";
import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-900 to-indigo-900 text-white">
      {/* Hero Section */}
      <header className="container mx-auto pt-24 pb-16 px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="md:w-1/2">
            <h1 className="text-5xl md:text-6xl font-bold mb-4">
              <span className="text-yellow-400">Spirit11</span> Fantasy Cricket League
            </h1>
            <p className="text-xl mb-8">
              Build your dream team. Compete with friends. Win big with your cricket knowledge!
            </p>
            <button className="bg-yellow-400 text-blue-900 font-bold py-3 px-8 rounded-lg text-lg hover:bg-yellow-300 transition duration-300" onClick={() => window.location.href = "/signup"}>
              Join Now
            </button>
          </div>
          <div className="md:w-1/2">
            <div className="relative h-72 md:h-96 w-full rounded-lg overflow-hidden shadow-2xl">
              <Image
                src="/cricket-stadium.jpg"
                alt="Cricket Stadium"
                layout="fill"
                objectFit="cover"
                className="rounded-lg"
                priority
              />
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section className="bg-blue-800 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Why Choose <span className="text-yellow-400">Spirit11</span>?</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-blue-700 p-8 rounded-lg shadow-lg">
              <div className="text-yellow-400 text-4xl mb-4">🏆</div>
              <h3 className="text-xl font-bold mb-4">Exciting Prizes</h3>
              <p>Compete for incredible rewards in daily contests and seasonal championships.</p>
            </div>

            <div className="bg-blue-700 p-8 rounded-lg shadow-lg">
              <div className="text-yellow-400 text-4xl mb-4">🔄</div>
              <h3 className="text-xl font-bold mb-4">Real-Time Updates</h3>
              <p>Watch your team score points as matches progress with our lightning-fast scoring system.</p>
            </div>

            <div className="bg-blue-700 p-8 rounded-lg shadow-lg">
              <div className="text-yellow-400 text-4xl mb-4">👥</div>
              <h3 className="text-xl font-bold mb-4">Private Leagues</h3>
              <p>Create exclusive competitions with friends, family, or colleagues.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">What Our Users Say</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-indigo-800 p-6 rounded-lg">
              <p className="italic mb-4">"Spirit11 completely changed how I enjoy cricket. The thrill of seeing my players perform is unmatched!"</p>
              <p className="font-bold">- John D.</p>
            </div>

            <div className="bg-indigo-800 p-6 rounded-lg">
              <p className="italic mb-4">"I've tried other fantasy platforms but Spirit11's interface and community keep me coming back every season."</p>
              <p className="font-bold">- Jane D.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-yellow-400 to-yellow-500 text-blue-900 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Play?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">Join thousands of cricket enthusiasts and put your knowledge to the test today.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-900 text-white font-bold py-3 px-8 rounded-lg text-lg hover:bg-blue-800 transition duration-300" onClick={() => window.location.href = "/signup"}>
              Sign Up
            </button>
            <button className="bg-transparent border-2 border-blue-900 font-bold py-3 px-8 rounded-lg text-lg hover:bg-blue-900 hover:text-white transition duration-300" onClick={() => window.location.href = "/login"}>
              Login
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-blue-950 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h3 className="text-2xl font-bold mb-2">
                <span className="text-yellow-400">Spirit11</span>
              </h3>
              <p className="text-blue-300">Fantasy Cricket at its best</p>
            </div>
            <div className="flex gap-6">
              <a href="#" className="text-blue-300 hover:text-yellow-400">About</a>
              <a href="#" className="text-blue-300 hover:text-yellow-400">Privacy</a>
              <a href="#" className="text-blue-300 hover:text-yellow-400">Terms</a>
              <a href="#" className="text-blue-300 hover:text-yellow-400">Contact</a>
            </div>
          </div>
          <div className="text-center mt-8 text-blue-400 text-sm">
            © 2025 CodeChefs. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
