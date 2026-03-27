'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Upload, Cloud, CheckCircle, AlertTriangle, FileText, Link as LinkIcon } from 'lucide-react';

interface RecentUpload {
  id: string;
  fileName: string;
  type: 'pdf' | 'jpg' | 'png';
  status: 'processing' | 'completed' | 'failed';
  uploadDate: string;
  size: string;
}

const MOCK_UPLOADS: RecentUpload[] = [
  {
    id: '1',
    fileName: 'Lab_Results_March_2026.pdf',
    type: 'pdf',
    status: 'completed',
    uploadDate: '2026-03-27',
    size: '2.4 MB',
  },
  {
    id: '2',
    fileName: 'Blood_Test_Scan.jpg',
    type: 'jpg',
    status: 'completed',
    uploadDate: '2026-03-25',
    size: '1.8 MB',
  },
  {
    id: '3',
    fileName: 'Genetic_Report.pdf',
    type: 'pdf',
    status: 'processing',
    uploadDate: '2026-03-27',
    size: '5.2 MB',
  },
];

export default function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showProgress, setShowProgress] = useState(false);
  const [recentUploads, setRecentUploads] = useState<RecentUpload[]>(MOCK_UPLOADS);
  const [manualBiomarkerValue, setManualBiomarkerValue] = useState('');
  const [manualBiomarkerDate, setManualBiomarkerDate] = useState('');

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    setShowProgress(true);
    setUploadProgress(0);

    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + Math.random() * 30;
      });
    }, 300);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setShowProgress(true);
      setUploadProgress(0);

      const interval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + Math.random() * 30;
        });
      }, 300);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400';
      case 'processing':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 animate-pulse';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400';
    }
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return '📄';
      case 'jpg':
      case 'png':
        return '🖼️';
      default:
        return '📁';
    }
  };

  const handleAddBiomarker = () => {
    if (manualBiomarkerValue && manualBiomarkerDate) {
      setManualBiomarkerValue('');
      setManualBiomarkerDate('');
      alert('Biomarker value added successfully!');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Data Upload</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Upload blood tests, connect wearables, or manually enter biomarker values
        </p>
      </div>

      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="upload">Upload Tests</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="manual">Manual Entry</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>

        {/* Upload Tests Tab */}
        <TabsContent value="upload" className="space-y-4 mt-6">
          {/* Drag and Drop Zone */}
          <Card
            className={`transition-all ${
              isDragging
                ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/10 dark:border-emerald-400'
                : 'border-dashed border-2 border-gray-300 dark:border-gray-700'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <CardContent className="p-8">
              <div className="flex flex-col items-center justify-center gap-4">
                <Cloud
                  size={48}
                  className={`${isDragging ? 'text-emerald-600 dark:text-emerald-400' : 'text-gray-400'}`}
                />
                <div className="text-center">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                    Drag and drop blood test files here
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    or click below to select files
                  </p>
                  <div className="flex gap-2 justify-center">
                    <Badge variant="outline">PDF</Badge>
                    <Badge variant="outline">JPG</Badge>
                    <Badge variant="outline">PNG</Badge>
                  </div>
                </div>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.jpg,.png"
                  onChange={handleFileInput}
                  className="hidden"
                  id="file-upload"
                />
                <Button
                  onClick={() => document.getElementById('file-upload')?.click()}
                  className="mt-4"
                >
                  <Upload size={16} className="mr-2" />
                  Select Files
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Upload Progress */}
          {showProgress && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Uploading</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Lab_Results_March_2026.pdf
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {Math.round(uploadProgress)}%
                    </span>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                </div>
              </CardContent>
            </Card>
          )}

          {/* Supported Formats */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Supported File Types</CardTitle>
              <CardDescription>Maximum file size: 10 MB per file</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-start gap-3">
                <FileText className="text-red-500 mt-1" size={20} />
                <div>
                  <p className="font-medium text-gray-900 dark:text-white text-sm">PDF Documents</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    Blood test reports, genetic analysis, lab documents
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-blue-500 mt-1 text-sm">🖼️</div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-white text-sm">Images</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    JPG and PNG scans of test results
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations Tab */}
        <TabsContent value="integrations" className="space-y-4 mt-6">
          {/* Oura Ring */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Oura Ring</span>
                <Badge variant="secondary">Not Connected</Badge>
              </CardTitle>
              <CardDescription>
                Track sleep quality, heart rate variability, and body temperature
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Connect your Oura Ring to automatically sync health metrics including sleep stages,
                recovery scores, and activity data.
              </p>
              <Button className="w-full bg-emerald-600 hover:bg-emerald-700">
                <LinkIcon size={16} className="mr-2" />
                Connect Oura Ring
              </Button>
            </CardContent>
          </Card>

          {/* Apple Health */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Apple Health</span>
                <Badge variant="secondary">Not Connected</Badge>
              </CardTitle>
              <CardDescription>
                Import health data from your Apple ecosystem
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Sync steps, heart rate, blood pressure, sleep data, and other metrics from Apple Health.
              </p>
              <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-400 space-y-2">
                <p>• Available on iOS and macOS</p>
                <p>• Requires Apple Health app</p>
                <p>• Data syncs in real-time</p>
              </div>
              <Button className="w-full" variant="outline">
                <LinkIcon size={16} className="mr-2" />
                Connect Apple Health
              </Button>
            </CardContent>
          </Card>

          {/* Garmin */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Garmin</span>
                <Badge variant="secondary">Coming Soon</Badge>
              </CardTitle>
              <CardDescription>
                Sync Garmin wearable data
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Track fitness metrics, stress levels, and body composition from Garmin devices.
              </p>
              <Button disabled className="w-full">
                Coming Soon
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Manual Entry Tab */}
        <TabsContent value="manual" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Add Biomarker Value</CardTitle>
              <CardDescription>
                Manually enter a biomarker measurement
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Biomarker Name
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
                  <option>Blood Glucose</option>
                  <option>Total Cholesterol</option>
                  <option>LDL Cholesterol</option>
                  <option>HDL Cholesterol</option>
                  <option>Triglycerides</option>
                  <option>Testosterone</option>
                  <option>TSH</option>
                  <option>Vitamin D</option>
                  <option>C-Reactive Protein</option>
                  <option>HbA1c</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Value
                  </label>
                  <Input
                    type="number"
                    placeholder="Enter value"
                    value={manualBiomarkerValue}
                    onChange={e => setManualBiomarkerValue(e.target.value)}
                    step="0.1"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Unit
                  </label>
                  <Input type="text" placeholder="mg/dL" disabled />
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Measurement Date
                </label>
                <Input
                  type="date"
                  value={manualBiomarkerDate}
                  onChange={e => setManualBiomarkerDate(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Notes (Optional)
                </label>
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                  rows={3}
                  placeholder="Add any notes about this measurement..."
                />
              </div>

              <Button
                onClick={handleAddBiomarker}
                disabled={!manualBiomarkerValue || !manualBiomarkerDate}
                className="w-full"
              >
                Add Biomarker Value
              </Button>
            </CardContent>
          </Card>

          <Alert>
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              Manual entries are for reference only. For accurate health decisions, use certified lab tests
              or validated wearable devices.
            </AlertDescription>
          </Alert>
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history" className="space-y-4 mt-6">
          <div className="space-y-3">
            {recentUploads.map(upload => (
              <Card key={upload.id}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3 flex-1">
                      <span className="text-2xl">{getFileIcon(upload.type)}</span>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 dark:text-white truncate">
                          {upload.fileName}
                        </h4>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          Uploaded {upload.uploadDate} • {upload.size}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 flex-shrink-0">
                      <Badge className={getStatusColor(upload.status)}>
                        {upload.status}
                      </Badge>
                      {upload.status === 'completed' && (
                        <CheckCircle className="text-emerald-600 dark:text-emerald-400" size={20} />
                      )}
                      {upload.status === 'processing' && (
                        <div className="animate-spin">⏳</div>
                      )}
                    </div>
                  </div>

                  {upload.status === 'completed' && (
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex gap-2">
                      <Button size="sm" variant="outline">
                        View Report
                      </Button>
                      <Button size="sm" variant="outline">
                        Download
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
