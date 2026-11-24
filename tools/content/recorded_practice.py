def apply_recorded_film(lesson, catalogue):
    """Use the published edition and keep a revisit's own teaching question."""
    own_id = f"S{lesson['slot']:03}"
    films = catalogue['lessons']
    film_id = own_id if own_id in films else lesson['videoId']
    if film_id not in films:
        return

    guide = films[film_id]
    release = guide.get('release') or catalogue['release']
    lesson.update(videoId=film_id, videoTitle=guide['title'], movie=release + film_id + '.mp4')
    if film_id == own_id:
        lesson['bridge'] = guide['bridge']
        lesson['filmUse'] = 'dedicated'
