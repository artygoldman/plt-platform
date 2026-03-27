export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: string;
  updatedAt: string;
}

export interface UserProfile {
  userId: string;
  dateOfBirth: string;
  gender: 'male' | 'female' | 'other';
  height: number;
  weight: number;
  activityLevel: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
  medicalHistory: string[];
  medications: string[];
  supplements: string[];
  allergens: string[];
  goals: string[];
}

export interface Biomarker {
  id: string;
  userId: string;
  name: string;
  value: number;
  unit: string;
  referenceMin: number;
  referenceMax: number;
  status: 'normal' | 'low' | 'high';
  category: string;
  measuredAt: string;
  nextTestDate?: string;
}

export interface BiomarkerHistory {
  biomarkerId: string;
  measurements: Array<{
    value: number;
    date: string;
    status: 'normal' | 'low' | 'high';
  }>;
  trend: 'improving' | 'stable' | 'declining';
  trendPercentage: number;
}

export interface SystemScore {
  id: string;
  name: string;
  category: string;
  score: number;
  maxScore: number;
  healthStatus: 'excellent' | 'good' | 'fair' | 'poor';
  recommendations: string[];
  lastUpdated: string;
}

export interface DigitalTwin {
  id: string;
  userId: string;
  systemScores: SystemScore[];
  overallScore: number;
  biologicalAge: number;
  chronologicalAge: number;
  riskFactors: string[];
  lifeExpectancy: number;
  predictions: {
    disease: string;
    probability: number;
    yearsUntil: number;
  }[];
  createdAt: string;
  updatedAt: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  role: string;
  level: number;
  specialization: string;
  active: boolean;
  createdAt: string;
}

export interface AgentDecision {
  id: string;
  type: string;
  recommendation: string;
  reasoning: string;
  confidence: number;
  timestamp: string;
}

export interface AgentSession {
  id: string;
  userId: string;
  agentId: string;
  decisions: AgentDecision[];
  status: 'active' | 'completed' | 'paused';
  startedAt: string;
  completedAt?: string;
  summary?: string;
}

export interface ContractItem {
  id: string;
  action: string;
  description: string;
  frequency: string;
  duration: string;
  category: string;
}

export interface DailyContract {
  id: string;
  userId: string;
  date: string;
  items: ContractItem[];
  completed: boolean;
  completedAt?: string;
  score: number;
}

export interface Protocol {
  id: string;
  name: string;
  description: string;
  objective: string;
  duration: string;
  items: {
    name: string;
    description: string;
    frequency: string;
    duration: string;
  }[];
  metrics: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Supplement {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  category: string;
  description?: string;
  sideEffects?: string[];
}

export interface InventoryItem {
  id: string;
  userId: string;
  type: 'supplement' | 'medication' | 'equipment';
  name: string;
  dosage?: string;
  quantity: number;
  unit: string;
  expiryDate: string;
  purchaseDate: string;
  status: 'active' | 'low' | 'expired';
}

export interface ScoreBreakdown {
  category: string;
  score: number;
  weight: number;
  factors: string[];
}

export interface LongevityScore {
  userId: string;
  overallScore: number;
  breakdown: ScoreBreakdown[];
  biologicalAge: number;
  estimatedLifespan: number;
  riskScore: number;
  preventableRisks: Array<{
    risk: string;
    severity: 'low' | 'medium' | 'high';
    recommendation: string;
  }>;
  actionItems: Array<{
    action: string;
    priority: 'low' | 'medium' | 'high';
    expectedImpact: number;
  }>;
  lastUpdated: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}
