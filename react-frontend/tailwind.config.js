/** @type {import('tailwindcss').Config} */
const {nextui} = require('@nextui-org/theme');

export default {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/preline/preline.js",
    "./node_modules/@nextui-org/theme/dist/components/(avatar|breadcrumbs|button|card|date-picker|divider|dropdown|input|pagination|table|popover|ripple|spinner|calendar|date-input|menu|checkbox|spacer).js"
  ],
  // enable dark mode via class strategy
  darkMode: 'class',
  plugins: [
    require('@tailwindcss/forms'),
    require('preline/plugin'),
    nextui()
  ],
}

