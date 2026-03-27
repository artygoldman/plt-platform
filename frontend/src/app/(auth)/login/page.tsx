'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    // Mock login logic
    setTimeout(() => {
      setIsLoading(false);
      console.log('Login attempt:', { email, password });
    }, 1000);
  };

  return (
    <div className="space-y-8">
      {/* Logo and tagline */}
      <div className="space-y-3 text-center">
        <div className="flex justify-center">
          <div className="w-16 h-16 rounded-xl bg-emerald-600 flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-2xl">PLT</span>
          </div>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Personal Longevity Team
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Your Personal Longevity Team
        </p>
      </div>

      {/* Login card */}
      <div className="bg-white dark:bg-gray-950 rounded-xl shadow-lg p-8 space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Sign In
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Enter your email and password to access your longevity profile
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email field */}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-gray-700 dark:text-gray-300">
              Email Address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Password field */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label
                htmlFor="password"
                className="text-gray-700 dark:text-gray-300"
              >
                Password
              </Label>
              <Link
                href="/forgot-password"
                className="text-xs text-emerald-600 hover:text-emerald-700 dark:hover:text-emerald-400"
              >
                Forgot?
              </Link>
            </div>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Sign in button */}
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200 dark:border-gray-800" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="px-2 bg-white dark:bg-gray-950 text-gray-600 dark:text-gray-400">
              Or continue with
            </span>
          </div>
        </div>

        {/* Social buttons */}
        <div className="grid grid-cols-2 gap-3">
          <Button
            variant="outline"
            className="border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300"
          >
            Google
          </Button>
          <Button
            variant="outline"
            className="border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300"
          >
            Apple
          </Button>
        </div>
      </div>

      {/* Register link */}
      <div className="text-center">
        <p className="text-gray-600 dark:text-gray-400">
          Don't have an account?{' '}
          <Link
            href="/register"
            className="text-emerald-600 hover:text-emerald-700 dark:hover:text-emerald-400 font-semibold"
          >
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
