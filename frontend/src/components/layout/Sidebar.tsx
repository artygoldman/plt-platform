'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Heart,
  Activity,
  ClipboardCheck,
  Bot,
  Upload,
  FileText,
  Pill,
  User,
  Menu,
  X,
  Moon,
  Sun,
} from 'lucide-react';
import { Button } from '@/components/ui/button';

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/dashboard', icon: <LayoutDashboard size={20} /> },
  { label: 'Digital Twin', href: '/digital-twin', icon: <Heart size={20} /> },
  { label: 'Biomarkers', href: '/biomarkers', icon: <Activity size={20} /> },
  { label: 'Daily Contract', href: '/daily-contract', icon: <ClipboardCheck size={20} /> },
  { label: 'Agents', href: '/agents', icon: <Bot size={20} /> },
  { label: 'Upload Data', href: '/upload', icon: <Upload size={20} /> },
  { label: 'Protocols', href: '/protocols', icon: <FileText size={20} /> },
  { label: 'Supplements', href: '/supplements', icon: <Pill size={20} /> },
  { label: 'Profile', href: '/profile', icon: <User size={20} /> },
];

export function Sidebar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);

  const isActive = (href: string) => {
    const basePath = href.split('/')[1];
    const currentPath = pathname.split('/')[1];
    return basePath === currentPath;
  };

  return (
    <>
      {/* Mobile hamburger button */}
      <div className="fixed top-4 left-4 z-50 lg:hidden">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsOpen(!isOpen)}
          className="text-gray-700 dark:text-gray-300"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </Button>
      </div>

      {/* Sidebar overlay on mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:sticky top-0 left-0 h-screen w-64 bg-white dark:bg-gray-950 border-r border-gray-200 dark:border-gray-800 flex flex-col z-40 transform transition-transform duration-300 lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Logo */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-800">
          <Link href="/dashboard" onClick={() => setIsOpen(false)}>
            <div className="flex items-center gap-3 cursor-pointer group">
              <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
                <span className="text-white font-bold text-lg">PLT</span>
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                PLT
              </span>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setIsOpen(false)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                isActive(item.href)
                  ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-900/50'
              }`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        {/* Footer - Dark mode toggle and user */}
        <div className="border-t border-gray-200 dark:border-gray-800 p-4 space-y-4">
          {/* Dark mode toggle */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsDark(!isDark)}
            className="w-full justify-start gap-3 text-gray-600 dark:text-gray-400"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
            <span className="text-sm">{isDark ? 'Light' : 'Dark'} Mode</span>
          </Button>

          {/* User profile */}
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-100 dark:bg-gray-900">
            <div className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center">
              <span className="text-white font-semibold text-sm">JD</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                John Doe
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Premium Member</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
