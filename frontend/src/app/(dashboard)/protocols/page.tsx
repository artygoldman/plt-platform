'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Calendar, Plus, BarChart3, Zap } from 'lucide-react';

interface Supplement {
  name: string;
  dose: string;
  timing: string;
  purpose: string;
}

interface Protocol {
  id: string;
  name: string;
  status: 'active' | 'archived';
  createdDate: string;
  supplements: Supplement[];
  exercisePlan: string;
  sleepProtocol: string;
  dietRecommendations: string;
  notes: string;
}

const ACTIVE_PROTOCOL: Protocol = {
  id: 'protocol-1',
  name: 'Metabolic Optimization Protocol v3',
  status: 'active',
  createdDate: '2026-02-15',
  supplements: [
    {
      name: 'Omega-3 (Fish Oil)',
      dose: '2000 mg EPA/DHA',
      timing: 'Morning with breakfast',
      purpose: 'Cardiovascular health & inflammation',
    },
    {
      name: 'Magnesium Glycinate',
      dose: '400 mg',
      timing: 'Evening before bed',
      purpose: 'Sleep quality & muscle relaxation',
    },
    {
      name: 'Vitamin D3',
      dose: '4000 IU',
      timing: 'Morning with fat',
      purpose: 'Immune function & bone health',
    },
    {
      name: 'NAD+ Precursor (NMN)',
      dose: '500 mg',
      timing: 'Morning on empty stomach',
      purpose: 'Mitochondrial health & energy',
    },
    {
      name: 'Resveratrol',
      dose: '150 mg',
      timing: 'With lunch',
      purpose: 'Longevity & cellular health',
    },
    {
      name: 'Alpha-Lipoic Acid',
      dose: '200 mg',
      timing: 'Morning before eating',
      purpose: 'Insulin sensitivity & mitochondrial function',
    },
    {
      name: 'Berberine',
      dose: '500 mg',
      timing: 'Before meals (2x daily)',
      purpose: 'Blood glucose & lipid management',
    },
    {
      name: 'Zinc + Selenium',
      dose: '15 mg Zn / 100 mcg Se',
      timing: 'Evening with dinner',
      purpose: 'Immune & thyroid support',
    },
  ],
  exercisePlan:
    'Monday & Wednesday: Strength training (45 min, focus on compound movements). Tuesday & Thursday: HIIT cardio (30 min). Friday: Functional training (40 min). Saturday: Long-form cardio or sports (60-90 min). Sunday: Active recovery or mobility work.',
  sleepProtocol:
    'Bedtime: 10:30 PM. Wake time: 6:30 AM. Room temperature: 65-68°F. Blackout curtains. No screens 1 hour before bed. Magnesium supplement 30 minutes before sleep. Morning: 15 minutes of bright light exposure within 1 hour of waking.',
  dietRecommendations:
    'Macros: 40% protein, 35% fat, 25% carbs. Protein target: 140-160g daily. Prioritize whole foods: grass-fed meats, wild-caught fish, organic vegetables, berries, nuts. Avoid: processed foods, seed oils, excessive sugar. Meal timing: First meal 8 AM, last meal 7 PM (13-hour fasting window overnight).',
  notes: 'Focus on metabolic flexibility and sustained energy. Continue monitoring glucose responses. Target weight: 185 lbs. Reassess in 8 weeks.',
};

const PAST_PROTOCOLS: Protocol[] = [
  {
    id: 'protocol-2',
    name: 'Cardiovascular Focus Protocol v2',
    status: 'archived',
    createdDate: '2025-11-20',
    supplements: [
      {
        name: 'Omega-3',
        dose: '2000 mg',
        timing: 'Morning',
        purpose: 'Heart health',
      },
      {
        name: 'CoQ10',
        dose: '300 mg',
        timing: 'With meals',
        purpose: 'Heart muscle support',
      },
    ],
    exercisePlan: 'Cardio-focused with zone 2 training: 4x weekly 60-minute sessions at 110-130 bpm.',
    sleepProtocol: 'Target 8 hours. Consistent sleep schedule.',
    dietRecommendations: 'Mediterranean-style diet. High omega-3 foods. Limited saturated fats.',
    notes: 'Improved LDL by 15 points over 12 weeks.',
  },
  {
    id: 'protocol-3',
    name: 'Initial Assessment Protocol',
    status: 'archived',
    createdDate: '2025-09-10',
    supplements: [
      {
        name: 'Multivitamin',
        dose: '1 tablet',
        timing: 'Morning',
        purpose: 'Nutritional baseline',
      },
    ],
    exercisePlan: 'General fitness: 3x weekly mixed cardio and strength.',
    sleepProtocol: 'Baseline sleep tracking.',
    dietRecommendations: 'Balanced macros, adequate protein.',
    notes: 'Initial baseline protocol. Transitioned to metabolic optimization.',
  },
];

export default function ProtocolsPage() {
  const [selectedCompareProtocol, setSelectedCompareProtocol] = useState<Protocol | null>(null);
  const [showCompare, setShowCompare] = useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Protocols</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Your personalized health protocols and optimization plans
        </p>
      </div>

      {/* Active Protocol */}
      <Card className="border-emerald-500 dark:border-emerald-400 border-2">
        <CardHeader className="bg-emerald-50 dark:bg-emerald-900/20">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="flex items-center gap-2">
                <Zap size={20} className="text-emerald-600 dark:text-emerald-400" />
                {ACTIVE_PROTOCOL.name}
              </CardTitle>
              <CardDescription className="mt-2">
                Active since {new Date(ACTIVE_PROTOCOL.createdDate).toLocaleDateString()}
              </CardDescription>
            </div>
            <Badge className="bg-emerald-600 hover:bg-emerald-700">Active</Badge>
          </div>
        </CardHeader>

        <CardContent className="pt-6">
          <Tabs defaultValue="supplements" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="supplements">Supplements</TabsTrigger>
              <TabsTrigger value="exercise">Exercise</TabsTrigger>
              <TabsTrigger value="sleep">Sleep</TabsTrigger>
              <TabsTrigger value="diet">Diet</TabsTrigger>
            </TabsList>

            {/* Supplements Tab */}
            <TabsContent value="supplements" className="space-y-4 mt-4">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left p-3 font-semibold text-gray-900 dark:text-white">
                        Supplement
                      </th>
                      <th className="text-left p-3 font-semibold text-gray-900 dark:text-white">
                        Dose
                      </th>
                      <th className="text-left p-3 font-semibold text-gray-900 dark:text-white">
                        Timing
                      </th>
                      <th className="text-left p-3 font-semibold text-gray-900 dark:text-white">
                        Purpose
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {ACTIVE_PROTOCOL.supplements.map((supp, idx) => (
                      <tr
                        key={idx}
                        className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                      >
                        <td className="p-3 font-medium text-gray-900 dark:text-white">
                          {supp.name}
                        </td>
                        <td className="p-3 text-gray-600 dark:text-gray-400">{supp.dose}</td>
                        <td className="p-3 text-gray-600 dark:text-gray-400">{supp.timing}</td>
                        <td className="p-3 text-gray-600 dark:text-gray-400">{supp.purpose}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-4">
                Total daily cost: ~$4.50 | Total active supplements: {ACTIVE_PROTOCOL.supplements.length}
              </p>
            </TabsContent>

            {/* Exercise Tab */}
            <TabsContent value="exercise" className="space-y-4 mt-4">
              <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                  Exercise Plan
                </h4>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                  {ACTIVE_PROTOCOL.exercisePlan}
                </p>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-800">
                  <p className="text-xs font-semibold text-blue-900 dark:text-blue-300 uppercase">
                    Weekly Volume
                  </p>
                  <p className="text-lg font-bold text-blue-600 dark:text-blue-400 mt-1">
                    5-6 hours
                  </p>
                </div>
                <div className="bg-emerald-50 dark:bg-emerald-900/20 p-3 rounded-lg border border-emerald-200 dark:border-emerald-800">
                  <p className="text-xs font-semibold text-emerald-900 dark:text-emerald-300 uppercase">
                    Focus
                  </p>
                  <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-1">
                    Strength + HIIT
                  </p>
                </div>
                <div className="bg-amber-50 dark:bg-amber-900/20 p-3 rounded-lg border border-amber-200 dark:border-amber-800">
                  <p className="text-xs font-semibold text-amber-900 dark:text-amber-300 uppercase">
                    Recovery
                  </p>
                  <p className="text-sm font-bold text-amber-600 dark:text-amber-400 mt-1">
                    1-2 days
                  </p>
                </div>
              </div>
            </TabsContent>

            {/* Sleep Tab */}
            <TabsContent value="sleep" className="space-y-4 mt-4">
              <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                  Sleep Protocol
                </h4>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                  {ACTIVE_PROTOCOL.sleepProtocol}
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-purple-50 dark:bg-purple-900/20 p-3 rounded-lg border border-purple-200 dark:border-purple-800">
                  <p className="text-xs font-semibold text-purple-900 dark:text-purple-300 uppercase">
                    Bedtime
                  </p>
                  <p className="text-lg font-bold text-purple-600 dark:text-purple-400 mt-1">
                    10:30 PM
                  </p>
                </div>
                <div className="bg-indigo-50 dark:bg-indigo-900/20 p-3 rounded-lg border border-indigo-200 dark:border-indigo-800">
                  <p className="text-xs font-semibold text-indigo-900 dark:text-indigo-300 uppercase">
                    Wake Time
                  </p>
                  <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                    6:30 AM
                  </p>
                </div>
                <div className="bg-cyan-50 dark:bg-cyan-900/20 p-3 rounded-lg border border-cyan-200 dark:border-cyan-800">
                  <p className="text-xs font-semibold text-cyan-900 dark:text-cyan-300 uppercase">
                    Target Hours
                  </p>
                  <p className="text-lg font-bold text-cyan-600 dark:text-cyan-400 mt-1">
                    8 hours
                  </p>
                </div>
              </div>
            </TabsContent>

            {/* Diet Tab */}
            <TabsContent value="diet" className="space-y-4 mt-4">
              <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                  Diet Recommendations
                </h4>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                  {ACTIVE_PROTOCOL.dietRecommendations}
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-800">
                  <p className="text-xs font-semibold text-red-900 dark:text-red-300 uppercase">
                    Protein
                  </p>
                  <p className="text-lg font-bold text-red-600 dark:text-red-400 mt-1">
                    40%
                  </p>
                </div>
                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg border border-yellow-200 dark:border-yellow-800">
                  <p className="text-xs font-semibold text-yellow-900 dark:text-yellow-300 uppercase">
                    Fat
                  </p>
                  <p className="text-lg font-bold text-yellow-600 dark:text-yellow-400 mt-1">
                    35%
                  </p>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg border border-green-200 dark:border-green-800">
                  <p className="text-xs font-semibold text-green-900 dark:text-green-300 uppercase">
                    Carbs
                  </p>
                  <p className="text-lg font-bold text-green-600 dark:text-green-400 mt-1">
                    25%
                  </p>
                </div>
              </div>
            </TabsContent>
          </Tabs>

          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <h4 className="font-semibold text-blue-900 dark:text-blue-300 text-sm mb-2">Notes</h4>
            <p className="text-sm text-blue-800 dark:text-blue-200">
              {ACTIVE_PROTOCOL.notes}
            </p>
          </div>

          <div className="flex gap-3 mt-6">
            <Button className="flex-1">
              <BarChart3 size={16} className="mr-2" />
              View Analytics
            </Button>
            <Dialog>
              <DialogTrigger asChild>
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => setSelectedCompareProtocol(PAST_PROTOCOLS[0])}
                >
                  Compare Protocols
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Compare Protocols</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Select a protocol to compare with the active protocol
                  </p>
                  <div className="space-y-2">
                    {PAST_PROTOCOLS.map(protocol => (
                      <Button
                        key={protocol.id}
                        variant="outline"
                        className="w-full justify-start"
                        onClick={() => setSelectedCompareProtocol(protocol)}
                      >
                        {protocol.name}
                      </Button>
                    ))}
                  </div>
                </div>
              </DialogContent>
            </Dialog>
            <Button variant="outline" className="flex-1">
              <Plus size={16} className="mr-2" />
              Request Analysis
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Protocol History */}
      <Card>
        <CardHeader>
          <CardTitle>Protocol History</CardTitle>
          <CardDescription>Previously used and archived protocols</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {PAST_PROTOCOLS.map(protocol => (
              <div
                key={protocol.id}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-emerald-500 dark:hover:border-emerald-400 transition-colors"
              >
                <div className="flex items-start justify-between gap-4 mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">
                      {protocol.name}
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 flex items-center gap-1">
                      <Calendar size={14} />
                      {new Date(protocol.createdDate).toLocaleDateString()}
                    </p>
                  </div>
                  <Badge variant="outline">Archived</Badge>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2 mb-3">
                  {protocol.notes}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    View Details
                  </Button>
                  <Button size="sm" variant="outline">
                    Compare
                  </Button>
                  <Button size="sm" variant="outline">
                    Reactivate
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
