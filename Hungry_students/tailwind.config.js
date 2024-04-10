/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily:{
        'custom':["League+Spartan", "sans-serif"]
      },
      colors:{primary:"b6beb8"},
    }
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

