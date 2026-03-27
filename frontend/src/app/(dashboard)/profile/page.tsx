'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { User, Lock, Bell, Shield, Trash2, Download, AlertTriangle, Copy, Eye, EyeOff } from 'lucide-react';

interface UserProfile {
  firstName: string;
  lastName: string;
  email: string;
  dateOfBirth: string;
  gender: 'male' | 'female' | 'other';
  avatar: string;
}

interface ConnectedService {
  name: string;
  status: 'connected' | 'not-connected';
  lastSync?: string;
  description: string;
}

const MOCK_USER: UserProfile = {
  firstName: 'John',
  lastName: 'Doe',
  email: 'john.doe@example.com',
  dateOfBirth: '1985-06-15',
  gender: 'male',
  avatar: 'JD',
};

const CONNECTED_SERVICES: ConnectedService[] = [
  {
    name: 'Oura Ring',
    status: 'not-connected',
    description: 'Sleep tracking and recovery metrics',
  },
  {
    name: 'Apple Health',
    status: 'not-connected',
    description: 'Health data from your Apple devices',
  },
  {
    name: 'Anthropic API',
    status: 'connected',
    lastSync: '2 hours ago',
    description: 'AI agent connectivity for analysis',
  },
];

const HEALTH_GOALS = [
  { id: 'longevity', label: 'Extend healthy lifespan', selected: true },
  { id: 'strength', label: 'Increase muscle mass', selected: true },
  { id: 'energy', label: 'Improve energy levels', selected: true },
  { id: 'sleep', label: 'Optimize sleep quality', selected: true },
  { id: 'cognition', label: 'Enhance cognitive function', selected: true },
  { id: 'metabolism', label: 'Optimize metabolism', selected: false },
  { id: 'immunity', label: 'Boost immune function', selected: false },
  { id: 'athletic', label: 'Improve athletic performance', selected: true },
];

export default function ProfilePage() {
  const [user, setUser] = useState<UserProfile>(MOCK_USER);
  const [editedUser, setEditedUser] = useState<UserProfile>(MOCK_USER);
  const [isEditing, setIsEditing] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const [healthGoals, setHealthGoals] = useState(HEALTH_GOALS);
  const [notificationSettings, setNotificationSettings] = useState({
    emailAlerts: true,
    emailWeeklySummary: true,
    emailMonthlyReport: true,
    pushNotifications: true,
    pushAlerts: true,
  });

  const handleSaveProfile = () => {
    setUser(editedUser);
    setIsEditing(false);
  };

  const handleGoalToggle = (id: string) => {
    setHealthGoals(
      healthGoals.map(goal =>
        goal.id === id ? { ...goal, selected: !goal.selected } : goal
      )
    );
  };

  const getAge = () => {
    const today = new Date();
    const birthDate = new Date(user.dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
      age--;
    }
    return age;
  };

  const selectedGoals = healthGoals.filter(g => g.selected).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Profile & Settings</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Manage your account, preferences, and connected services
        </p>
      </div>

      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="profile" className="flex items-center gap-2">
            <User size={16} />
            <span className="hidden sm:inline">Profile</span>
          </TabsTrigger>
          <TabsTrigger value="health" className="flex items-center gap-2">
            <Shield size={16} />
            <span className="hidden sm:inline">Health</span>
          </TabsTrigger>
          <TabsTrigger value="integrations" className="flex items-center gap-2">
            <Lock size={16} />
            <span className="hidden sm:inline">Integrations</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="flex items-center gap-2">
            <Bell size={16} />
            <span className="hidden sm:inline">Notifications</span>
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile" className="space-y-4 mt-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Account Information</CardTitle>
                <CardDescription>Your personal details</CardDescription>
              </div>
              {!isEditing && (
                <Button onClick={() => setIsEditing(true)} variant="outline">
                  Edit Profile
                </Button>
              )}
            </CardHeader>
            <CardContent className="space-y-6">
              {!isEditing ? (
                <div className="space-y-4">
                  <div className="flex items-center gap-6 mb-6">
                    <div className="w-20 h-20 rounded-full bg-emerald-600 flex items-center justify-center text-white text-2xl font-bold">
                      {user.avatar}
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg text-gray-900 dark:text-white">
                        {user.firstName} {user.lastName}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {user.email}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        First Name
                      </p>
                      <p className="text-gray-900 dark:text-white">{user.firstName}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Last Name
                      </p>
                      <p className="text-gray-900 dark:text-white">{user.lastName}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Email
                      </p>
                      <p className="text-gray-900 dark:text-white">{user.email}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Date of Birth
                      </p>
                      <p className="text-gray-900 dark:text-white">
                        {new Date(user.dateOfBirth).toLocaleDateString()} (Age {getAge()})
                      </p>
                    </div>
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Gender
                      </p>
                      <p className="text-gray-900 dark:text-white capitalize">{user.gender}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Member Since
                      </p>
                      <p className="text-gray-900 dark:text-white">January 2024</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        First Name
                      </label>
                      <Input
                        value={editedUser.firstName}
                        onChange={e => setEditedUser({ ...editedUser, firstName: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Last Name
                      </label>
                      <Input
                        value={editedUser.lastName}
                        onChange={e => setEditedUser({ ...editedUser, lastName: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Email
                      </label>
                      <Input
                        type="email"
                        value={editedUser.email}
                        onChange={e => setEditedUser({ ...editedUser, email: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Date of Birth
                      </label>
                      <Input
                        type="date"
                        value={editedUser.dateOfBirth}
                        onChange={e => setEditedUser({ ...editedUser, dateOfBirth: e.target.value })}
                      />
                    </div>
                  </div>
                  <div className="flex gap-3 pt-4">
                    <Button onClick={handleSaveProfile}>Save Changes</Button>
                    <Button
                      variant="outline"
                      onClick={() => {
                        setEditedUser(user);
                        setIsEditing(false);
                      }}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Change Password</CardTitle>
              <CardDescription>Update your account password</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Current Password
                </label>
                <Input type="password" placeholder="••••••••" />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  New Password
                </label>
                <Input type="password" placeholder="••••••••" />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Confirm New Password
                </label>
                <Input type="password" placeholder="••••••••" />
              </div>
              <Button>Update Password</Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Health Goals Tab */}
        <TabsContent value="health" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Health Goals</CardTitle>
              <CardDescription>
                Select your primary health objectives ({selectedGoals}/{healthGoals.length})
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {healthGoals.map(goal => (
                  <div
                    key={goal.id}
                    className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-400 transition-colors cursor-pointer"
                    onClick={() => handleGoalToggle(goal.id)}
                  >
                    <Checkbox
                      checked={goal.selected}
                      onCheckedChange={() => handleGoalToggle(goal.id)}
                    />
                    <label className="flex-1 text-sm font-medium text-gray-900 dark:text-white cursor-pointer">
                      {goal.label}
                    </label>
                  </div>
                ))}
              </div>
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Target Longevity Age</h4>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Desired Healthy Lifespan
                  </label>
                  <div className="flex items-center gap-2">
                    <Input
                      type="number"
                      defaultValue="95"
                      min="70"
                      max="120"
                      className="w-24"
                    />
                    <span className="text-sm text-gray-600 dark:text-gray-400">years old</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations Tab */}
        <TabsContent value="integrations" className="space-y-4 mt-6">
          {CONNECTED_SERVICES.map(service => (
            <Card key={service.name}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {service.name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {service.description}
                    </p>
                    {service.lastSync && (
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                        Last synced: {service.lastSync}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {service.status === 'connected' ? (
                      <>
                        <Badge className="bg-emerald-600 hover:bg-emerald-700">Connected</Badge>
                        <Button size="sm" variant="outline">
                          Disconnect
                        </Button>
                      </>
                    ) : (
                      <>
                        <Badge variant="outline">Not Connected</Badge>
                        <Button size="sm">Connect</Button>
                      </>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          {/* API Key Section */}
          <Card>
            <CardHeader>
              <CardTitle>API Key</CardTitle>
              <CardDescription>
                Secure access to PLT API for integrations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Your API Key
                </label>
                <div className="flex gap-2">
                  <Input
                    type={showApiKey ? 'text' : 'password'}
                    value="plt_api_xxxxxxxxxxxxxxxxxxxxx"
                    readOnly
                    className="font-mono text-sm"
                  />
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setShowApiKey(!showApiKey)}
                  >
                    {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
                  </Button>
                  <Button size="sm" variant="outline">
                    <Copy size={16} />
                  </Button>
                </div>
              </div>
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Keep your API key secret. Do not share it or commit it to version control.
                </AlertDescription>
              </Alert>
              <Button variant="outline">Regenerate Key</Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>
                Manage how and when you receive notifications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Email Notifications</h4>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <Checkbox
                      checked={notificationSettings.emailAlerts}
                      onCheckedChange={checked =>
                        setNotificationSettings({
                          ...notificationSettings,
                          emailAlerts: checked as boolean,
                        })
                      }
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white text-sm">
                        Biomarker Alerts
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        Get notified when biomarkers are out of optimal range
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <Checkbox
                      checked={notificationSettings.emailWeeklySummary}
                      onCheckedChange={checked =>
                        setNotificationSettings({
                          ...notificationSettings,
                          emailWeeklySummary: checked as boolean,
                        })
                      }
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white text-sm">
                        Weekly Summary
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        Receive a summary of your health metrics every Sunday
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <Checkbox
                      checked={notificationSettings.emailMonthlyReport}
                      onCheckedChange={checked =>
                        setNotificationSettings({
                          ...notificationSettings,
                          emailMonthlyReport: checked as boolean,
                        })
                      }
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white text-sm">
                        Monthly Report
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        Detailed monthly health report and recommendations
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Push Notifications</h4>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <Checkbox
                      checked={notificationSettings.pushNotifications}
                      onCheckedChange={checked =>
                        setNotificationSettings({
                          ...notificationSettings,
                          pushNotifications: checked as boolean,
                        })
                      }
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white text-sm">
                        General Notifications
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        Receive push notifications for important updates
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <Checkbox
                      checked={notificationSettings.pushAlerts}
                      onCheckedChange={checked =>
                        setNotificationSettings({
                          ...notificationSettings,
                          pushAlerts: checked as boolean,
                        })
                      }
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white text-sm">
                        Critical Alerts
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        Get urgent alerts for critical health metrics
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <Button>Save Preferences</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Danger Zone */}
      <Card className="border-red-200 dark:border-red-900/50">
        <CardHeader className="bg-red-50 dark:bg-red-900/10">
          <CardTitle className="text-red-600 dark:text-red-400">Danger Zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white">Download Your Data</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Export all your health data in standard formats
              </p>
            </div>
            <Button variant="outline" className="flex-shrink-0">
              <Download size={16} className="mr-2" />
              Download
            </Button>
          </div>

          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Delete Account</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Permanently delete your account and all associated data
                </p>
              </div>
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="destructive" className="flex-shrink-0">
                    <Trash2 size={16} className="mr-2" />
                    Delete Account
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Delete Account</DialogTitle>
                    <DialogDescription>
                      This action cannot be undone. Please type your email address to confirm.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <Input
                      placeholder="Enter your email to confirm"
                      type="email"
                      defaultValue={user.email}
                    />
                    <Alert className="border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-900/50">
                      <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
                      <AlertDescription className="text-red-700 dark:text-red-300">
                        All your data will be permanently deleted and cannot be recovered.
                      </AlertDescription>
                    </Alert>
                    <div className="flex gap-2">
                      <Button variant="destructive" className="flex-1">
                        Delete My Account
                      </Button>
                      <DialogTrigger asChild>
                        <Button variant="outline" className="flex-1">
                          Cancel
                        </Button>
                      </DialogTrigger>
                    </div>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
