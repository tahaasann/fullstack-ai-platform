import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getLesson, completeLesson, updateLessonTime } from '../api/client';

export function useLesson(lessonId: string) {
  const queryClient = useQueryClient();

  const { data: lesson, isLoading, error } = useQuery({
    queryKey: ['lesson', lessonId],
    queryFn: () => getLesson(lessonId),
    enabled: !!lessonId,
  });

  const completeMutation = useMutation({
    mutationFn: () => completeLesson(lessonId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lesson', lessonId] });
      queryClient.invalidateQueries({ queryKey: ['progress'] });
    },
  });

  const updateTimeMutation = useMutation({
    mutationFn: (seconds: number) => updateLessonTime(lessonId, seconds),
  });

  return { lesson, isLoading, error, completeMutation, updateTimeMutation };
}
