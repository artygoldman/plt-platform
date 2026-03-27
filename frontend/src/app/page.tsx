import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-background/95">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <Badge className="mb-4">Personal Longevity Team</Badge>
          <h1 className="text-5xl font-bold tracking-tight mb-4">
            Welcome to PLT
          </h1>
          <p className="text-xl text-muted mb-8 max-w-2xl mx-auto">
            Your personal team of AI agents working 24/7 to optimize your health
            and longevity
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/dashboard">
              <Button size="lg">Get Started</Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg">
                Sign In
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Digital Twin</CardTitle>
              <CardDescription>
                AI-powered health model
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted">
                Get a complete digital representation of your health with real-time updates
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Agents</CardTitle>
              <CardDescription>
                27 specialized agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted">
                Expert agents analyzing your biomarkers and providing personalized recommendations
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Longevity Score</CardTitle>
              <CardDescription>
                Predict your lifespan
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted">
                Track your biological age and estimate your remaining healthy years
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
