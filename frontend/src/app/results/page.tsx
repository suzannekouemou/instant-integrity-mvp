'use client';

import { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { AuthGuard } from '@/components/AuthGuard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { StatusBadge } from '@/components/ui/Badge';
import { Alert } from '@/components/ui/Alert';
import { LoadingSpinner } from '@/components/ui/Loading';
import { formatDate, formatConfidence } from '@/lib/utils';
import { api } from '@/lib/api';
import type { ResultResponse } from '@/types';
import { 
  FileText, 
  ChevronLeft, 
  ChevronRight, 
  Filter, 
  ArrowUpDown,
  ArrowLeft, 
  CheckCircle, 
  AlertTriangle, 
  HelpCircle,
  Calendar,
  Cpu,
  BarChart3
} from 'lucide-react';

const statusOptions = [
  { value: 'all', label: 'All Statuses' },
  { value: 'authentic', label: 'Authentic' },
  { value: 'suspect', label: 'Suspect' },
  { value: 'inconclusive', label: 'Inconclusive' },
];

const sortOptions = [
  { value: 'newest', label: 'Newest First' },
  { value: 'oldest', label: 'Oldest First' },
  { value: 'confidence-high', label: 'Highest Confidence' },
  { value: 'confidence-low', label: 'Lowest Confidence' },
];

const ITEMS_PER_PAGE = 10;

export default function ResultsPage() {
  return (
    <AuthGuard>
      <ResultsRouter />
    </AuthGuard>
  );
}

// Router: shows detail view if ?id= present, otherwise list view
function ResultsRouter() {
  const searchParams = useSearchParams();
  const selectedId = searchParams.get('id');

  if (selectedId) {
    return <ResultDetailContent sampleId={selectedId} />;
  }
  return <ResultsListContent />;
}

// Detail View Component
function ResultDetailContent({ sampleId }: { sampleId: string }) {
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadResult = async () => {
      setIsLoading(true);
      try {
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
              result.status === 'authentic' ? 'bg-green-100 dark:bg-green-900/30' :
              result.status === 'suspect' ? 'bg-red-100 dark:bg-red-900/30' : 'bg-yellow-100 dark:bg-yellow-900/30'
            }`}>
              {getStatusIcon(result.status)}
            </div>

            {/* Status Info */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white capitalize">
                  {result.status}
                </h1>
                <StatusBadge status={result.status} />
              </div>
              <p className="text-gray-600 dark:text-gray-400">{getStatusMessage(result.status)}</p>
            </div>

            {/* Confidence Score */}
            <div className="text-center md:text-right">
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {formatConfidence(result.confidence)}
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Confidence Score</p>
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
                <dt className="text-sm text-gray-500 dark:text-gray-400">Sample ID</dt>
                <dd className="text-sm font-mono text-gray-900 dark:text-white break-all">
                  {result.sample_id}
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500 dark:text-gray-400">Result ID</dt>
                <dd className="text-sm font-mono text-gray-900 dark:text-white break-all">
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
                  <dt className="text-sm text-gray-500 dark:text-gray-400">Model Version</dt>
                  <dd className="text-sm font-medium text-gray-900 dark:text-white">{result.model_version}</dd>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-gray-400" />
                <div>
                  <dt className="text-sm text-gray-500 dark:text-gray-400">Analyzed</dt>
                  <dd className="text-sm font-medium text-gray-900 dark:text-white">
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
            <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{result.summary}</p>
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
                <span className="text-xs font-semibold inline-block text-gray-600 dark:text-gray-400">
                  {result.confidence < 0.5 ? 'Low' : result.confidence < 0.8 ? 'Medium' : 'High'}
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block text-gray-900 dark:text-white">
                  {formatConfidence(result.confidence)}
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-3 text-xs flex rounded-full bg-gray-200 dark:bg-gray-700">
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

// List View Component
function ResultsListContent() {
  const [results, setResults] = useState<ResultResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const loadResults = async () => {
      setIsLoading(true);
      const data = await api.getRecentResults(50);
      setResults(data);
      setIsLoading(false);
    };
    loadResults();
  }, []);

  // Filter and sort results
  const filteredResults = useMemo(() => {
    let filtered = [...results];

    // Apply status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter((r) => r.status === statusFilter);
    }

    // Apply sorting
    switch (sortBy) {
      case 'newest':
        filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        break;
      case 'oldest':
        filtered.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        break;
      case 'confidence-high':
        filtered.sort((a, b) => b.confidence - a.confidence);
        break;
      case 'confidence-low':
        filtered.sort((a, b) => a.confidence - b.confidence);
        break;
    }

    return filtered;
  }, [results, statusFilter, sortBy]);

  // Pagination
  const totalPages = Math.ceil(filteredResults.length / ITEMS_PER_PAGE);
  const paginatedResults = filteredResults.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  // Reset to page 1 when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [statusFilter, sortBy]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Analysis Results</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">View and filter your authenticity analysis results</p>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-gray-500" />
              <Select
                id="status-filter"
                options={statusOptions}
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-40"
              />
            </div>
            <div className="flex items-center gap-2">
              <ArrowUpDown className="h-4 w-4 text-gray-500" />
              <Select
                id="sort-by"
                options={sortOptions}
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-44"
              />
            </div>
            <div className="ml-auto text-sm text-gray-500 dark:text-gray-400">
              {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results Table */}
      <Card>
        <CardHeader>
          <CardTitle>Results</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <LoadingSpinner />
          ) : paginatedResults.length === 0 ? (
            <div className="p-8 text-center text-gray-500 dark:text-gray-400">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300 dark:text-gray-600" />
              {results.length === 0 ? (
                <>
                  <p>No results yet. Upload your first sample to get started!</p>
                  <Link href="/upload">
                    <Button className="mt-4">Upload Sample</Button>
                  </Link>
                </>
              ) : (
                <p>No results match your filters.</p>
              )}
            </div>
          ) : (
            <>
              {/* Desktop Table */}
              <div className="hidden md:block overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Sample ID
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Confidence
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Model
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {paginatedResults.map((result) => (
                      <tr key={result.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                          {result.sample_id.slice(0, 8)}...
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <StatusBadge status={result.status} />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                          {formatConfidence(result.confidence)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {result.model_version}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {formatDate(result.created_at)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right">
                          <Link href={`/results?id=${result.sample_id}`}>
                            <Button variant="ghost" size="sm">
                              View
                            </Button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Mobile Cards */}
              <div className="md:hidden divide-y divide-gray-200 dark:divide-gray-700">
                {paginatedResults.map((result) => (
                  <Link
                    key={result.id}
                    href={`/results?id=${result.sample_id}`}
                    className="block p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {result.sample_id.slice(0, 8)}...
                      </span>
                      <StatusBadge status={result.status} />
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                      <span>{formatConfidence(result.confidence)} confidence</span>
                      <span>{formatDate(result.created_at)}</span>
                    </div>
                  </Link>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200 dark:border-gray-700">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Page {currentPage} of {totalPages}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
