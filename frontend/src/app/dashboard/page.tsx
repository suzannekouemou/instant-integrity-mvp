'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { StatusBadge } from '@/components/ui/Badge';
import { formatDate, formatConfidence } from '@/lib/utils';
import { api } from '@/lib/api';
import type { ResultResponse } from '@/types';
import { 
  Upload, 
  CheckCircle, 
  AlertTriangle, 
  HelpCircle,
  TrendingUp,
  FileText,
  ArrowRight
} from 'lucide-react';

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}

function DashboardContent() {
  const [recentResults, setRecentResults] = useState<ResultResponse[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    authentic: 0,
    suspect: 0,
    inconclusive: 0,
  });

  useEffect(() => {
    const loadData = async () => {
      const results = await api.getRecentResults(10);
      setRecentResults(results);
      
      // Calculate stats
      const total = results.length;
      const authentic = results.filter(r => r.status === 'authentic').length;
      const suspect = results.filter(r => r.status === 'suspect').length;
      const inconclusive = results.filter(r => r.status === 'inconclusive').length;
      
      setStats({ total, authentic, suspect, inconclusive });
    };
    loadData();
  }, []);

  const statCards = [
    { title: 'Total Samples', value: stats.total, icon: FileText, color: 'text-blue-600 bg-blue-50' },
    { title: 'Authentic', value: stats.authentic, icon: CheckCircle, color: 'text-green-600 bg-green-50' },
    { title: 'Suspect', value: stats.suspect, icon: AlertTriangle, color: 'text-red-600 bg-red-50' },
    { title: 'Inconclusive', value: stats.inconclusive, icon: HelpCircle, color: 'text-yellow-600 bg-yellow-50' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Overview of your authenticity verification results</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${stat.color}`}>
                  <stat.icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-4 mb-8">
        <Card className="hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Upload className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Upload New Sample</h3>
                  <p className="text-sm text-gray-500">Analyze spectral data for authenticity</p>
                </div>
              </div>
              <Link href="/upload">
                <Button>
                  Upload <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">View All Results</h3>
                  <p className="text-sm text-gray-500">Browse and filter analysis history</p>
                </div>
              </div>
              <Link href="/results">
                <Button variant="outline">
                  View <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Results */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Recent Results</CardTitle>
            <Link href="/results" className="text-sm text-blue-600 hover:text-blue-700">
              View all →
            </Link>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {recentResults.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No results yet. Upload your first sample to get started!</p>
              <Link href="/upload">
                <Button className="mt-4">Upload Sample</Button>
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {recentResults.slice(0, 5).map((result) => (
                <Link
                  key={result.id}
                  href={`/results/${result.sample_id}`}
                  className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <StatusBadge status={result.status} />
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        Sample {result.sample_id.slice(0, 8)}...
                      </p>
                      <p className="text-sm text-gray-500">
                        {formatDate(result.created_at)}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      {formatConfidence(result.confidence)}
                    </p>
                    <p className="text-xs text-gray-500">confidence</p>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
