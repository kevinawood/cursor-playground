#!/bin/bash

# RSS Reader Technical Documentation PDF Generator
# This script converts the markdown documentation to PDF

echo "📚 Generating RSS Reader Technical Documentation PDF..."

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc is not installed. Installing..."
    sudo apt update
    sudo apt install -y pandoc texlive-xetex
fi

# Check if we're in the right directory
if [ ! -f "TECHNICAL_DOCUMENTATION.md" ]; then
    echo "❌ TECHNICAL_DOCUMENTATION.md not found in current directory"
    echo "Please run this script from the rss-reader project root"
    exit 1
fi

# Generate PDF
echo "🔄 Converting markdown to PDF..."
pandoc TECHNICAL_DOCUMENTATION.md \
    -o RSS_Reader_Technical_Documentation.pdf \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V mainfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    --toc \
    --toc-depth=3 \
    --highlight-style=tango

if [ $? -eq 0 ]; then
    echo "✅ PDF generated successfully!"
    echo "📄 File: RSS_Reader_Technical_Documentation.pdf"
    echo "📁 Location: $(pwd)/RSS_Reader_Technical_Documentation.pdf"
    
    # Show file size
    file_size=$(du -h RSS_Reader_Technical_Documentation.pdf | cut -f1)
    echo "📊 File size: $file_size"
    
    # Open the PDF if possible
    if command -v xdg-open &> /dev/null; then
        echo "🚀 Opening PDF..."
        xdg-open RSS_Reader_Technical_Documentation.pdf &
    elif command -v open &> /dev/null; then
        echo "🚀 Opening PDF..."
        open RSS_Reader_Technical_Documentation.pdf &
    else
        echo "💡 You can open the PDF manually from the file location above"
    fi
else
    echo "❌ Failed to generate PDF"
    exit 1
fi 