'use client';

import { useState } from 'react';
import { Bell, Search, LogOut, Settings, User as UserIcon } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';

interface HeaderProps {
  title?: string;
}

export function Header({ title = 'Dashboard' }: HeaderProps) {
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="sticky top-0 z-30 w-full bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
      <div className="flex items-center justify-between h-16 px-6 gap-4">
        {/* Left side - Title */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {title}
          </h1>
        </div>

        {/* Right side - Search, Notifications, User Menu */}
        <div className="flex items-center gap-4">
          {/* Search bar - hidden on mobile */}
          <div className="hidden md:flex items-center gap-2 bg-gray-100 dark:bg-gray-900 rounded-lg px-3 py-2 flex-1 max-w-xs">
            <Search size={18} className="text-gray-500 dark:text-gray-400" />
            <Input
              type="text"
              placeholder="Search..."
              className="bg-transparent border-0 focus:ring-0 text-sm"
            />
          </div>

          {/* Notifications bell */}
          <div className="relative">
            <Button
              variant="ghost"
              size="icon"
              className="relative text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              onClick={() => setShowNotifications(!showNotifications)}
            >
              <Bell size={20} />
              {/* Notification badge */}
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full" />
            </Button>

            {/* Notifications dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 shadow-lg z-50">
                <div className="p-4">
                  <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
                    Notifications
                  </h3>
                  <div className="space-y-3">
                    {[
                      {
                        title: 'Biomarker Alert',
                        message: 'Your blood glucose is above optimal range',
                        time: '2 hours ago',
                      },
                      {
                        title: 'Daily Contract',
                        message: 'You completed today\'s exercise target',
                        time: '4 hours ago',
                      },
                      {
                        title: 'Agent Decision',
                        message: 'Metabolic Agent recommends protocol adjustment',
                        time: '1 day ago',
                      },
                    ].map((notif, idx) => (
                      <div
                        key={idx}
                        className="p-3 bg-gray-50 dark:bg-gray-800/50 rounded border border-gray-200 dark:border-gray-700"
                      >
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {notif.title}
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {notif.message}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                          {notif.time}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* User avatar dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full overflow-hidden w-10 h-10 bg-emerald-600"
              >
                <span className="text-white font-semibold text-sm">JD</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <div className="p-4 pb-2">
                <p className="text-sm font-semibold text-gray-900 dark:text-white">
                  John Doe
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  john@example.com
                </p>
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link href="/profile" className="flex items-center gap-2 cursor-pointer">
                  <UserIcon size={16} />
                  <span>Profile</span>
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link href="/settings" className="flex items-center gap-2 cursor-pointer">
                  <Settings size={16} />
                  <span>Settings</span>
                </Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600 dark:text-red-400 flex items-center gap-2 cursor-pointer">
                <LogOut size={16} />
                <span>Logout</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
