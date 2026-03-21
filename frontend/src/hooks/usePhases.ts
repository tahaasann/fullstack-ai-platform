import { useQuery } from '@tanstack/react-query';
import { getPhases } from '../api/client';

export function usePhases() {
  return useQuery({
    queryKey: ['phases'],
    queryFn: getPhases,
    staleTime: 10 * 60 * 1000, // phases rarely change
  });
}
