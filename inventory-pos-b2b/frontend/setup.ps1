# Create necessary directories
New-Item -ItemType Directory -Force -Path "src"
New-Item -ItemType Directory -Force -Path "public"
New-Item -ItemType Directory -Force -Path "src/components"
New-Item -ItemType Directory -Force -Path "src/components/layout"
New-Item -ItemType Directory -Force -Path "src/pages"
New-Item -ItemType Directory -Force -Path "src/theme"

# Install dependencies
npm install

# Start the development server
npm start 