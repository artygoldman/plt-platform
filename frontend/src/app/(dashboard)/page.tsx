'use client';

import { useState } from 'react';
import { TrendingUp, TrendingDown, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

// Mock data for charts
const scoreData = [
  { date: 'Mon', score: 72 },
  { date: 'Tue', score: 74 },
  { date: 'Wed', score: 75 },
  { date: 'Thu', score: 76 },
  { date: 'Fri', score: 78 },
  { date: 'Sat', score: 79 },
  { date: 'Sun', score: 81 },
];

const bodySystemsData = [
  { name: 'Cardiovascular', score: 85, status: 'optimal' },
  { name: 'Metabolic', score: 78, status: 'optimal' },
  { name: 'Immune', score: 82, status: 'optimal' },
  { name: 'Hormonal', score: 75, status: 'warning' },
  { name: 'Neurological', score: 88, status: 'optimal' },
  { name: 'Musculoskeletal', score: 80, status: 'optimal' },
  { name: 'Digestive', score: 76, status: 'warning' },
  { name: 'Respiratory', score: 84, status: 'optimal' },
  { name: 'Dermatological', score: 81, status: 'optimal' },
  { name: 'Renal', score: 83, status: 'optimal' },
  { name: 'Hepatic', score: 79, status: 'optimal' },
];

export default function DashboardPage() {
  const [expandedSystem, setExpandedSystem] = useState<string | null>(null);

  const getLongevityScore = () => 81;
  const getBiologicalAge = () => 42;
  const getChronologicalAge = () => 55;
  const getTodayProgress = () => 85;
  const getOverallTwinScore = () => 81;

  return (
    <div className="space-y-6">
      {/* Header section */}
      <div className="space-y-2">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          Your Longevity Dashboard
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Track your health metrics and personal longevity journey
        </p>
      </div>

      {/* Top metrics grid - 3 columns on desktop, 2 on tablet, 1 on mobile */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Longevity Score Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Longevity Score
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="text-5xl font-bold text-emerald-600">
                {getLongevityScore()}
              </div>
              <div className="flex items-center gap-1 text-green-600">
                <TrendingUp size={20} />
                <span className="text-sm font-semibold">+2 pts</span>
              </div>
            </div>
            <div className="h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-600 rounded-full"
                style={{ width: `${(getLongevityScore() / 100) * 100}%` }}
              />
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Based on your biomarkers and lifestyle metrics
            </p>
          </CardContent>
        </Card>

        {/* Biological Age Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Biological Age
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="text-4xl font-bold text-emerald-600">
                  {getBiologicalAge()}
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Biological
                </p>
              </div>
              <div className="text-right space-y-1">
                <div className="text-3xl font-bold text-gray-400">
                  {getChronologicalAge()}
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Chronological
                </p>
              </div>
            </div>
            <Badge className="w-fit bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">
              {getChronologicalAge() - getBiologicalAge()} years younger
            </Badge>
          </CardContent>
        </Card>

        {/* Today's Contract Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Today's Contract
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Daily Progress
                </span>
                <span className="text-xs font-semibold text-emerald-600">
                  {getTodayProgress()}%
                </span>
              </div>
              <Progress value={getTodayProgress()} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-600 dark:text-gray-400">
                  ✓ Supplements taken
                </span>
                <CheckCircle size={16} className="text-emerald-600" />
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-600 dark:text-gray-400">
                  ✓ Exercise (45 min)
                </span>
                <CheckCircle size={16} className="text-emerald-600" />
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-600 dark:text-gray-400">
                  ◐ Sleep target (7.5h)
                </span>
                <Clock size={16} className="text-orange-500" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Second row of cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Biomarker Alerts Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Biomarker Alerts
            </CardTitle>
            <CardDescription className="text-xs">
              3 recent out-of-range values
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="p-3 bg-orange-50 dark:bg-orange-900/10 rounded border border-orange-200 dark:border-orange-900/30">
                <div className="flex items-start gap-2">
                  <AlertCircle size={16} className="text-orange-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-orange-900 dark:text-orange-200">
                      Blood Glucose
                    </p>
                    <p className="text-xs text-orange-700 dark:text-orange-300">
                      118 mg/dL (high)
                    </p>
                  </div>
                </div>
              </div>
              <div className="p-3 bg-yellow-50 dark:bg-yellow-900/10 rounded border border-yellow-200 dark:border-yellow-900/30">
                <div className="flex items-start gap-2">
                  <AlertCircle size={16} className="text-yellow-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-yellow-900 dark:text-yellow-200">
                      Inflammation Marker
                    </p>
                    <p className="text-xs text-yellow-700 dark:text-yellow-300">
                      CRP 3.2 (borderline)
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Agent Activity Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Agent Activity
            </CardTitle>
            <CardDescription className="text-xs">
              Last 5 decisions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {[
              {
                agent: 'Metabolic Agent',
                decision: 'Adjusted carb timing',
                status: 'completed',
              },
              {
                agent: 'Sleep Agent',
                decision: 'Recommended melatonin',
                status: 'pending',
              },
              {
                agent: 'Exercise Agent',
                decision: 'Increased recovery day',
                status: 'completed',
              },
              {
                agent: 'Immune Agent',
                decision: 'Added vitamin D',
                status: 'completed',
              },
            ].map((item, idx) => (
              <div key={idx} className="flex items-start justify-between text-xs p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-900">
                <div className="flex-1">
                  <p className="font-medium text-gray-900 dark:text-white">
                    {item.agent}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    {item.decision}
                  </p>
                </div>
                <Badge
                  className={
                    item.status === 'completed'
                      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300'
                      : 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                  }
                >
                  {item.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Weekly Streak Card */}
        <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Weekly Streak
            </CardTitle>
            <CardDescription className="text-xs">
              Your 7-day completion
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between items-end gap-2 h-24">
              {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, idx) => (
                <div key={day} className="text-center flex-1">
                  <div
                    className={`w-full h-16 rounded-t-lg mb-1 transition-all ${
                      idx < 6
                        ? 'bg-emerald-600'
                        : 'bg-gray-300 dark:bg-gray-700'
                    }`}
                  />
                  <p className="text-xs font-medium text-gray-600 dark:text-gray-400">
                    {day}
                  </p>
                </div>
              ))}
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-4 text-center">
              6/7 days complete • 86% consistency
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Score trend and Digital Twin Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score Trend Chart */}
        <Card className="lg:col-span-1 bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Score Trend
            </CardTitle>
            <CardDescription className="text-xs">
              Last 7 days
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={scoreData}>
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#059669"
                    strokeWidth={2}
                    dot={{ fill: '#059669', r: 4 }}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Digital Twin Summary */}
        <Card className="lg:col-span-2 bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
              Digital Twin Summary
            </CardTitle>
            <CardDescription className="text-xs">
              11 body systems health status
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {bodySystemsData.map((system) => (
                <div
                  key={system.name}
                  className="p-3 rounded-lg bg-gray-50 dark:bg-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {system.name}
                    </span>
                    <Badge
                      className={
                        system.status === 'optimal'
                          ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300'
                          : 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300'
                      }
                    >
                      {system.score}
                    </Badge>
                  </div>
                  <Progress value={system.score} className="h-1.5" />
                </div>
              ))}
            </div>
            <div className="pt-2 border-t border-gray-200 dark:border-gray-800">
              <p className="text-xs text-gray-600 dark:text-gray-400">
                <span className="font-semibold text-emerald-600">
                  Overall Twin Score: {getOverallTwinScore()}
                </span>
                • Updated 2 hours ago
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Upcoming Actions Card */}
      <Card className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800">
        <CardHeader>
          <CardTitle className="text-sm font-semibold text-gray-600 dark:text-gray-400">
            Upcoming Actions
          </CardTitle>
          <CardDescription className="text-xs">
            Next steps in your longevity protocol
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              {
                time: 'Today 3:00 PM',
                action: 'Take omega-3 supplement',
                type: 'supplement',
              },
              {
                time: 'Today 6:00 PM',
                action: 'Evening workout session',
                type: 'exercise',
              },
              {
                time: 'Tomorrow 9:00 AM',
                action: 'Doctor appointment',
                type: 'appointment',
              },
              {
                time: 'Tomorrow 2:00 PM',
                action: 'Biomarker test collection',
                type: 'test',
              },
            ].map((item, idx) => (
              <div
                key={idx}
                className="p-4 rounded-lg bg-gradient-to-br from-emerald-50 to-blue-50 dark:from-emerald-900/10 dark:to-blue-900/10 border border-emerald-200 dark:border-emerald-800"
              >
                <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                  {item.time}
                </p>
                <p className="text-sm font-semibold text-gray-900 dark:text-white">
                  {item.action}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
