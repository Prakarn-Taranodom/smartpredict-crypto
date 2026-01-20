# Finnhub API Setup (รองรับหุ้นไทย + อเมริกา)

## ทำไมใช้ Finnhub?

✅ **รองรับหุ้นไทย** (.BK): AOT.BK, BBL.BK, PTT.BK
✅ **รองรับหุ้นอเมริกา**: AAPL, MSFT, GOOGL
✅ **ฟรี 60 requests/นาที** (1,800 requests/ชั่วโมง)
✅ **ไม่ถูก block** บน Render

## Step 1: Get Free API Key

1. ไป https://finnhub.io/register
2. สมัครด้วย email (ฟรี)
3. Login → Dashboard
4. Copy **API Key** (ตัวอย่าง: `abc123xyz456`)

## Step 2: ตั้งค่าใน Render

1. Render Dashboard → เลือก service `smartpredict-stock`
2. **Environment** → **Add Environment Variable**
3. ตั้งค่า:
   - Key: `FINNHUB_API_KEY`
   - Value: `YOUR_API_KEY_HERE`
4. **Save Changes**
5. Render จะ auto-redeploy (รอ 3-5 นาที)

## Step 3: ทดสอบ

### หุ้นอเมริกา:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- TSLA (Tesla)

### หุ้นไทย:
- AOT.BK (ท่าอากาศยาน)
- BBL.BK (กรุงเทพ)
- PTT.BK (ปตท.)
- CPALL.BK (ซีพี ออลล์)

## API Limits (Free Tier)

- **60 requests/นาที**
- **30 requests/วินาที**
- เพียงพอสำหรับ demo และ testing
- ไม่จำกัดจำนวนหุ้น

## Supported Markets

- 🇺🇸 US Stocks (NYSE, NASDAQ)
- 🇹🇭 Thailand (SET)
- 🇯🇵 Japan
- 🇬🇧 UK
- 🇩🇪 Germany
- และอีกมากมาย

## Troubleshooting

**Error: "FINNHUB_API_KEY not found"**
- ตรวจสอบว่าเพิ่ม environment variable แล้ว
- ตรวจสอบการสะกด: `FINNHUB_API_KEY` (case-sensitive)
- Redeploy หลังเพิ่ม variable

**Error: "No data found for XXX.BK"**
- ตรวจสอบ ticker ให้ถูกต้อง
- ใช้ format: `AOT.BK` (ไม่ใช่ `AOT`)
- ลองค้นหา ticker ที่ https://finnhub.io/

**Error: "API rate limit"**
- Free tier: 60 req/นาที
- รอ 1 นาทีแล้วลองใหม่
- หรือ upgrade เป็น paid plan

## เปรียบเทียบกับ Alpha Vantage

| Feature | Finnhub | Alpha Vantage |
|---------|---------|---------------|
| หุ้นไทย | ✅ รองรับ | ❌ ไม่รองรับ |
| Free Limit | 60/นาที | 25/วัน |
| Markets | 60+ ประเทศ | US เท่านั้น |
| แนะนำ | ✅ ใช้ตัวนี้ | สำหรับ US เท่านั้น |
