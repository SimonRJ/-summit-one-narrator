"""Shared source-fidelity rules for AMC solution films.
Semantic source colours always win over the decorative house palette.
"""
import json,re
from pathlib import Path

def load_question(path):
    q=json.loads(Path(path).read_text())
    for k in ['question_text','problem_type','solution_approach']:
        assert isinstance(q.get(k),str) and q[k].strip(), f'Missing {k}'
    assert ' '.join(q['question_lines'])==q['question_text'], 'Opening must preserve the exact question'
    assert q['question_segment']==1 and q['orientation_segment']<q['solution_starts_at_segment']
    assert isinstance(q['colours_carry_meaning'],bool)
    assert q['diagram_surface'] in ['dark','light']
    if q['colours_carry_meaning']:
        assert q['source_colours'], 'Supply the actual source colours; never substitute the house palette'
        assert q.get('colour_meanings'), 'Document what each colour represents'
        assert set(q['colour_meanings'])<=set(q['source_colours'])
    for colour in q['source_colours'].values():assert re.fullmatch(r'#[0-9a-fA-F]{6}',colour)
    return q

def source_colour(question,role):
    """No decorative fallback for a source-colour role."""
    return question['source_colours'][role]

def diagram_surface(question):
    """A light canvas is available when true source colours need it for contrast."""
    return '#ffffff' if question['diagram_surface']=='light' else '#000000'
