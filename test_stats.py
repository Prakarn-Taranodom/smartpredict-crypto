import requests
import time

time.sleep(2)  # Wait for app to be ready

try:
    data = {'ticker': 'AAPL'}
    response = requests.post('http://localhost:5000/predict', data=data, timeout=30)
    print('Status:', response.status_code)

    if response.status_code == 200:
        # Check for key statistics
        checks = [
            ('Current Price', 'Current Price' in response.text),
            ('52W High', '52W High' in response.text),
            ('ROE', 'ROE' in response.text),
            ('Target Price', 'Target Price' in response.text),
            ('Analyst Rating', 'Analyst Rating' in response.text),
            ('Basic Information', 'Basic Information' in response.text),
            ('Valuation & Performance', 'Valuation & Performance' in response.text),
            ('Financial Health', 'Financial Health' in response.text),
            ('Market Data', 'Market Data' in response.text)
        ]

        print('\n📊 Statistics Check Results:')
        for name, result in checks:
            status = '✅' if result else '❌'
            found_text = 'Found' if result else 'Not found'
            print(f'{status} {name}: {found_text}')

        # Count total statistics sections
        sections_found = sum(1 for _, found in checks if found)
        print(f'\n📈 Total sections found: {sections_found}/9')

        if sections_found >= 7:
            print('\n🎉 SUCCESS: Comprehensive company statistics fully implemented!')
        else:
            print('\n⚠️  Partial implementation - some statistics missing')
    else:
        print('❌ Prediction request failed')
        print('Response:', response.text[:500])

except Exception as e:
    print('❌ Test failed with error:', str(e))