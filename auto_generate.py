#!/usr/bin/env python
"""
Automated video generation script
Generates affiliate videos automatically
"""

import argparse
import sys
from services.video_automation_scheduler import VideoAutomationScheduler

def main():
    parser = argparse.ArgumentParser(description='Dropship Affiliate Video Generator')
    
    parser.add_argument(
        '--videos',
        type=int,
        default=5,
        help='Number of videos to generate (default: 5)'
    )
    
    parser.add_argument(
        '--schedule',
        choices=['once', 'daily', 'hourly'],
        default='once',
        help='Schedule type (default: once)'
    )
    
    parser.add_argument(
        '--time',
        default='00:00',
        help='Scheduled time in HH:MM format (default: 00:00)'
    )
    
    parser.add_argument(
        '--categories',
        nargs='+',
        default=['health', 'wealth', 'wellness'],
        help='Product categories (default: health wealth wellness)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🎬 DROPSHIP AFFILIATE VIDEO GENERATOR")
    print("="*60)
    
    scheduler = VideoAutomationScheduler()
    
    if args.schedule == 'once':
        print(f"\n📹 Generating {args.videos} videos...")
        videos = scheduler.generate_video_batch(
            num_videos=args.videos,
            categories=args.categories
        )
        print(f"\n✅ Complete! Generated {len(videos)} videos")
    
    elif args.schedule == 'daily':
        print(f"\n📅 Starting daily scheduler...")
        print(f"   - Videos per day: {args.videos}")
        print(f"   - Time: {args.time} UTC")
        print(f"   - Categories: {', '.join(args.categories)}")
        scheduler.start_scheduler(schedule_time=args.time, interval='daily')
        print("\n✓ Scheduler running! Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n✓ Scheduler stopped")
    
    elif args.schedule == 'hourly':
        print(f"\n⏰ Starting hourly scheduler...")
        print(f"   - Videos per run: {args.videos}")
        print(f"   - Categories: {', '.join(args.categories)}")
        scheduler.start_scheduler(interval='hourly')
        print("\n✓ Scheduler running! Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n✓ Scheduler stopped")

if __name__ == '__main__':
    main()
