from utils import get_transcript, remove_fillers, get_channel_videos, filter_videos_last_2_years
# total_transcript = get_transcript('https://www.youtube.com/watch?v=hUY8DiQgUUg')
# filtered_transcript = remove_fillers('https://www.youtube.com/watch?v=hUY8DiQgUUg')
# print(total_transcript)
# print("----------------------------------")
# print(filtered_transcript)
videos = get_channel_videos('https://www.youtube.com/@KillTony')
print(videos)