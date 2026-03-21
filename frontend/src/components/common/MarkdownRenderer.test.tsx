import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import MarkdownRenderer from './MarkdownRenderer';

describe('MarkdownRenderer', () => {
  it('renders bold text', () => {
    render(<MarkdownRenderer content="**bold text**" />);
    const bold = screen.getByText('bold text');
    expect(bold.tagName).toBe('STRONG');
  });

  it('renders headings', () => {
    render(<MarkdownRenderer content="# Heading 1" />);
    expect(screen.getByText('Heading 1').tagName).toBe('H1');
  });

  it('renders inline code', () => {
    render(<MarkdownRenderer content="Use `console.log`" />);
    expect(screen.getByText('console.log').tagName).toBe('CODE');
  });

  it('renders links with security attributes', () => {
    render(<MarkdownRenderer content="[Link](https://example.com)" />);
    const link = screen.getByText('Link');
    expect(link.getAttribute('target')).toBe('_blank');
    expect(link.getAttribute('rel')).toContain('noopener');
  });

  it('returns null for empty content', () => {
    const { container } = render(<MarkdownRenderer content="" />);
    expect(container.firstChild).toBeNull();
  });
});
