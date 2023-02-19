def srt_to_text(srt_captions: dict) -> str:
    
    captions_list = [cap['text'] for cap in srt_captions]
    str_captions = " ".join(captions_list)
    
    return str_captions