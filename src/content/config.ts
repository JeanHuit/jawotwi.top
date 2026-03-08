import { defineCollection, z } from 'astro:content';

const musingsCollection = defineCollection({
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string().optional(),
    author: z.string().optional().default('John Awotwi'),
    // Support both 'date' and 'pubDate' for backwards compatibility
    date: z.coerce.date().optional(),
    pubDate: z.coerce.date().optional(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().optional().default(false),
    heroImage: image().optional(),
    tags: z.array(z.string()).optional().default([]),
    category: z.string().optional(),
    keywords: z.array(z.string()).optional().default([]),
    excerpt: z.string().optional(),
  }).transform((data) => ({
    ...data,
    // Use pubDate if available, otherwise use date
    pubDate: data.pubDate || data.date || new Date(),
  })),
});

const projectsCollection = defineCollection({
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    subtitle: z.string().optional(),
    category: z.string().optional(),
    tags: z.array(z.string()).optional().default([]),
    heroImage: image().optional(),
    featured: z.boolean().optional().default(false),
    url: z.string().url().optional(),
    github: z.string().url().optional(),
  }),
});

const servicesCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    icon: z.string().optional(),
    featured: z.boolean().optional().default(false),
  }),
});

const programsCollection = defineCollection({
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    year: z.string(),
    type: z.enum(['event', 'program', 'workshop', 'initiative']),
    heroImage: image().optional(),
  }),
});

export const collections = {
  musings: musingsCollection,
  projects: projectsCollection,
  services: servicesCollection,
  programs: programsCollection,
};
