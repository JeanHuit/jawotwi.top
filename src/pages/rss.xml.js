import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export const GET = async (context) => {
  const musings = await getCollection('musings', ({ data }) => {
    return !data.draft;
  });

  const sortedMusings = musings.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  return rss({
    title: 'John Awotwi - Musings',
    description: 'Thoughts, ideas, and reflections on technology, life, and everything in between.',
    site: context.site,
    items: sortedMusings.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description || post.data.excerpt || '',
      link: `/musings/${post.slug}/`,
      author: post.data.author || 'John Awotwi',
    })),
    customData: `<language>en-us</language>`,
  });
};
