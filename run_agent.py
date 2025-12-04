from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv
import asyncio
import os
import glob
    

load_dotenv()
    
async def main():
    
    llm = ChatGoogle(model="gemini-2.5-flash") 
    
    
    task = """
Go to http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html.
I want to create a two-site comparison page for this book.
Please extract the following information and present it as a single JSON object:
1. The book title.
2. The 5-star rating (as a number, e.g., 2).
3. The price (excluding the currency symbol).
4. The product description text.
5. The stock availability (e.g., "In stock (22 available)").
"""
    
    
    print("Agent running... Waiting for browser automation to start.")
    
    
    agent = Agent(
        task=task,
        llm=llm,
        save_gif=False,  
        save_history=True,
        browser_config={
            
            'headless': False, 
            'record_video': {
                'dir': 'videos/', 
                'size': {'width': 800, 'height': 600}
            },
            'args': ['--no-sandbox'], 
            'wait_for_network_idle_page_load_time': 6.0 
        }
    )
    history = await agent.run() 
    
    
    print("="*60)
    print("✅ AGENT RUN COMPLETE ✅")
    print("="*60)
    
    
    final_json_output = history.final_result() 
    print("\n--- FINAL JSON OUTPUT ---")
    print(final_json_output) 
    
    
    video_files = glob.glob('videos/*.webm') + glob.glob('videos/*.mp4')
    
    if video_files:
        
        latest_video = max(video_files, key=os.path.getmtime)
        print(f"\n--- VIDEO OUTPUT PATH ---")
        print(f"Video (Visual Proof) is saved at: {latest_video}")
        print("💡 Download this video file and convert it to a GIF for your submission.")
    else:
        print("\n--- VISUAL PROOF NOT FOUND ---")
        print("🔴 Video/GIF failed to generate. Use the JSON output and try the conversion steps.")
    
if __name__ == "__main__":

    asyncio.run(main())
