'use client';

import { useState } from 'react';
import { ChevronDown, TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface BodySystem {
  id: string;
  name: string;
  score: number;
  status: 'optimal' | 'warning' | 'critical';
  trend: 'up' | 'down' | 'stable';
  trendValue: number;
  description: string;
  keyBiomarkers: Array<{
    name: string;
    value: string;
    status: 'optimal' | 'warning' | 'critical';
  }>;
}

const bodySystems: BodySystem[] = [
  {
    id: 'cardiovascular',
    name: 'Cardiovascular',
    score: 85,
    status: 'optimal',
    trend: 'up',
    trendValue: 3,
    description: 'Heart and blood vessel health performing optimally',
    keyBiomarkers: [
      { name: 'Resting Heart Rate', value: '58 bpm', status: 'optimal' },
      { name: 'Blood Pressure', value: '118/76 mmHg', status: 'optimal' },
      { name: 'Cholesterol', value: '180 mg/dL', status: 'optimal' },
    ],
  },
  {
    id: 'metabolic',
    name: 'Metabolic',
    score: 78,
    status: 'optimal',
    trend: 'stable',
    trendValue: 0,
    description: 'Energy production and nutrient processing functioning well',
    keyBiomarkers: [
      { name: 'Blood Glucose', value: '105 mg/dL', status: 'warning' },
      { name: 'Insulin', value: '9.2 µU/mL', status: 'optimal' },
      { name: 'Metabolic Rate', value: '1680 kcal/day', status: 'optimal' },
    ],
  },
  {
    id: 'immune',
    name: 'Immune',
    score: 82,
    status: 'optimal',
    trend: 'up',
    trendValue: 2,
    description: 'Immune system strength and disease resistance are strong',
    keyBiomarkers: [
      { name: 'White Blood Cells', value: '6.8 K/µL', status: 'optimal' },
      { name: 'Lymphocytes', value: '32%', status: 'optimal' },
      { name: 'Inflammation Marker', value: '3.2 mg/L', status: 'warning' },
    ],
  },
  {
    id: 'hormonal',
    name: 'Hormonal',
    score: 75,
    status: 'warning',
    trend: 'down',
    trendValue: -2,
    description: 'Hormone balance needs attention and optimization',
    keyBiomarkers: [
      { name: 'Cortisol', value: '12 µg/dL', status: 'warning' },
      { name: 'Thyroid (TSH)', value: '2.3 mIU/L', status: 'optimal' },
      { name: 'Testosterone', value: '580 ng/dL', status: 'warning' },
    ],
  },
  {
    id: 'neurological',
    name: 'Neurological',
    score: 88,
    status: 'optimal',
    trend: 'up',
    trendValue: 4,
    description: 'Brain function and cognitive performance excellent',
    keyBiomarkers: [
      { name: 'Cognitive Function', value: 'Excellent', status: 'optimal' },
      { name: 'Sleep Quality', value: '8.2/10', status: 'optimal' },
      { name: 'Reaction Time', value: '250ms', status: 'optimal' },
    ],
  },
  {
    id: 'musculoskeletal',
    name: 'Musculoskeletal',
    score: 80,
    status: 'optimal',
    trend: 'up',
    trendValue: 2,
    description: 'Muscle and bone health maintaining strength',
    keyBiomarkers: [
      { name: 'Muscle Mass', value: '38 kg', status: 'optimal' },
      { name: 'Bone Density', value: 'T-score: +0.8', status: 'optimal' },
      { name: 'Flexibility', value: 'Good', status: 'optimal' },
    ],
  },
  {
    id: 'digestive',
    name: 'Digestive',
    score: 76,
    status: 'warning',
    trend: 'stable',
    trendValue: 0,
    description: 'Digestive function adequate, microbiome needs support',
    keyBiomarkers: [
      { name: 'Gut Dysbiosis Index', value: '5.2', status: 'warning' },
      { name: 'Digestive Enzymes', value: 'Normal', status: 'optimal' },
      { name: 'Intestinal Permeability', value: 'Moderate', status: 'warning' },
    ],
  },
  {
    id: 'respiratory',
    name: 'Respiratory',
    score: 84,
    status: 'optimal',
    trend: 'stable',
    trendValue: 1,
    description: 'Lung function and oxygen capacity are strong',
    keyBiomarkers: [
      { name: 'FEV1', value: '92% predicted', status: 'optimal' },
      { name: 'VO2 Max', value: '45 ml/kg/min', status: 'optimal' },
      { name: 'Oxygen Saturation', value: '98%', status: 'optimal' },
    ],
  },
  {
    id: 'dermatological',
    name: 'Dermatological',
    score: 81,
    status: 'optimal',
    trend: 'up',
    trendValue: 1,
    description: 'Skin health and barrier function excellent',
    keyBiomarkers: [
      { name: 'Hydration Level', value: '45%', status: 'optimal' },
      { name: 'Collagen Density', value: 'Good', status: 'optimal' },
      { name: 'pH Balance', value: '5.2', status: 'optimal' },
    ],
  },
  {
    id: 'renal',
    name: 'Renal',
    score: 83,
    status: 'optimal',
    trend: 'stable',
    trendValue: 0,
    description: 'Kidney function and filtration performing optimally',
    keyBiomarkers: [
      { name: 'Creatinine', value: '0.9 mg/dL', status: 'optimal' },
      { name: 'GFR', value: '92 mL/min/1.73m²', status: 'optimal' },
      { name: 'Electrolytes', value: 'Balanced', status: 'optimal' },
    ],
  },
  {
    id: 'hepatic',
    name: 'Hepatic',
    score: 79,
    status: 'optimal',
    trend: 'up',
    trendValue: 1,
    description: 'Liver function and detoxification capacity adequate',
    keyBiomarkers: [
      { name: 'AST', value: '28 U/L', status: 'optimal' },
      { name: 'ALT', value: '22 U/L', status: 'optimal' },
      { name: 'Bilirubin', value: '0.8 mg/dL', status: 'optimal' },
    ],
  },
];

const getStatusColor = (status: 'optimal' | 'warning' | 'critical') => {
  switch (status) {
    case 'optimal':
      return 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300';
    case 'warning':
      return 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300';
    case 'critical':
      return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300';
  }
};

const getProgressColor = (status: 'optimal' | 'warning' | 'critical') => {
  switch (status) {
    case 'optimal':
      return '';
    case 'warning':
      return 'accent-orange-500';
    case 'critical':
      return 'accent-red-500';
  }
};

export default function DigitalTwinPage() {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const overallScore = Math.round(
    bodySystems.reduce((sum, sys) => sum + sys.score, 0) / bodySystems.length
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          Digital Twin Analysis
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Complete body systems health assessment
        </p>
      </div>

      {/* Overall Score Card */}
      <Card className="bg-gradient-to-br from-emerald-50 to-blue-50 dark:from-emerald-900/20 dark:to-blue-900/20 border-emerald-200 dark:border-emerald-800">
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex-1">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                Overall Digital Twin Health Score
              </p>
              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-bold text-emerald-600">
                  {overallScore}
                </span>
                <span className="text-lg text-gray-600 dark:text-gray-400">
                  / 100
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                {bodySystems.filter((s) => s.status === 'optimal').length} systems optimal •{' '}
                {bodySystems.filter((s) => s.status === 'warning').length} systems need attention
              </p>
            </div>
            <div className="relative w-32 h-32">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-gray-200 dark:text-gray-700"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="8"
                  strokeDasharray={`${(overallScore / 100) * 251.2} 251.2`}
                  strokeLinecap="round"
                  className="text-emerald-600 transform -rotate-90"
                  style={{ transformOrigin: '50% 50%' }}
                />
                <text
                  x="50"
                  y="50"
                  textAnchor="middle"
                  dy="0.3em"
                  className="text-2xl font-bold fill-emerald-600"
                >
                  {overallScore}
                </text>
              </svg>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Body Systems Grid */}
      <div className="space-y-3">
        <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">
          Body Systems Status
        </p>
        <div className="grid gap-3">
          {bodySystems.map((system) => (
            <Card
              key={system.id}
              className="bg-white dark:bg-gray-950 border-gray-200 dark:border-gray-800 cursor-pointer hover:border-emerald-300 dark:hover:border-emerald-700 transition-colors"
              onClick={() =>
                setExpandedId(expandedId === system.id ? null : system.id)
              }
            >
              <CardContent className="p-0">
                {/* System header */}
                <div className="p-4 flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
                        {system.name}
                      </h3>
                      <Badge className={getStatusColor(system.status)}>
                        {system.status.charAt(0).toUpperCase() +
                          system.status.slice(1)}
                      </Badge>
                      <div className="flex items-center gap-1 text-xs font-semibold ml-auto">
                        {system.trend === 'up' && (
                          <TrendingUp size={14} className="text-green-600" />
                        )}
                        {system.trend === 'down' && (
                          <TrendingDown size={14} className="text-orange-600" />
                        )}
                        <span
                          className={
                            system.trend === 'up'
                              ? 'text-green-600'
                              : system.trend === 'down'
                              ? 'text-orange-600'
                              : 'text-gray-600'
                          }
                        >
                          {system.trend === 'up' ? '+' : ''}
                          {system.trendValue}
                        </span>
                      </div>
                    </div>

                    {/* Score bar */}
                    <div className="flex items-center gap-3">
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-gray-600 dark:text-gray-400">
                            System Score
                          </span>
                          <span className="text-sm font-bold text-emerald-600">
                            {system.score}/100
                          </span>
                        </div>
                        <Progress
                          value={system.score}
                          className={getProgressColor(system.status)}
                        />
                      </div>
                    </div>

                    {/* Description */}
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">
                      {system.description}
                    </p>
                  </div>

                  {/* Expand button */}
                  <ChevronDown
                    size={20}
                    className={`text-gray-400 transition-transform ml-4 flex-shrink-0 ${
                      expandedId === system.id ? 'rotate-180' : ''
                    }`}
                  />
                </div>

                {/* Expanded content */}
                {expandedId === system.id && (
                  <div className="border-t border-gray-200 dark:border-gray-800 p-4 bg-gray-50 dark:bg-gray-900/50 space-y-4">
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
                        Key Biomarkers
                      </h4>
                      <div className="space-y-2">
                        {system.keyBiomarkers.map((marker, idx) => (
                          <div
                            key={idx}
                            className="flex items-center justify-between p-3 bg-white dark:bg-gray-950 rounded border border-gray-200 dark:border-gray-800"
                          >
                            <div>
                              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">
                                {marker.name}
                              </p>
                              <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">
                                {marker.value}
                              </p>
                            </div>
                            <Badge className={getStatusColor(marker.status)}>
                              {marker.status === 'optimal'
                                ? 'Optimal'
                                : marker.status === 'warning'
                                ? 'Warning'
                                : 'Critical'}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800 rounded p-3">
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        <span className="font-semibold">Recommendation:</span> Monitor
                        this system regularly and discuss optimizations with your health
                        team. Schedule follow-up tests in 8 weeks.
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Last Updated */}
      <Card className="bg-gray-50 dark:bg-gray-900/50 border-gray-200 dark:border-gray-800">
        <CardContent className="p-4">
          <p className="text-xs text-gray-600 dark:text-gray-400">
            <span className="font-semibold">Last Updated:</span> Today at 2:30 PM
            based on latest biomarker tests and wearable data
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
