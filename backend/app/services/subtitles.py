def segments_to_srt(segments):
    def fmt(t):
        h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t-int(t))*1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    out=[]
    for i,seg in enumerate(segments,1):
        out.append(f"{i}\n{fmt(seg['start'])} --> {fmt(seg['end'])}\n{seg['text']}\n")
    return "\n".join(out)

def segments_to_vtt(segments):
    def fmt(t):
        h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t-int(t))*1000)
        return f"{h:02}:{m:02}:{s:02}.{ms:03}"
    lines=["WEBVTT",""]
    for seg in segments:
        lines.append(f"{fmt(seg['start'])} --> {fmt(seg['end'])}")
        lines.append(seg['text'])
        lines.append("")
    return "\n".join(lines)
