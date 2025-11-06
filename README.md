# 📱 Telegram Tracker

Automated Telegram channel monitoring tool for keyword-based message filtering with webhook delivery.

## 🚀 Features

- **Multi-channel monitoring** - Track multiple Telegram channels simultaneously
- **Flexible keyword configuration** - Different keyword sets for each channel
- **Complete time coverage** - Search through ALL messages within specified time period (not just last 50)
- **Automatic delivery** - Found messages are automatically sent to webhook
- **Configurable intervals** - Flexible polling frequency settings

## 📋 How it works

1. **Telegram API connection** via Telethon library
2. **Message retrieval** - Fetch messages from last N hours from specified channels
3. **Keyword filtering** - Search for messages containing specified keywords
4. **Result delivery** - Send found messages to configured webhook (Make.com)

## ⚙️ Installation and Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Telegram API keys

1. Go to https://my.telegram.org/apps
2. Create a new application
3. Get your `API_ID` and `API_HASH`

### 3. Configure environment variables

Create `.env` file in project root:

```env
# Telegram API credentials
API_ID=your_api_id_here
API_HASH=your_api_hash_here

# Make webhook URL
MAKE_WEBHOOK_URL=https://hook.eu1.make.com/your_webhook_url_here

# Channels to monitor (comma-separated)
CHANNELS=@channel1,@channel2,@channel3

# Keywords for different channels
# Format: KEYWORDS_channelname=keyword1,keyword2,keyword3
KEYWORDS_channel1=news,announcement,important
KEYWORDS_channel2=sale,buy,exchange
KEYWORDS_channel3=job,vacancy,resume

# Check interval in hours (default: 8)
CHECK_INTERVAL_HOURS=8
```

### 4. Initialize Telegram session

```bash
python src/init_session.py
```

On first run you'll need to:
- Enter your phone number
- Enter confirmation code from SMS
- Enter 2FA password if enabled

### 5. Run the script

```bash
python src/main.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_ID` | Telegram application ID | `12345678` |
| `API_HASH` | Telegram application hash | `abcdef1234567890` |
| `MAKE_WEBHOOK_URL` | Webhook URL for result delivery | `https://hook.eu1.make.com/xxx` |
| `CHANNELS` | List of channels to monitor | `@channel1,@channel2` |
| `KEYWORDS_*` | Keywords for channels | `KEYWORDS_channel1=word1,word2` |
| `CHECK_INTERVAL_HOURS` | Check interval in hours | `8` |

### Keyword Format

Keywords are configured via environment variables in format:
```
KEYWORDS_channel_name=word1,word2,word3
```

Where `channel_name` is the channel name without `@` symbol and in lowercase.

**Example:**
- Channel: `@baraholka_dubai`
- Variable: `KEYWORDS_baraholka_dubai=sale,buy,exchange`

## 📊 Project Structure

```
src/
├── main.py          # Main file with monitoring loop
├── config.py        # Configuration loading from environment variables
├── watcher.py       # Telegram API interaction and message filtering
├── sender.py        # Webhook delivery
├── init_session.py  # Telegram session initialization
└── utils.py         # Utility functions
```

## 🔄 Workflow

1. **Load configuration** from environment variables
2. **Infinite monitoring loop:**
   - For each channel:
     - Fetch all messages from last N hours
     - Filter by keywords
     - Send found messages to webhook
   - Wait for specified interval
3. **Repeat cycle**

## 📝 Data Format

Webhook receives JSON with found message information:

```json
{
  "channel": "@channel_name",
  "id": 123456,
  "text": "Message text with keyword",
  "link": "https://t.me/channel_name/123456",
  "date": "2024-01-01T12:00:00+00:00"
}
```

## 🛠️ Troubleshooting

### Authorization Error
```
Session not authorized. Run initial login first.
```
**Solution:** Run `python src/init_session.py` to initialize session.

### Webhook Error
```
404 Client Error: Not Found for url: https://hook.eu1.make.com/xxx
```
**Solution:** Check `MAKE_WEBHOOK_URL` variable in `.env` file.

### No Messages
```
No keywords configured for @channel
```
**Solution:** Add `KEYWORDS_channelname` variable to `.env` file.

## 📈 Logging

Script outputs detailed information about its operation:

- Number of messages retrieved per period
- Keywords found for each channel
- Number of messages with matches
- Webhook delivery status
- Errors and warnings

## 🔒 Security

- API keys stored in environment variables
- `.env` file added to `.gitignore`
- Telegram session saved locally in `session.session`

## 📄 License

See [LICENSE](LICENSE) file for details.
