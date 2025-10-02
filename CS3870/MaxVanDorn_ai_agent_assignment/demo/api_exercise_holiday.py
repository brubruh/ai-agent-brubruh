import requests
import json
from datetime import datetime

def get_public_holidays(country_code="US", year=2024):
    """
    Get public holidays for a specific country and year
    Uses Nager.Date API (free, no key required)
    """
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        holidays = response.json()
        return holidays
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Test with 3 different countries
countries = ['US', 'CA', 'GB']
country_names = {'US': 'United States', 'CA': 'Canada', 'GB': 'United Kingdom'}
holiday_data = {}

print("=== PUBLIC HOLIDAYS 2024 ===\n")

for country in countries:
    print(f"Fetching holidays for {country_names[country]} ({country})...")
    holidays = get_public_holidays(country)
    
    if holidays:
        holiday_data[country] = holidays
        print(f"✓ Successfully retrieved {len(holidays)} holidays\n")
        
        # Extract and print holiday names and dates
        print(f"--- {country_names[country]} Holidays ---")
        for holiday in holidays:
            date = holiday.get('date', 'Unknown date')
            name = holiday.get('name', 'Unknown holiday')
            # Format date for better readability
            try:
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')
            except:
                formatted_date = date
            print(f"  {formatted_date}: {name}")
        print()
    else:
        print(f"✗ Failed to retrieve holidays for {country_names[country]}\n")
        holiday_data[country] = []

# Create summary comparing holiday counts by country
print("=== HOLIDAY COUNT SUMMARY ===")
print(f"{'Country':<15} {'Code':<6} {'Count':<6}")
print("-" * 30)

total_holidays = 0
for country in countries:
    count = len(holiday_data.get(country, []))
    total_holidays += count
    print(f"{country_names[country]:<15} {country:<6} {count:<6}")

print("-" * 30)
print(f"{'TOTAL':<15} {'':6} {total_holidays:<6}")

# Find country with most/least holidays
if holiday_data:
    max_country = max(countries, key=lambda c: len(holiday_data.get(c, [])))
    min_country = min(countries, key=lambda c: len(holiday_data.get(c, [])))
    
    max_count = len(holiday_data.get(max_country, []))
    min_count = len(holiday_data.get(min_country, []))
    
    print(f"\n📊 Analysis:")
    print(f"  Most holidays: {country_names[max_country]} ({max_count} holidays)")
    print(f"  Least holidays: {country_names[min_country]} ({min_count} holidays)")
    
    if max_count > 0:
        avg_holidays = total_holidays / len([c for c in countries if holiday_data.get(c)])
        print(f"  Average: {avg_holidays:.1f} holidays per country")

# Save detailed data to JSON file
try:
    output_data = {
        'summary': {
            'total_countries': len(countries),
            'total_holidays': total_holidays,
            'year': 2024
        },
        'countries': {}
    }
    
    for country in countries:
        output_data['countries'][country] = {
            'name': country_names[country],
            'holiday_count': len(holiday_data.get(country, [])),
            'holidays': holiday_data.get(country, [])
        }
    
    with open('holiday_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Detailed data saved to 'holiday_data.json'")
    
except Exception as e:
    print(f"\n❌ Error saving data to file: {e}")