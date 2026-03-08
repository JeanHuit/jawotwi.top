/** @type {import('eslint').Linter.Config} */
export default {
  extends: [
    'eslint:recommended',
    'plugin:astro/recommended',
    'plugin:jsx-a11y/recommended',
  ],
  overrides: [
    {
      files: ['*.astro'],
      parser: 'astro-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser',
        extraFileExtensions: ['.astro'],
      },
      rules: {
        'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      },
    },
    {
      files: ['*.astro/*.js', '*.astro/*.ts'],
      parser: '@typescript-eslint/parser',
      rules: {
        'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      },
    },
  ],
  root: true,
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  ignorePatterns: ['dist/', 'node_modules/', '*.md'],
};
