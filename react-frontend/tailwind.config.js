/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    './node_modules/preline/preline.js',
  ],
  // enable dark mode via class strategy
  darkMode: 'class',
  plugins: [
    require('@tailwindcss/forms'),
    require('preline/plugin')
  ],
}

