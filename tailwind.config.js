/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,js}"],
  theme: {
    
    extend: {
      boxShadow: {
        'card-shadow': '2px 6px 20px rgba(0, 0, 0, 0.5)',
      },
      fontFamily: {
        'sans': ['Inter', 'Helvetica', 'Arial', 'sans-serif'],
      },
      colors: {
        primary: '#C44E00',
        primary_hover: '#993D00',
        card_bg: '#fdf3eb',
        page_bg: '#ff9ba6',
        button_bg: '#efe1de',
        button_bg_hover: '#dec1ba',
        primary: '#c34e00',
        primary_hover: '#993d00',
      }
    },
  },
  plugins: [],
}
