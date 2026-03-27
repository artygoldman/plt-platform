'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ChevronDown, ChevronRight, Clock } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  tier: number;
  status: 'active' | 'idle' | 'running';
  lastRun: string;
  decisionsCount: number;
  description: string;
  recentDecisions: string[];
}

const MOCK_AGENTS: Agent[] = [
  // Tier 1: Strategic Core
  {
    id: 'cmo',
    name: 'Chief Medical Officer',
    tier: 1,
    status: 'active',
    lastRun: '2 hours ago',
    decisionsCount: 847,
    description: 'Strategic oversight and medical decision authority',
    recentDecisions: [
      'Approved new cardiovascular protocol',
      'Reviewed quarterly health summary',
      'Escalated hormone imbalance concern',
    ],
  },
  {
    id: 'verifier',
    name: 'Data Verifier',
    tier: 1,
    status: 'idle',
    lastRun: '5 hours ago',
    decisionsCount: 1203,
    description: 'Validates data integrity and consistency',
    recentDecisions: [
      'Verified blood test authenticity',
      'Flagged inconsistent glucose readings',
      'Confirmed wearable data accuracy',
    ],
  },
  {
    id: 'sysbiologist',
    name: 'System Biologist',
    tier: 1,
    status: 'active',
    lastRun: '1 hour ago',
    decisionsCount: 562,
    description: 'Analyzes biological system interactions',
    recentDecisions: [
      'Identified HPA axis dysregulation',
      'Connected gut health to inflammation',
      'Predicted seasonal metabolic shifts',
    ],
  },
  {
    id: 'analyst',
    name: 'Data Analyst',
    tier: 1,
    status: 'running',
    lastRun: 'Now',
    decisionsCount: 1544,
    description: 'Processes and interprets health metrics',
    recentDecisions: [
      'Completed monthly trend analysis',
      'Generated predictive models',
      'Identified outlier biomarkers',
    ],
  },
  // Tier 2: Medical Core (8 specialists)
  {
    id: 'cardiologist',
    name: 'Cardiologist Agent',
    tier: 2,
    status: 'idle',
    lastRun: '3 days ago',
    decisionsCount: 234,
    description: 'Cardiovascular health specialist',
    recentDecisions: [
      'Monitored LDL trends',
      'Assessed arterial health markers',
      'Recommended CoQ10 supplementation',
    ],
  },
  {
    id: 'endocrinologist',
    name: 'Endocrinologist Agent',
    tier: 2,
    status: 'active',
    lastRun: '4 hours ago',
    decisionsCount: 412,
    description: 'Hormone and metabolic specialist',
    recentDecisions: [
      'Analyzed testosterone decline',
      'Optimized insulin sensitivity protocol',
      'Reviewed thyroid function',
    ],
  },
  {
    id: 'gastroenterologist',
    name: 'Gastroenterologist Agent',
    tier: 2,
    status: 'idle',
    lastRun: '2 weeks ago',
    decisionsCount: 156,
    description: 'Digestive system specialist',
    recentDecisions: [
      'Recommended probiotic strains',
      'Assessed microbiome diversity',
      'Suggested dietary modifications',
    ],
  },
  {
    id: 'neurologist',
    name: 'Neurologist Agent',
    tier: 2,
    status: 'idle',
    lastRun: '10 days ago',
    decisionsCount: 189,
    description: 'Neurological health specialist',
    recentDecisions: [
      'Evaluated cognitive markers',
      'Recommended neuroprotective compounds',
      'Assessed sleep quality metrics',
    ],
  },
  {
    id: 'immunologist',
    name: 'Immunologist Agent',
    tier: 2,
    status: 'active',
    lastRun: '6 hours ago',
    decisionsCount: 356,
    description: 'Immune system specialist',
    recentDecisions: [
      'Monitored inflammation markers',
      'Recommended immune-boosting protocol',
      'Analyzed vaccine response data',
    ],
  },
  {
    id: 'orthopedist',
    name: 'Orthopedist Agent',
    tier: 2,
    status: 'idle',
    lastRun: '1 week ago',
    decisionsCount: 142,
    description: 'Musculoskeletal health specialist',
    recentDecisions: [
      'Assessed joint mobility scores',
      'Recommended strength training adjustments',
      'Evaluated bone density trends',
    ],
  },
  {
    id: 'pulmonologist',
    name: 'Pulmonologist Agent',
    tier: 2,
    status: 'idle',
    lastRun: '2 weeks ago',
    decisionsCount: 98,
    description: 'Respiratory system specialist',
    recentDecisions: [
      'Monitored oxygen saturation',
      'Assessed breathing efficiency',
      'Recommended breathing exercises',
    ],
  },
  {
    id: 'nephrologist',
    name: 'Nephrologist Agent',
    tier: 2,
    status: 'active',
    lastRun: '3 hours ago',
    decisionsCount: 167,
    description: 'Kidney and urinary health specialist',
    recentDecisions: [
      'Monitored kidney function markers',
      'Adjusted hydration protocol',
      'Recommended electrolyte balance',
    ],
  },
  // Tier 3: Lifestyle (5 agents)
  {
    id: 'sleep-coach',
    name: 'Sleep Coach Agent',
    tier: 3,
    status: 'active',
    lastRun: '1 hour ago',
    decisionsCount: 487,
    description: 'Sleep quality and optimization',
    recentDecisions: [
      'Optimized bedroom temperature schedule',
      'Adjusted bedtime protocol',
      'Analyzed sleep stage distribution',
    ],
  },
  {
    id: 'stress-mgmt',
    name: 'Stress Management Agent',
    tier: 3,
    status: 'active',
    lastRun: '2 hours ago',
    decisionsCount: 523,
    description: 'Stress reduction and cortisol management',
    recentDecisions: [
      'Recommended meditation protocols',
      'Adjusted daily schedule for recovery',
      'Suggested stress-relief supplements',
    ],
  },
  {
    id: 'longevity',
    name: 'Longevity Agent',
    tier: 3,
    status: 'running',
    lastRun: 'Now',
    decisionsCount: 612,
    description: 'Long-term health and aging optimization',
    recentDecisions: [
      'Reviewed senescent cell markers',
      'Recommended NAD+ precursors',
      'Assessed epigenetic aging factors',
    ],
  },
  {
    id: 'social-wellness',
    name: 'Social Wellness Agent',
    tier: 3,
    status: 'idle',
    lastRun: '5 days ago',
    decisionsCount: 234,
    description: 'Social connection and mental health',
    recentDecisions: [
      'Scheduled community activities',
      'Recommended social engagement goals',
      'Monitored mood patterns',
    ],
  },
  {
    id: 'cognitive-enhancement',
    name: 'Cognitive Enhancement Agent',
    tier: 3,
    status: 'active',
    lastRun: '3 hours ago',
    decisionsCount: 445,
    description: 'Cognitive performance optimization',
    recentDecisions: [
      'Recommended focus-enhancing supplements',
      'Optimized learning schedule',
      'Suggested cognitive exercises',
    ],
  },
  // Tier 4: Executors
  {
    id: 'nutritionist',
    name: 'Nutritionist Agent',
    tier: 4,
    status: 'active',
    lastRun: '2 hours ago',
    decisionsCount: 856,
    description: 'Meal planning and nutritional optimization',
    recentDecisions: [
      'Adjusted macro ratios for goals',
      'Recommended seasonal produce',
      'Optimized nutrient timing',
    ],
  },
  {
    id: 'fitness-coach',
    name: 'Fitness Coach Agent',
    tier: 4,
    status: 'active',
    lastRun: '1 hour ago',
    decisionsCount: 734,
    description: 'Exercise programming and optimization',
    recentDecisions: [
      'Updated strength training program',
      'Adjusted cardio intensity',
      'Recommended recovery days',
    ],
  },
  // Tier 5: Operations (4 agents)
  {
    id: 'dispatcher',
    name: 'Dispatcher Agent',
    tier: 5,
    status: 'running',
    lastRun: 'Now',
    decisionsCount: 2145,
    description: 'Coordinates communication between all agents',
    recentDecisions: [
      'Routed cardiologist recommendations',
      'Prioritized urgent alerts',
      'Coordinated inter-agent discussions',
    ],
  },
  {
    id: 'inventory',
    name: 'Inventory Agent',
    tier: 5,
    status: 'active',
    lastRun: '30 minutes ago',
    decisionsCount: 567,
    description: 'Supplement and resource management',
    recentDecisions: [
      'Restocked low vitamin D supplies',
      'Ordered testing kits',
      'Tracked supplement expiration',
    ],
  },
  {
    id: 'concierge',
    name: 'Concierge Agent',
    tier: 5,
    status: 'idle',
    lastRun: '12 hours ago',
    decisionsCount: 892,
    description: 'User interface and support',
    recentDecisions: [
      'Answered health FAQs',
      'Scheduled appointments',
      'Processed user requests',
    ],
  },
  {
    id: 'finance',
    name: 'Finance Agent',
    tier: 5,
    status: 'idle',
    lastRun: '1 day ago',
    decisionsCount: 145,
    description: 'Cost optimization and budget management',
    recentDecisions: [
      'Optimized supplement budget',
      'Identified cost-effective alternatives',
      'Tracked health expenses',
    ],
  },
  // Tier 6: IT (4 agents)
  {
    id: 'support',
    name: 'Technical Support Agent',
    tier: 6,
    status: 'idle',
    lastRun: '8 hours ago',
    decisionsCount: 423,
    description: 'System troubleshooting and support',
    recentDecisions: [
      'Resolved wearable sync issues',
      'Fixed data import errors',
      'Optimized system performance',
    ],
  },
  {
    id: 'ux',
    name: 'UX/Design Agent',
    tier: 6,
    status: 'idle',
    lastRun: '2 days ago',
    decisionsCount: 267,
    description: 'User experience optimization',
    recentDecisions: [
      'Improved dashboard layout',
      'Simplified data visualization',
      'Enhanced mobile interface',
    ],
  },
  {
    id: 'developer',
    name: 'Developer Agent',
    tier: 6,
    status: 'idle',
    lastRun: '3 days ago',
    decisionsCount: 612,
    description: 'System development and architecture',
    recentDecisions: [
      'Implemented new data encryption',
      'Optimized API performance',
      'Deployed security patches',
    ],
  },
  {
    id: 'qa',
    name: 'QA Agent',
    tier: 6,
    status: 'idle',
    lastRun: '4 days ago',
    decisionsCount: 834,
    description: 'Quality assurance and testing',
    recentDecisions: [
      'Validated data accuracy',
      'Tested integration workflows',
      'Verified compliance standards',
    ],
  },
];

const TIERS = [
  { level: 1, name: 'Strategic Core', color: 'border-purple-500' },
  { level: 2, name: 'Medical Core', color: 'border-blue-500' },
  { level: 3, name: 'Lifestyle', color: 'border-emerald-500' },
  { level: 4, name: 'Executors', color: 'border-amber-500' },
  { level: 5, name: 'Operations', color: 'border-orange-500' },
  { level: 6, name: 'IT', color: 'border-cyan-500' },
];

export default function AgentsPage() {
  const [expandedTier, setExpandedTier] = useState<number | null>(1);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400';
      case 'idle':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800/50 dark:text-gray-400';
      case 'running':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 animate-pulse';
      default:
        return '';
    }
  };

  const getStatusDot = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-emerald-500';
      case 'running':
        return 'bg-blue-500 animate-pulse';
      default:
        return 'bg-gray-400';
    }
  };

  const groupedAgents = TIERS.map(tier => ({
    ...tier,
    agents: MOCK_AGENTS.filter(a => a.tier === tier.level),
  }));

  const MOCK_ACTIVITY_LOG = [
    { timestamp: '2 mins ago', action: 'Data Analyst completed trend analysis', type: 'analysis' },
    { timestamp: '15 mins ago', action: 'Dispatcher coordinated 3 inter-agent discussions', type: 'coordination' },
    { timestamp: '1 hour ago', action: 'Longevity Agent updated aging assessment', type: 'update' },
    { timestamp: '1 hour ago', action: 'Fitness Coach adjusted exercise program', type: 'adjustment' },
    { timestamp: '2 hours ago', action: 'Nutritionist recommended new meal plan', type: 'recommendation' },
    { timestamp: '2 hours ago', action: 'Sleep Coach optimized sleep protocol', type: 'optimization' },
    { timestamp: '3 hours ago', action: 'Endocrinologist reviewed hormone levels', type: 'review' },
    { timestamp: '4 hours ago', action: 'Cognitive Enhancement Agent suggested nootropics', type: 'suggestion' },
    { timestamp: '5 hours ago', action: 'System Biologist identified gut-brain axis effect', type: 'discovery' },
    { timestamp: '6 hours ago', action: 'Chief Medical Officer approved new protocol', type: 'approval' },
    { timestamp: '8 hours ago', action: 'Inventory Agent restocked supplements', type: 'inventory' },
    { timestamp: '12 hours ago', action: 'Data Verifier flagged inconsistent readings', type: 'alert' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Agents</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          27 specialized agents organized in 6 tiers managing your longevity
        </p>
      </div>

      {/* Agent Hierarchy Visualization */}
      <Card>
        <CardHeader>
          <CardTitle>Agent Hierarchy</CardTitle>
          <CardDescription>6-tier system architecture with {MOCK_AGENTS.length} specialized agents</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {groupedAgents.map(tier => (
            <div key={tier.level} className="border-l-4 border-gray-200 dark:border-gray-700 pl-4">
              <button
                onClick={() => setExpandedTier(expandedTier === tier.level ? null : tier.level)}
                className="flex items-center gap-3 w-full p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
              >
                {expandedTier === tier.level ? (
                  <ChevronDown size={20} className="text-emerald-600 dark:text-emerald-400" />
                ) : (
                  <ChevronRight size={20} className="text-gray-600 dark:text-gray-400" />
                )}
                <div className="flex-1 text-left">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    Tier {tier.level}: {tier.name}
                  </h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {tier.agents.length} agent{tier.agents.length !== 1 ? 's' : ''}
                  </p>
                </div>
                <div className="flex gap-2">
                  {tier.agents.map(agent => (
                    <div
                      key={agent.id}
                      className={`w-2 h-2 rounded-full ${getStatusDot(agent.status)}`}
                    />
                  ))}
                </div>
              </button>

              {expandedTier === tier.level && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-3 ml-2">
                  {tier.agents.map(agent => (
                    <button
                      key={agent.id}
                      onClick={() => setSelectedAgent(agent)}
                      className="p-3 rounded-lg border-2 border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-400 text-left transition-colors bg-white dark:bg-gray-800/50"
                    >
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <h4 className="font-medium text-sm text-gray-900 dark:text-white">
                          {agent.name}
                        </h4>
                        <div className={`w-2 h-2 rounded-full mt-1 flex-shrink-0 ${getStatusDot(agent.status)}`} />
                      </div>
                      <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
                        {agent.description}
                      </p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-gray-500 dark:text-gray-500">
                        <Badge variant="outline" className="text-xs">
                          {agent.status}
                        </Badge>
                        <span>{agent.decisionsCount} decisions</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Selected Agent Details */}
      {selectedAgent && (
        <Card>
          <CardHeader className="flex flex-row items-start justify-between">
            <div className="flex-1">
              <CardTitle className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${getStatusDot(selectedAgent.status)}`} />
                {selectedAgent.name}
              </CardTitle>
              <CardDescription className="mt-2">
                Tier {selectedAgent.tier} • {selectedAgent.description}
              </CardDescription>
            </div>
            <Badge className={getStatusColor(selectedAgent.status)}>
              {selectedAgent.status}
            </Badge>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="decisions">Recent Decisions</TabsTrigger>
                <TabsTrigger value="metrics">Metrics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-4 mt-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold">
                      Status
                    </p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white mt-2 capitalize">
                      {selectedAgent.status}
                    </p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold flex items-center gap-2">
                      <Clock size={14} />
                      Last Run
                    </p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white mt-2">
                      {selectedAgent.lastRun}
                    </p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 dark:text-gray-400 uppercase font-semibold">
                      Decisions
                    </p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white mt-2">
                      {selectedAgent.decisionsCount}
                    </p>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="decisions" className="space-y-3 mt-4">
                {selectedAgent.recentDecisions.map((decision, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700"
                  >
                    <p className="text-sm text-gray-900 dark:text-white">
                      • {decision}
                    </p>
                  </div>
                ))}
              </TabsContent>

              <TabsContent value="metrics" className="space-y-3 mt-4">
                <div className="space-y-2">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    Total Decisions: {selectedAgent.decisionsCount}
                  </p>
                  <div className="bg-gray-200 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-600 h-full rounded-full"
                      style={{
                        width: `${(selectedAgent.decisionsCount / 2000) * 100}%`,
                      }}
                    />
                  </div>
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Participation: {((selectedAgent.decisionsCount / 25000) * 100).toFixed(1)}% of total system decisions
                </p>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Activity Log */}
      <Card>
        <CardHeader>
          <CardTitle>Activity Log</CardTitle>
          <CardDescription>Recent agent activities and decisions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {MOCK_ACTIVITY_LOG.map((log, idx) => (
              <div
                key={idx}
                className="flex items-start gap-4 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex-shrink-0">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-white">
                    {log.action}
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                    {log.timestamp}
                  </p>
                </div>
                <Badge variant="outline" className="text-xs flex-shrink-0 capitalize">
                  {log.type}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
