'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Progress } from '@/components/ui/progress';
import { Flame, Calendar } from 'lucide-react';

interface ContractItem {
  id: string;
  time: string;
  title: string;
  description: string;
  category: 'morning' | 'midday' | 'evening';
  categoryLabel: string;
  completed: boolean;
}

interface CalendarDay {
  date: string;
  status: 'completed' | 'partial' | 'missed';
}

const MOCK_CONTRACTS: ContractItem[] = [
  // Morning
  {
    id: 'morning-1',
    time: '07:00',
    title: 'Morning Supplements',
    description: 'Take daily supplement stack: Omega-3, Magnesium, NAD+, NMN',
    category: 'morning',
    categoryLabel: 'Morning',
    completed: true,
  },
  {
    id: 'morning-2',
    time: '07:30',
    title: 'Blood Glucose Check',
    description: 'Measure fasting glucose level',
    category: 'morning',
    categoryLabel: 'Morning',
    completed: true,
  },
  {
    id: 'morning-3',
    time: '08:00',
    title: 'Cold Plunge',
    description: '3 minutes in 50°F cold water',
    category: 'morning',
    categoryLabel: 'Morning',
    completed: false,
  },
  {
    id: 'morning-4',
    time: '08:15',
    title: 'Morning Sunlight',
    description: '15 minutes of natural light exposure',
    category: 'morning',
    categoryLabel: 'Morning',
    completed: true,
  },
  // Midday
  {
    id: 'midday-1',
    time: '12:00',
    title: 'Strength Training',
    description: 'Resistance exercise: 45 minutes',
    category: 'midday',
    categoryLabel: 'Midday',
    completed: true,
  },
  {
    id: 'midday-2',
    time: '13:00',
    title: 'Hydration Goal',
    description: 'Drink 500ml of water with electrolytes',
    category: 'midday',
    categoryLabel: 'Midday',
    completed: true,
  },
  {
    id: 'midday-3',
    time: '14:00',
    title: 'Midday Glucose Check',
    description: 'Measure glucose level 2 hours post-meal',
    category: 'midday',
    categoryLabel: 'Midday',
    completed: false,
  },
  {
    id: 'midday-4',
    time: '14:30',
    title: 'Walk Break',
    description: '15 minute walk after lunch',
    category: 'midday',
    categoryLabel: 'Midday',
    completed: true,
  },
  // Evening
  {
    id: 'evening-1',
    time: '18:00',
    title: 'Evening Supplements',
    description: 'Take: Magnesium Glycinate, Zinc, Vitamin K2',
    category: 'evening',
    categoryLabel: 'Evening',
    completed: false,
  },
  {
    id: 'evening-2',
    time: '20:00',
    title: 'Sleep Protocol',
    description: 'Dim lights, set temperature to 65°F, no screens 30min before bed',
    category: 'evening',
    categoryLabel: 'Evening',
    completed: false,
  },
  {
    id: 'evening-3',
    time: '20:30',
    title: 'Meditation',
    description: '10 minutes of guided meditation or breathwork',
    category: 'evening',
    categoryLabel: 'Evening',
    completed: false,
  },
  {
    id: 'evening-4',
    time: '21:00',
    title: 'Bedtime Routine',
    description: 'Target sleep: 8 hours. Aim for 10 PM bedtime.',
    category: 'evening',
    categoryLabel: 'Evening',
    completed: false,
  },
];

const MOCK_CALENDAR: CalendarDay[] = [
  ...Array.from({ length: 25 }, (_, i) => ({
    date: `2026-03-${(i + 1).toString().padStart(2, '0')}`,
    status: i < 5 ? ('completed' as const) : i < 10 ? ('partial' as const) : ('completed' as const),
  })),
  ...Array.from({ length: 2 }, (_, i) => ({
    date: `2026-03-${(i + 26).toString().padStart(2, '0')}`,
    status: 'partial' as const,
  })),
];

export default function ContractsPage() {
  const [contracts, setContracts] = useState<ContractItem[]>(MOCK_CONTRACTS);
  const [selectedMonth, setSelectedMonth] = useState('2026-03');

  const toggleComplete = (id: string) => {
    setContracts(contracts.map(c => c.id === id ? { ...c, completed: !c.completed } : c));
  };

  const completedCount = contracts.filter(c => c.completed).length;
  const completionPercentage = (completedCount / contracts.length) * 100;
  const streak = 25;

  const groupedByCategory = {
    morning: contracts.filter(c => c.category === 'morning'),
    midday: contracts.filter(c => c.category === 'midday'),
    evening: contracts.filter(c => c.category === 'evening'),
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-emerald-500';
      case 'partial':
        return 'bg-amber-500';
      case 'missed':
        return 'bg-gray-400';
      default:
        return 'bg-gray-300';
    }
  };

  const getStatusLabel = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Daily Contracts</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Your daily health commitments and progress tracking</p>
      </div>

      {/* Progress Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Today's Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {completedCount}/{contracts.length}
              </div>
              <Progress value={completionPercentage} className="h-2" />
              <p className="text-xs text-gray-600 dark:text-gray-400">
                {completionPercentage.toFixed(0)}% completed
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Flame size={16} className="text-orange-500" />
              Streak
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-orange-600">
                {streak}
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                consecutive days
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Upcoming</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {contracts.filter(c => !c.completed).length}
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                items remaining today
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Daily Contract Checklist */}
      <Card>
        <CardHeader>
          <CardTitle>Today's Contract</CardTitle>
          <CardDescription>
            Complete all items to maintain your streak and achieve optimal health
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {Object.entries(groupedByCategory).map(([categoryKey, items]) => (
            <div key={categoryKey}>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3 capitalize">
                {categoryKey} ({items.filter(i => i.completed).length}/{items.length})
              </h3>
              <div className="space-y-2">
                {items.map(item => (
                  <div
                    key={item.id}
                    className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-400 transition-colors"
                  >
                    <Checkbox
                      checked={item.completed}
                      onCheckedChange={() => toggleComplete(item.id)}
                      className="mt-1"
                    />
                    <div className="flex-1 min-w-0">
                      <p
                        className={`font-medium text-sm ${
                          item.completed
                            ? 'text-gray-500 dark:text-gray-500 line-through'
                            : 'text-gray-900 dark:text-white'
                        }`}
                      >
                        {item.title}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {item.description}
                      </p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="outline" className="text-xs">
                          {item.time}
                        </Badge>
                        <Badge variant="secondary" className="text-xs">
                          {item.categoryLabel}
                        </Badge>
                      </div>
                    </div>
                    {item.completed && (
                      <div className="text-emerald-600 dark:text-emerald-400 font-bold text-lg">✓</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* 30-Day Calendar View */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar size={20} />
            March 2026 Overview
          </CardTitle>
          <CardDescription>
            Green = completed, Yellow = partial, Gray = missed
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-7 gap-2">
            {/* Day headers */}
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div
                key={day}
                className="h-10 flex items-center justify-center font-semibold text-gray-600 dark:text-gray-400 text-sm"
              >
                {day}
              </div>
            ))}

            {/* Calendar days */}
            {Array.from({ length: 6 }, (_, weekIdx) =>
              Array.from({ length: 7 }, (_, dayIdx) => {
                const dayNum = weekIdx * 7 + dayIdx + 1;
                if (dayNum > 31) return null;

                const dayData = MOCK_CALENDAR.find(d =>
                  d.date === `2026-03-${dayNum.toString().padStart(2, '0')}`
                );

                return (
                  <div
                    key={dayNum}
                    className={`h-10 rounded-lg flex items-center justify-center font-medium text-sm cursor-pointer transition-transform hover:scale-105 ${
                      dayData
                        ? `${getStatusColor(dayData.status)} text-white`
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500'
                    }`}
                    title={dayData ? getStatusLabel(dayData.status) : ''}
                  >
                    {dayNum}
                  </div>
                );
              })
            )}
          </div>

          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-emerald-500 rounded" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Completed</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-amber-500 rounded" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Partial</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-400 rounded" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Missed</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
