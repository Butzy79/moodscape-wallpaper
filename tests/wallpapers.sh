#!/bin/bash

# SETTINGS
PEXELS_API_KEY="YOUR_PEXELS_KEY" # https://www.pexels.com/api
UNSPLASH_ACCESS_KEY="CupGcHluHJVFJb1FaEz5zRSTN3y6KG_KRGXyDM_gSb8" # https://unsplash.com/developers

COUNT=10


# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SOURCE="$1"
DIR="$2"
query="$3"
MODE="$4"

show_help() {
cat << EOF

Wallpaper Downloader by The Best Ricky

Usage:
  $0 <source> <directory> "search query" <resolution>

Sources:
  wallhaven     Download wallpapers from Wallhaven
  pexels        Download photos from Pexels (API key required)
  unsplash      Download photos from Unsplash (API key required)

Resolutions (Wallhaven only):
  1080          At least 1920x1080
  2k            At least 2560x1440
  4k            At least 3840x2160
  wide          16:9 wallpapers
  ultrawide     21:9 wallpapers

Examples:
  $0 wallhaven ./cars "porsche race" 4k
  $0 wallhaven ./cars "ferrari gt3" ultrawide
  $0 pexels ./cars "porsche gt3"
  $0 unsplash ./cars "classic porsche"

Options:
  -h, --help, -?, /?     Show this help

EOF
}

# Help
case "$1" in
    -h|--help|-?|/?)
        show_help
        exit 0
        ;;
esac

if [ -z "$SOURCE" ] || [ -z "$DIR" ] || [ -z "$query" ]; then
    show_help
    exit 1
fi

if [ -z "$SOURCE" ] || [ -z "$DIR" ] || [ -z "$query" ]; then
  echo -e "${RED}Usage:${NC}"
  echo "./wall.sh <wallhaven|pexels|unsplash> <dir> \"query\" [mode]"
  exit 1
fi

mkdir -p "$DIR"
q="${query// /+}"

echo -e "${CYAN}Source:${NC} $SOURCE"
echo -e "${CYAN}Query:${NC} $query"
echo -e "${CYAN}Dir:${NC} $DIR"

#######################################
# WALLHAVEN
#######################################
if [ "$SOURCE" == "wallhaven" ]; then

  RES_FILTER=""

  if [ "$MODE" == "4k" ]; then
    RES_FILTER="&atleast=3840x2160"
  elif [ "$MODE" == "2k" ]; then
    RES_FILTER="&atleast=2560x1440"
  elif [ "$MODE" == "1080" ]; then
    RES_FILTER="&atleast=1920x1080"
  elif [ "$MODE" == "wide" ]; then
    RES_FILTER="&ratios=16x9"
  elif [ "$MODE" == "ultrawide" ]; then
    RES_FILTER="&ratios=landscape&atleast=2560x1080"
  fi

  json=$(curl -s "https://wallhaven.cc/api/v1/search?q=${q}${RES_FILTER}&sorting=relevance&order=desc&purity=100")

  urls=$(echo "$json" | grep -o '"path":"[^"]*"' | head -n $COUNT | cut -d'"' -f4 | sed 's/\\\//\//g')

#######################################
# PEXELS
#######################################
elif [ "$SOURCE" == "pexels" ]; then

  json=$(curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=${q}&per_page=${COUNT}")

  urls=$(echo "$json" | grep -o '"original":"[^"]*"' | cut -d'"' -f4)

#######################################
# UNSPLASH
#######################################
elif [ "$SOURCE" == "unsplash" ]; then

  json=$(curl -s "https://api.unsplash.com/search/photos?query=${q}&per_page=${COUNT}&client_id=${UNSPLASH_ACCESS_KEY}")

  urls=$(echo "$json" | grep -o '"regular":"[^"]*"' | cut -d'"' -f4)

else
  echo -e "${RED}Invalid source: ${SOURCE}${NC}"
  echo "Valid sources:"
  echo "  - wallhaven"
  echo "  - pexels"
  echo "  - unsplash"
  exit 1
fi

#######################################
# DOWNLOAD COMMON
#######################################

i=1
for url in $urls; do
  filename="${DIR}/img_${i}.jpg"

  echo -e "${YELLOW}Downloading:${NC} $url"

  curl -sS --no-progress-meter -L "$url" -o "$filename"

  ((i++))
done

echo -e "${GREEN}Done.${NC} Saved in $DIR"