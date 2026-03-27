'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react';

interface Biomarker {
  id: string;
  name: string;
  category: 'blood' | 'hormones' | 'metabolic' | 'cardiovascular' | 'vitamins';
  currentValue: number;
  unit: string;
  referenceMin: number;
  referenceMax: number;
  status: 'optimal' | 'warning' | 'critical';
  trend: 'up' | 'down' | 'stable';
  lastUpdated: string;
  history: Array<{ date: string; value: number }>;
}

const MOCK_BIOMARKERS: Biomarker[] = [
  {
    id: 'glucose',
    name: 'Blood Glucose',
    category: 'metabolic',
    currentValue: 95,
    unit: 'mg/dL',
    referenceMin: 70,
    referenceMax: 100,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-27',
    history: [
      { date: '2025-09-27', value: 102 },
      { date: '2025-10-27', value: 98 },
      { date: '2025-11-27', value: 96 },
      { date: '2025-12-27', value: 94 },
      { date: '2026-01-27', value: 95 },
      { date: '2026-02-27', value: 94 },
      { date: '2026-03-27', value: 95 },
    ],
  },
  {
    id: 'hba1c',
    name: 'HbA1c',
    category: 'metabolic',
    currentValue: 5.2,
    unit: '%',
    referenceMin: 4.0,
    referenceMax: 5.6,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-15',
    history: [
      { date: '2025-09-15', value: 5.8 },
      { date: '2025-10-15', value: 5.6 },
      { date: '2025-11-15', value: 5.4 },
      { date: '2025-12-15', value: 5.3 },
      { date: '2026-01-15', value: 5.2 },
      { date: '2026-02-15', value: 5.2 },
      { date: '2026-03-15', value: 5.2 },
    ],
  },
  {
    id: 'cholesterol',
    name: 'Total Cholesterol',
    category: 'cardiovascular',
    currentValue: 185,
    unit: 'mg/dL',
    referenceMin: 0,
    referenceMax: 200,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 210 },
      { date: '2025-10-20', value: 205 },
      { date: '2025-11-20', value: 195 },
      { date: '2025-12-20', value: 188 },
      { date: '2026-01-20', value: 185 },
      { date: '2026-02-20', value: 185 },
      { date: '2026-03-20', value: 185 },
    ],
  },
  {
    id: 'ldl',
    name: 'LDL Cholesterol',
    category: 'cardiovascular',
    currentValue: 105,
    unit: 'mg/dL',
    referenceMin: 0,
    referenceMax: 130,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 135 },
      { date: '2025-10-20', value: 130 },
      { date: '2025-11-20', value: 120 },
      { date: '2025-12-20', value: 112 },
      { date: '2026-01-20', value: 108 },
      { date: '2026-02-20', value: 106 },
      { date: '2026-03-20', value: 105 },
    ],
  },
  {
    id: 'hdl',
    name: 'HDL Cholesterol',
    category: 'cardiovascular',
    currentValue: 58,
    unit: 'mg/dL',
    referenceMin: 40,
    referenceMax: 100,
    status: 'optimal',
    trend: 'up',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 42 },
      { date: '2025-10-20', value: 45 },
      { date: '2025-11-20', value: 48 },
      { date: '2025-12-20', value: 52 },
      { date: '2026-01-20', value: 55 },
      { date: '2026-02-20', value: 57 },
      { date: '2026-03-20', value: 58 },
    ],
  },
  {
    id: 'apoB',
    name: 'ApoB',
    category: 'cardiovascular',
    currentValue: 68,
    unit: 'mg/dL',
    referenceMin: 0,
    referenceMax: 130,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 98 },
      { date: '2025-10-20', value: 92 },
      { date: '2025-11-20', value: 82 },
      { date: '2025-12-20', value: 75 },
      { date: '2026-01-20', value: 70 },
      { date: '2026-02-20', value: 69 },
      { date: '2026-03-20', value: 68 },
    ],
  },
  {
    id: 'lpa',
    name: 'Lipoprotein(a)',
    category: 'cardiovascular',
    currentValue: 25,
    unit: 'nmol/L',
    referenceMin: 0,
    referenceMax: 50,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-15',
    history: [
      { date: '2025-09-15', value: 27 },
      { date: '2025-10-15', value: 27 },
      { date: '2025-11-15', value: 26 },
      { date: '2025-12-15', value: 25 },
      { date: '2026-01-15', value: 25 },
      { date: '2026-02-15', value: 25 },
      { date: '2026-03-15', value: 25 },
    ],
  },
  {
    id: 'testosterone',
    name: 'Testosterone',
    category: 'hormones',
    currentValue: 685,
    unit: 'ng/dL',
    referenceMin: 300,
    referenceMax: 1000,
    status: 'optimal',
    trend: 'up',
    lastUpdated: '2026-03-10',
    history: [
      { date: '2025-09-10', value: 545 },
      { date: '2025-10-10', value: 580 },
      { date: '2025-11-10', value: 620 },
      { date: '2025-12-10', value: 650 },
      { date: '2026-01-10', value: 670 },
      { date: '2026-02-10', value: 680 },
      { date: '2026-03-10', value: 685 },
    ],
  },
  {
    id: 'tsh',
    name: 'TSH',
    category: 'hormones',
    currentValue: 1.8,
    unit: 'mIU/L',
    referenceMin: 0.5,
    referenceMax: 5.0,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-01',
    history: [
      { date: '2025-09-01', value: 2.2 },
      { date: '2025-10-01', value: 2.0 },
      { date: '2025-11-01', value: 1.9 },
      { date: '2025-12-01', value: 1.8 },
      { date: '2026-01-01', value: 1.8 },
      { date: '2026-02-01', value: 1.8 },
      { date: '2026-03-01', value: 1.8 },
    ],
  },
  {
    id: 't3',
    name: 'Free T3',
    category: 'hormones',
    currentValue: 3.4,
    unit: 'pg/mL',
    referenceMin: 2.3,
    referenceMax: 4.2,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-01',
    history: [
      { date: '2025-09-01', value: 3.2 },
      { date: '2025-10-01', value: 3.2 },
      { date: '2025-11-01', value: 3.3 },
      { date: '2025-12-01', value: 3.4 },
      { date: '2026-01-01', value: 3.4 },
      { date: '2026-02-01', value: 3.4 },
      { date: '2026-03-01', value: 3.4 },
    ],
  },
  {
    id: 't4',
    name: 'Free T4',
    category: 'hormones',
    currentValue: 1.12,
    unit: 'ng/dL',
    referenceMin: 0.82,
    referenceMax: 1.77,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-01',
    history: [
      { date: '2025-09-01', value: 1.08 },
      { date: '2025-10-01', value: 1.09 },
      { date: '2025-11-01', value: 1.10 },
      { date: '2025-12-01', value: 1.11 },
      { date: '2026-01-01', value: 1.12 },
      { date: '2026-02-01', value: 1.12 },
      { date: '2026-03-01', value: 1.12 },
    ],
  },
  {
    id: 'cortisol',
    name: 'Cortisol (Morning)',
    category: 'hormones',
    currentValue: 18,
    unit: 'µg/dL',
    referenceMin: 10,
    referenceMax: 20,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-25',
    history: [
      { date: '2025-09-25', value: 22 },
      { date: '2025-10-25', value: 21 },
      { date: '2025-11-25', value: 20 },
      { date: '2025-12-25', value: 19 },
      { date: '2026-01-25', value: 18 },
      { date: '2026-02-25', value: 18 },
      { date: '2026-03-25', value: 18 },
    ],
  },
  {
    id: 'vitaminD',
    name: 'Vitamin D',
    category: 'vitamins',
    currentValue: 52,
    unit: 'ng/mL',
    referenceMin: 30,
    referenceMax: 100,
    status: 'optimal',
    trend: 'up',
    lastUpdated: '2026-03-10',
    history: [
      { date: '2025-09-10', value: 35 },
      { date: '2025-10-10', value: 38 },
      { date: '2025-11-10', value: 42 },
      { date: '2025-12-10', value: 47 },
      { date: '2026-01-10', value: 50 },
      { date: '2026-02-10', value: 51 },
      { date: '2026-03-10', value: 52 },
    ],
  },
  {
    id: 'b12',
    name: 'Vitamin B12',
    category: 'vitamins',
    currentValue: 650,
    unit: 'pg/mL',
    referenceMin: 200,
    referenceMax: 900,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-15',
    history: [
      { date: '2025-09-15', value: 640 },
      { date: '2025-10-15', value: 645 },
      { date: '2025-11-15', value: 648 },
      { date: '2025-12-15', value: 650 },
      { date: '2026-01-15', value: 650 },
      { date: '2026-02-15', value: 650 },
      { date: '2026-03-15', value: 650 },
    ],
  },
  {
    id: 'ferritin',
    name: 'Ferritin',
    category: 'vitamins',
    currentValue: 95,
    unit: 'ng/mL',
    referenceMin: 30,
    referenceMax: 300,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-10',
    history: [
      { date: '2025-09-10', value: 92 },
      { date: '2025-10-10', value: 93 },
      { date: '2025-11-10', value: 94 },
      { date: '2025-12-10', value: 95 },
      { date: '2026-01-10', value: 95 },
      { date: '2026-02-10', value: 95 },
      { date: '2026-03-10', value: 95 },
    ],
  },
  {
    id: 'crp',
    name: 'C-Reactive Protein',
    category: 'blood',
    currentValue: 0.8,
    unit: 'mg/L',
    referenceMin: 0,
    referenceMax: 3.0,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 2.5 },
      { date: '2025-10-20', value: 2.2 },
      { date: '2025-11-20', value: 1.8 },
      { date: '2025-12-20', value: 1.3 },
      { date: '2026-01-20', value: 1.0 },
      { date: '2026-02-20', value: 0.9 },
      { date: '2026-03-20', value: 0.8 },
    ],
  },
  {
    id: 'homocysteine',
    name: 'Homocysteine',
    category: 'blood',
    currentValue: 8.5,
    unit: 'µmol/L',
    referenceMin: 0,
    referenceMax: 15,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-15',
    history: [
      { date: '2025-09-15', value: 12.8 },
      { date: '2025-10-15', value: 12.0 },
      { date: '2025-11-15', value: 11.0 },
      { date: '2025-12-15', value: 10.0 },
      { date: '2026-01-15', value: 9.2 },
      { date: '2026-02-15', value: 8.8 },
      { date: '2026-03-15', value: 8.5 },
    ],
  },
  {
    id: 'insulin',
    name: 'Fasting Insulin',
    category: 'metabolic',
    currentValue: 4.2,
    unit: 'mIU/L',
    referenceMin: 2.0,
    referenceMax: 12.0,
    status: 'optimal',
    trend: 'down',
    lastUpdated: '2026-03-25',
    history: [
      { date: '2025-09-25', value: 6.5 },
      { date: '2025-10-25', value: 6.0 },
      { date: '2025-11-25', value: 5.4 },
      { date: '2025-12-25', value: 4.8 },
      { date: '2026-01-25', value: 4.5 },
      { date: '2026-02-25', value: 4.3 },
      { date: '2026-03-25', value: 4.2 },
    ],
  },
  {
    id: 'creatinine',
    name: 'Creatinine',
    category: 'blood',
    currentValue: 0.95,
    unit: 'mg/dL',
    referenceMin: 0.7,
    referenceMax: 1.3,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 0.96 },
      { date: '2025-10-20', value: 0.96 },
      { date: '2025-11-20', value: 0.95 },
      { date: '2025-12-20', value: 0.95 },
      { date: '2026-01-20', value: 0.95 },
      { date: '2026-02-20', value: 0.95 },
      { date: '2026-03-20', value: 0.95 },
    ],
  },
  {
    id: 'alt',
    name: 'ALT',
    category: 'blood',
    currentValue: 28,
    unit: 'U/L',
    referenceMin: 7,
    referenceMax: 56,
    status: 'optimal',
    trend: 'stable',
    lastUpdated: '2026-03-20',
    history: [
      { date: '2025-09-20', value: 32 },
      { date: '2025-10-20', value: 30 },
      { date: '2025-11-20', value: 29 },
      { date: '2025-12-20', value: 28 },
      { date: '2026-01-20', value: 28 },
      { date: '2026-02-20', value: 28 },
      { date: '2026-03-20', value: 28 },
    ],
  },
];

export default function BiomarkersPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedBiomarker, setSelectedBiomarker] = useState<Biomarker | null>(null);
  const [showDetail, setShowDetail] = useState(false);

  const categories = ['all', 'blood', 'hormones', 'metabolic', 'cardiovascular', 'vitamins'];

  const filteredBiomarkers = selectedCategory === 'all'
    ? MOCK_BIOMARKERS
    : MOCK_BIOMARKERS.filter(b => b.category === selectedCategory);

  const criticalBiomarkers = MOCK_BIOMARKERS.filter(b => b.status === 'critical' || b.status === 'warning');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'optimal':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400';
      case 'warning':
        return 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400';
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400';
    }
  };

  const getTrendIcon = (trend: string) => {
    if (trend === 'up') return <TrendingUp size={16} className="text-emerald-600" />;
    if (trend === 'down') return <TrendingDown size={16} className="text-emerald-600" />;
    return <span className="text-gray-400">—</span>;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Biomarkers</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Monitor your health metrics and trends</p>
      </div>

      {criticalBiomarkers.length > 0 && (
        <Alert className="border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-900/50">
          <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
          <AlertDescription className="text-red-700 dark:text-red-300">
            {criticalBiomarkers.length} biomarker(s) outside optimal range. Review and take action.
          </AlertDescription>
        </Alert>
      )}

      <Tabs value={selectedCategory} onValueChange={setSelectedCategory} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="blood">Blood</TabsTrigger>
          <TabsTrigger value="hormones">Hormones</TabsTrigger>
          <TabsTrigger value="metabolic">Metabolic</TabsTrigger>
          <TabsTrigger value="cardiovascular">Cardio</TabsTrigger>
          <TabsTrigger value="vitamins">Vitamins</TabsTrigger>
        </TabsList>

        <TabsContent value={selectedCategory} className="space-y-4 mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredBiomarkers.map(biomarker => (
              <Card
                key={biomarker.id}
                className="cursor-pointer hover:border-emerald-500 dark:hover:border-emerald-400 transition-colors"
                onClick={() => {
                  setSelectedBiomarker(biomarker);
                  setShowDetail(true);
                }}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-base">{biomarker.name}</CardTitle>
                      <CardDescription className="text-xs mt-1">
                        Ref: {biomarker.referenceMin}-{biomarker.referenceMax} {biomarker.unit}
                      </CardDescription>
                    </div>
                    <Badge className={getStatusColor(biomarker.status)}>
                      {biomarker.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-baseline justify-between">
                      <span className="text-2xl font-bold text-gray-900 dark:text-white">
                        {biomarker.currentValue}
                      </span>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {biomarker.unit}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-600 dark:text-gray-400">
                        Updated {new Date(biomarker.lastUpdated).toLocaleDateString()}
                      </span>
                      {getTrendIcon(biomarker.trend)}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      <Dialog open={showDetail} onOpenChange={setShowDetail}>
        <DialogContent className="max-w-2xl">
          {selectedBiomarker && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center justify-between">
                  <span>{selectedBiomarker.name}</span>
                  <Badge className={getStatusColor(selectedBiomarker.status)}>
                    {selectedBiomarker.status}
                  </Badge>
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-6">
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold">
                      Current Value
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                      {selectedBiomarker.currentValue} {selectedBiomarker.unit}
                    </p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold">
                      Reference Range
                    </p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white mt-2">
                      {selectedBiomarker.referenceMin}–{selectedBiomarker.referenceMax}
                    </p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold">
                      Trend
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      {getTrendIcon(selectedBiomarker.trend)}
                      <span className="font-semibold text-gray-900 dark:text-white capitalize">
                        {selectedBiomarker.trend}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-4">6-Month History</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={selectedBiomarker.history}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis
                        dataKey="date"
                        stroke="#9ca3af"
                        style={{ fontSize: '12px' }}
                        tick={{ fill: '#9ca3af' }}
                      />
                      <YAxis
                        stroke="#9ca3af"
                        style={{ fontSize: '12px' }}
                        tick={{ fill: '#9ca3af' }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1f2937',
                          border: '1px solid #374151',
                          borderRadius: '8px',
                        }}
                        labelStyle={{ color: '#fff' }}
                      />
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#10b981"
                        dot={{ fill: '#10b981', r: 4 }}
                        activeDot={{ r: 6 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-300 text-sm">Recommendations</h4>
                  <ul className="text-sm text-blue-800 dark:text-blue-200 mt-2 space-y-1 list-disc list-inside">
                    <li>Maintain current lifestyle habits</li>
                    <li>Continue with routine monitoring</li>
                    <li>Schedule follow-up in 3 months</li>
                  </ul>
                </div>

                <Button onClick={() => setShowDetail(false)} className="w-full">
                  Close
                </Button>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
