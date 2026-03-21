import { useQuery } from '@tanstack/react-query';
import { getProgressOverview } from '../api/client';

export function useProgress() {
  return useQuery({
    queryKey: ['progress'],
    queryFn: getProgressOverview,
    staleTime: 30 * 1000,
  });
}
