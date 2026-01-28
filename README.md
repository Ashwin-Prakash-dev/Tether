# Tether - P 


Get real-time push notifications on your phone whenever large trades ($100k+) happen on Polymarket prediction markets.


## Why I Built This


A few weeks ago, I came across this article 

https://www.theguardian.com/society/2026/jan/05/us-traders-make-big-profits-betting-on-nicolas-maduro-capture-in-january. 

Whether this was insider information or just luck, I can't say but it made me recognize that large trades on prediction markets can be a signal of information before it reaches mainstream news. 

As someone interested in both economics and geopolitics, I saw Polymarket's large buying/selling activity as a potentially valuable "early-warning system". Rather than manually checking the platform every now and then or subscribing to a special service, I built this tool to automatically notify me whenever significant capital (the threshold which I can choose) moves into a market. The goal is to have real time knowledge of such trades, especially on bets covering major geopolitical events and use this as an additional signal when evaluating investment decisions

## Features

-  **Push notifications** via Pushover when major trades occur
-  **Configurable threshold** (default: $100k USD)
-  **Automatic checking** every 2 minutes
-  **No duplicate alerts** - uses Redis to track seen trades
-  **Runs 24/7 in the cloud** 
-  **Completely free** using Render + cron-job.org

## How It Works

1. External cron service (cron-job.org) hits the `/check` endpoint every 2 minutes
2. App fetches recent large trades from Polymarket's API
3. Checks Redis to see if we've already alerted on each trade
4. Sends Pushover notification for new whale trades
5. Marks trade as seen in Redis (stored for 7 days)

## Setup

### Prerequisites

- GitHub account
- Pushover account (for notifications)
- Render account (for hosting)
- cron-job.org account (for scheduling)

### 1. Get Pushover Credentials

1. Sign up at [pushover.net](https://pushover.net)
2. Note your **User Key** (shown on dashboard)
3. Create a new application/API token
4. Note your **API Token**
5. Install Pushover app on your phone

### 2. Deploy to Render

1. Fork/clone this repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New +"** → **"Web Service"**
4. Connect your repository
5. Configure:
   - **Name:** `polymarket-whale-alerts` (or your choice)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `PUSHOVER_API_TOKEN` = your Pushover API token
   - `PUSHOVER_USER_KEY` = your Pushover user key
   - `REDIS_URL` = (will add in next step)

### 3. Set Up Redis

1. In Render Dashboard, click **"New +"** → **"Redis"**
2. **Name:** `polymarket-redis`
3. Click **"Create Redis"**
4. Copy the **Internal Redis URL** or **External Redis URL**
5. Go back to your web service → Environment tab
6. Add/update `REDIS_URL` with the Redis URL you copied

### 4. Set Up Automated Checking

1. Go to [cron-job.org](https://cron-job.org) and sign up
2. Click **"Create cronjob"**
3. Configure:
   - **Title:** `Polymarket Whale Alerts`
   - **URL:** `https://your-render-app.onrender.com/check` (replace with your actual URL)
   - **Schedule:** Every 2 minutes (or use custom: `*/2 * * * *`)
   - **Method:** GET
   - **Timeout:** 60 seconds (to handle cold starts)
4. Click **"Create cronjob"**
5. Test by clicking **"Execute now"**

## Configuration

Edit these values in `app.py`:

```python
MIN_CASH_USD = 100_000        # Minimum trade size to alert on
LOOKBACK_SECONDS = 3600       # How far back to check (1 hour)
SEEN_TTL_SECONDS = 7 * 24 * 3600  # How long to remember trades (7 days)
LIMIT = 200                   # Max trades to fetch per check
```

## API Endpoints

- `GET /health` - Health check
- `GET /check` - Check for new whale trades and send alerts
- `GET /debug` - View recent trades without sending alerts
- `GET /redis-debug` - Debug Redis connection

## Project Structure

```
.
├── app.py           # FastAPI application with endpoints
├── alerts.py        # Pushover notification logic
├── polymarket.py    # Polymarket API integration
├── state.py         # Redis state management
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Tech Stack

- **FastAPI** - Web framework
- **Redis** - Track seen trades (prevent duplicates)
- **Pushover** - Push notifications
- **Render** - Cloud hosting (free tier)
- **cron-job.org** - Scheduled execution (free)
- **Polymarket API** - Trade data


