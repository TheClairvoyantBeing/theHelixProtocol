/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './index.html'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        obsidian: {
          900: '#1e1e1e',
          800: '#2d2d2d',
          700: '#363636',
          600: '#404040',
          500: '#525252',
          400: '#737373',
          300: '#a3a3a3',
          200: '#e5e5e5',
          100: '#eeeeee',
          50: '#f5f5f5',
        },
        claude: {
          accent: '#d97757',
          bubble: '#e3e1df',
          darkBubble: '#383635',
        }
      }
    },
  },
  plugins: [],
}
