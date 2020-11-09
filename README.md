# Carrier247 mobile numbers parser
## What can it do?
Group mobile phone numbers with operators associated with these numbers by using [Carrier247](https://www.data247.com/services/main) API by [data247](https://www.data247.com/)
## Usage
1. Put mobile numbers to numbers.txt
2. Create .env file and add ```API_KEY=YOUR_API_KEY``` inside
3. Run ```__main__.py``` from terminal with argument of iso code of country like DK, GB, AE (case insensitive)
4. Mobile numbers sorted by carrier names saved to ```{iso_code}-response-{current_date}({current_time}).json``` in the same directory
