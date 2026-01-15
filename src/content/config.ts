import { defineCollection, z } from 'astro:content';

const musingsCollection = defineCollection({
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string().optional(),
    author: z.string().optional(),
    date: z.coerce.date(), // Changed from pubDate to date to match your markdown
    pubDate: z.coerce.date().optional(), // Keep for compatibility if needed
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().optional().default(false),
    heroImage: image().optional(),
    tags: z.array(z.string()).optional(),
    category: z.string().optional(),
    keywords: z.array(z.string()).optional(),
    excerpt: z.string().optional(),
  }),
});

export const collections = {
  musings: musingsCollection
};
