'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    dateOfBirth: '',
    gender: '',
    terms: false,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const target = e.target as HTMLInputElement;
      setFormData((prev) => ({
        ...prev,
        [name]: target.checked,
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    // Mock registration logic
    setTimeout(() => {
      setIsLoading(false);
      console.log('Registration attempt:', formData);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      {/* Logo and tagline */}
      <div className="space-y-3 text-center">
        <div className="flex justify-center">
          <div className="w-14 h-14 rounded-lg bg-emerald-600 flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-xl">PLT</span>
          </div>
        </div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Join PLT
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Your Personal Longevity Team
        </p>
      </div>

      {/* Register card */}
      <div className="bg-white dark:bg-gray-950 rounded-xl shadow-lg p-8 space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Create Account
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Get started with your personalized longevity profile
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name field */}
          <div className="space-y-2">
            <Label htmlFor="name" className="text-gray-700 dark:text-gray-300">
              Full Name
            </Label>
            <Input
              id="name"
              type="text"
              placeholder="John Doe"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Email field */}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-gray-700 dark:text-gray-300">
              Email Address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Date of Birth field */}
          <div className="space-y-2">
            <Label htmlFor="dateOfBirth" className="text-gray-700 dark:text-gray-300">
              Date of Birth
            </Label>
            <Input
              id="dateOfBirth"
              type="date"
              name="dateOfBirth"
              value={formData.dateOfBirth}
              onChange={handleChange}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Gender field */}
          <div className="space-y-2">
            <Label htmlFor="gender" className="text-gray-700 dark:text-gray-300">
              Gender
            </Label>
            <select
              id="gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Password field */}
          <div className="space-y-2">
            <Label htmlFor="password" className="text-gray-700 dark:text-gray-300">
              Password
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Confirm password field */}
          <div className="space-y-2">
            <Label
              htmlFor="confirmPassword"
              className="text-gray-700 dark:text-gray-300"
            >
              Confirm Password
            </Label>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800"
            />
          </div>

          {/* Terms checkbox */}
          <div className="flex items-start gap-2">
            <Checkbox
              id="terms"
              name="terms"
              checked={formData.terms}
              onCheckedChange={(checked) =>
                setFormData((prev) => ({
                  ...prev,
                  terms: checked as boolean,
                }))
              }
              className="mt-1"
            />
            <label htmlFor="terms" className="text-xs text-gray-600 dark:text-gray-400">
              I agree to the{' '}
              <Link href="/terms" className="text-emerald-600 hover:underline">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="text-emerald-600 hover:underline">
                Privacy Policy
              </Link>
            </label>
          </div>

          {/* Create account button */}
          <Button
            type="submit"
            disabled={isLoading || !formData.terms}
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2"
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </Button>
        </form>
      </div>

      {/* Login link */}
      <div className="text-center">
        <p className="text-gray-600 dark:text-gray-400">
          Already have an account?{' '}
          <Link
            href="/login"
            className="text-emerald-600 hover:text-emerald-700 dark:hover:text-emerald-400 font-semibold"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
