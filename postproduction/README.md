# Summit One post-production pipeline

This converts a verified narration WAV plus an existing visual master into the final delivery MP4 without changing narration speed or pitch.

## Rules
- Audio is authoritative. Kokoro narration is never time-stretched.
- Visual timing is preserved when the duration difference is ≤1.2%.
- Visuals are linearly retimed when the audio/visual duration ratio is within 0.80–1.25. Because the glow/caption animation is already rendered into the visual master, the same retime keeps the visual cue sequence proportional to the narration.
- Ratios outside 0.80–1.25 stop automatically unless explicitly forced for a review candidate.
- Final MP4 is H.264/yuv420p + mono AAC/48 kHz with fast-start metadata.
- Every output gets a sidecar VTT, QA JSON and SHA-256. The VTT uses scaled existing word timings where available, otherwise a duration-weighted estimate.
- Integrity requires valid H.264 video, non-silent AAC audio and final duration within 0.20 s of the narration.
- A001 and A049 should use their polished approved final videos as *visual* sources (audio stripped/replaced), not the rejected/generic early masters.

## Single video
`python finish_video.py --video-id A040 --visual A040_visual_master.mp4 --audio A040.wav --registry DEPLOY_VIDEO_REGISTRY.json --out-dir final/A040`

## Batch
`python batch_finish.py --visual-root masters --audio-root kokoro --registry DEPLOY_VIDEO_REGISTRY.json --out-root final --overrides visual_overrides.json`

The batch summary deliberately distinguishes narration completion from final-video completion. A generated WAV never marks the MP4 complete by itself.