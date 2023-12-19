# /bin/zsh run_scrapping.sh
QUERY='Chartered Accountant in guelph'
TOTAL=500

conda activate b2bleadsemailscraper
pip install -r requirements.txt
playwright install chromium
python3 maps_scraper.py -s=$QUERY -t=$TOTAL
python3 email_parser.py -s=$QUERY -t=$TOTAL