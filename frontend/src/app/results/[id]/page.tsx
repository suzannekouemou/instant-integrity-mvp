'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { StatusBadge } from '@/components/ui/Badge';
import { Alert } from '@/components/ui/Alert';
import { LoadingSpinner } from '@/components/ui/Loading';
import { formatDate, formatConfidence } from '@/lib/utils';
import { api } from '@/lib/api';
import type { ResultResponse } from '@/types';
import { 
  ArrowLeft, 
  CheckCircle, 
  AlertTriangle, 
  HelpCircle,
  Calendar,
  Cpu,
  BarChart3,
  FileText
} from 'lucide-react';

export default function ResultDetailPage() {
  return (
    <AuthGuard>
      <ResultDetailContent />
    </AuthGuard>
  );
}

function ResultDetailContent() {
  const params = useParams();
  const sampleId = params.id as string;
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadResult = async () => {
      setIsLoading(true);
      try {
        // Try to fetch from API first
        const data = await api.getResult(sampleId);
        setResult(data);
      } catch (err) {
        // Fall back to local storage
        const stored = localStorage.getItem('recent_results');
        if (stored) {
          const results: ResultResponse[] = JSON.parse(stored);
          const found = results.find(r => r.sample_id === sampleId);
          if (found) {
            setResult(found);
          } else {
            setError('Result not found');
          }
        } else {
          setError(err instanceof Error ? err.message : 'Failed to load result');
        }
      } finally {
        setIsLoading(false);
      }
    };

    if (sampleId) {
      loadResult();
    }
  }, [sampleId]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'authentic':
        return <CheckCircle className="h-8 w-8 text-green-600" />;
      case 'suspect':
        return <AlertTriangle className="h-8 w-8 text-red-600" />;
      default:
        return <HelpCircle className="h-8 w-8 text-yellow-600" />;
    }
  };

  const getStatusMessage = (status: string) => {
    switch (status) {
      case 'authentic':
        return 'This sample appears to be authentic based on spectral analysis.';
      case 'suspect':
        return 'This sample shows signs of potential adulteration or non-conformity.';
      default:
        return 'The analysis was inconclusive. Additional testing may be required.';
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Alert type="error" message={error || 'Result not found'} className="mb-4" />
        <Link href="/results">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Results
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link href="/results" className="inline-block mb-6">
        <Button variant="ghost" size="sm">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Results
        </Button>
      </Link>

      {/* Main Result Card */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row md:items-center gap-6">
            {/* Status Icon */}
            <div className={`p-4 rounded-full ${
              result.status === 'authentic' ? 'bg-green-100' :
              result.status === 'suspect' ? 'bg-red-100' : 'bg-yellow-100'
            }`}>
              {getStatusIcon(result.status)}
            </div>

            {/* Status Info */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-2xl font-bold text-gray-900 capitalize">
                  {result.status}
                </h1>
                <StatusBadge status={result.status} />
              </div>
              <p className="text-gray-600">{getStatusMessage(result.status)}</p>
            </div>

            {/* Confidence Score */}
            <div className="text-center md:text-right">
              <div className="text-3xl font-bold text-gray-900">
                {formatConfidence(result.confidence)}
              </div>
              <p className="text-sm text-gray-500">Confidence Score</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Details Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Sample Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-gray-500" />
              Sample Information
            </CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="space-y-4">
              <div>
                <dt className="text-sm text-gray-500">Sample ID</dt>
                <dd className="text-sm font-mono text-gray-900 break-all">
                  {result.sample_id}
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">Result ID</dt>
                <dd className="text-sm font-mono text-gray-900 break-all">
                  {result.id}
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        {/* Analysis Details */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-gray-500" />
              Analysis Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="space-y-4">
              <div className="flex items-center gap-3">
                <Cpu className="h-5 w-5 text-gray-400" />
                <div>
                  <dt className="text-sm text-gray-500">Model Version</dt>
                  <dd className="text-sm font-medium text-gray-900">{result.model_version}</dd>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-gray-400" />
                <div>
                  <dt className="text-sm text-gray-500">Analyzed</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {formatDate(result.created_at)}
                  </dd>
                </div>
              </div>
            </dl>
          </CardContent>
        </Card>
      </div>

      {/* Summary */}
      {result.summary && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 whitespace-pre-wrap">{result.summary}</p>
          </CardContent>
        </Card>
      )}

      {/* Confidence Meter */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Confidence Level</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <div>
                <span className="text-xs font-semibold inline-block text-gray-600">
                  {result.confidence < 0.5 ? 'Low' : result.confidence < 0.8 ? 'Medium' : 'High'}
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block text-gray-900">
                  {formatConfidence(result.confidence)}
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-3 text-xs flex rounded-full bg-gray-200">
              <div
                style={{ width: `${result.confidence * 100}%` }}
                className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center transition-all duration-500 ${
                  result.status === 'authentic' ? 'bg-green-500' :
                  result.status === 'suspect' ? 'bg-red-500' : 'bg-yellow-500'
                }`}
              ></div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
