/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        valorant: {
          red: '#ff4655',
          dark: '#0f1923',
          gray: '#ece8e1',
          black: '#111111',
        }
      }
    },
  },
  plugins: [],
}
