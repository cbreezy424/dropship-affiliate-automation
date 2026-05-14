# Dropship Affiliate Automation 🎬💰

Automated system to create affiliate videos for dropshipping products and post to social media. Built with free tools and minimal cost.

## Features

✅ **Product Management** - Add products with prices, images, descriptions
✅ **Affiliate Link Integration** - Auto-generate Amazon affiliate links
✅ **AI Script Generation** - Create engaging product scripts automatically
✅ **Video Creation** - Generate videos with images + voiceover
✅ **Social Media Ready** - Formatted for TikTok, Instagram Reels, YouTube Shorts
✅ **Batch Processing** - Create multiple videos at once

## Tech Stack

- **Backend:** Python + Flask
- **Database:** SQLite
- **Video Creation:** FFmpeg
- **Text-to-Speech:** gTTS (Google Text-to-Speech - Free)
- **Script Generation:** Groq API (Free tier available)
- **Frontend:** HTML/CSS + Bootstrap

## Installation

### Prerequisites
```bash
# Python 3.8+
# FFmpeg (install via: brew install ffmpeg on Mac, apt-get install ffmpeg on Linux)
```

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/cbreezy424/dropship-affiliate-automation.git
cd dropship-affiliate-automation
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Get Free API Keys**
- [Groq API](https://console.groq.com) - Free tier for script generation
- Add to `.env` file

5. **Initialize database**
```bash
python init_db.py
```

6. **Run the application**
```bash
python app.py
```

Visit: `http://localhost:5000`

## Project Structure

```
dropship-affiliate-automation/
├── app.py                 # Main Flask app
├── config.py             # Configuration
├── init_db.py            # Database initialization
├── requirements.txt      # Dependencies
├── .env.example          # Environment variables template
│
├── app/
│   ├── routes.py         # Flask routes
│   ├── models.py         # Database models
│   ├── database.py       # Database setup
│   └── utils.py          # Utility functions
│
├── services/
│   ├── product_service.py      # Product management
│   ├── script_generator.py     # AI script generation
│   ├── video_creator.py        # Video generation
│   ├── tts_service.py          # Text-to-speech
│   └── affiliate_manager.py    # Affiliate links
│
├── templates/
│   ├── index.html        # Dashboard
│   ├── products.html     # Product management
│   ├── video_editor.html # Video preview
│   └── settings.html     # Settings
│
└── static/
    ├── css/
    ├── js/
    └── media/            # Generated videos & images
```

## Usage

### 1. Add Products
- Go to Dashboard → Add Product
- Enter: Name, Price, Image URL, Description, Amazon ASIN (optional)
- System auto-generates affiliate links

### 2. Generate Scripts
- Select products
- Click "Generate Scripts"
- AI creates engaging product descriptions

### 3. Create Videos
- Select products with scripts
- Click "Create Videos"
- System generates video with voiceover

### 4. Download & Post
- Videos ready for TikTok, Instagram Reels, YouTube Shorts
- Download and post to social media

## Cost Breakdown

| Service | Cost | Alternative |
|---------|------|-------------|
| Groq API | Free (50 req/day) | Upgrade for more |
| gTTS | Free | Free |
| FFmpeg | Free | Free |
| Hosting | Free (local) | Replit/Render |
| Database | Free (SQLite) | Free |
| **Total Monthly** | **$0-5** | Scale as needed |

## API Keys Needed

Create `.env` file:
```
GROQ_API_KEY=your_key_here
AMAZON_AFFILIATE_ID=your_affiliate_id
FLASK_SECRET_KEY=your_secret_key
```

## Workflow Example

```
1. Add Product (AliExpress link)
   ↓
2. Generate Script (AI creates description)
   ↓
3. Create Video (FFmpeg + voiceover)
   ↓
4. Download (MP4 format)
   ↓
5. Post to TikTok/Instagram/YouTube
   ↓
6. Earn Affiliate Commission
```

## Features Coming Soon

- [ ] Batch video generation
- [ ] Automatic social media posting (API integration)
- [ ] Performance analytics
- [ ] Product research automation
- [ ] Multi-language support
- [ ] Custom branding/watermarks

## Troubleshooting

**FFmpeg not found?**
```bash
# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

**Groq API slow?**
- Switch to free tier of alternative: Replicate.com, Together.ai

**Videos not generating?**
- Check FFmpeg installation
- Verify image URLs are accessible
- Check console logs

## Legal Disclaimer

- Ensure you have rights to product images
- Follow FTC guidelines for affiliate disclosures
- Comply with Amazon Associates agreement
- Respect platform ToS (TikTok, Instagram, YouTube)

## Contributing

Feel free to improve this system! Fork and submit PRs.

## License

MIT License - Use freely for personal/commercial projects

---

**Made with ❤️ for automation enthusiasts**

Need help? Check the Wiki or open an issue!