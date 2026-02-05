'use client';

import { useState, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { AuthGuard } from '@/components/AuthGuard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { Alert } from '@/components/ui/Alert';
import { api } from '@/lib/api';
import type { SampleType } from '@/types';
import { Upload, FileSpreadsheet, X } from 'lucide-react';

const uploadSchema = z.object({
  sample_type: z.enum(['flour', 'spice', 'herb', 'other']),
});

type UploadFormData = z.infer<typeof uploadSchema>;

const sampleTypeOptions = [
  { value: 'flour', label: 'Flour' },
  { value: 'spice', label: 'Spice' },
  { value: 'herb', label: 'Herb' },
  { value: 'other', label: 'Other' },
];

export default function UploadPage() {
  return (
    <AuthGuard>
      <UploadContent />
    </AuthGuard>
  );
}

function UploadContent() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UploadFormData>({
    resolver: zodResolver(uploadSchema),
    defaultValues: {
      sample_type: 'flour',
    },
  });

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please upload a CSV file');
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a CSV file');
      }
    }
  };

  const removeFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const onSubmit = async (data: UploadFormData) => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await api.uploadSample(file, data.sample_type as SampleType);
      api.storeResult(result);
      setSuccess('Sample analyzed successfully!');
      
      // Redirect to result page after a short delay
      setTimeout(() => {
        router.push(`/results/${result.sample_id}`);
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Upload Sample</h1>
        <p className="text-gray-500 mt-1">Upload spectral data for authenticity analysis</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Spectral Data Upload</CardTitle>
        </CardHeader>
        <CardContent>
          {error && <Alert type="error" message={error} className="mb-4" />}
          {success && <Alert type="success" message={success} className="mb-4" />}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Sample Type Selector */}
            <Select
              id="sample_type"
              label="Sample Type"
              options={sampleTypeOptions}
              error={errors.sample_type?.message}
              {...register('sample_type')}
            />

            {/* File Upload Area */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CSV File
              </label>
              <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragging
                    ? 'border-blue-500 bg-blue-50'
                    : file
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />

                {file ? (
                  <div className="flex items-center justify-center gap-4">
                    <div className="flex items-center gap-3 bg-white px-4 py-2 rounded-lg border border-gray-200">
                      <FileSpreadsheet className="h-6 w-6 text-green-600" />
                      <div className="text-left">
                        <p className="text-sm font-medium text-gray-900">{file.name}</p>
                        <p className="text-xs text-gray-500">
                          {(file.size / 1024).toFixed(1)} KB
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={removeFile}
                        className="p-1 hover:bg-gray-100 rounded"
                      >
                        <X className="h-4 w-4 text-gray-500" />
                      </button>
                    </div>
                  </div>
                ) : (
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600">
                      <span className="text-blue-600 hover:text-blue-700">Click to upload</span>
                      {' '}or drag and drop
                    </p>
                    <p className="text-sm text-gray-500 mt-1">CSV files only (max 10MB)</p>
                  </label>
                )}
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full"
              size="lg"
              isLoading={isLoading}
              disabled={!file}
            >
              {isLoading ? 'Analyzing...' : 'Analyze Sample'}
            </Button>
          </form>

          {/* Help Text */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="text-sm font-medium text-gray-900 mb-2">CSV Format Requirements:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• First column: Wavenumber values</li>
              <li>• Second column: Absorbance/Intensity values</li>
              <li>• UTF-8 encoding</li>
              <li>• Comma-separated values</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
