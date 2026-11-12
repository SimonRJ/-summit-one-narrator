"""Complete the remaining short solutions and restore the verified 2008 Q2 figure."""
from pathlib import Path
import json
solutions=[
('amc-up-2008',2,'DATA-03','Between 1 and 2 the number line has ten equal intervals, so each short interval is one tenth, or 0.1. The arrow points three intervals after 1. Its value is 1 + 3×0.1 = 1.3. Read the scale before counting the small ticks.'),
('amc-up-2008',4,'FRAC-04','Half full means one of two equal parts of the 7500-litre capacity. Divide by 2: 7500 ÷ 2 = 3750 litres. Check by doubling: 3750 + 3750 = 7500.'),
('amc-up-2008',5,'RATE-01','One bottle fills three glasses of the stated size. Seven identical bottles therefore fill seven groups of three glasses: 7 × 3 = 21. The question asks for glasses, so multiply by the number of glasses per bottle.'),
('amc-up-2008',6,'DIG-01','An increase is the new price minus the old price: 153.5 − 149.9. From 149.9 to 150 is 0.1, then from 150 to 153.5 is 3.5. Add 0.1 + 3.5 = 3.6 cents per litre. Keep the answer in cents, not dollars.'),
('amc-up-2008',9,'ALG-01','Three equal boxes and two loose cars contain 17 cars altogether. Remove the two loose cars: 17 − 2 = 15 cars are in the boxes. Divide equally among three boxes: 15 ÷ 3 = 5 cars per box. Check: 3 × 5 + 2 = 17.'),
('amc-up-2023',3,'ALG-01','The two visible dice show 5 and 3, for a total of 8. The three dice must total 12, so the missing die shows 12 − 8 = 4. Check: 5 + 3 + 4 = 12.'),
('amc-up-2024',1,'RATE-01','Each birthday increases the age by one. Fourteen years after the birth year 2016 is 2016 + 14 = 2030. Thus the fourteenth birthday is in 2030.')]
rows=[dict(exam_id=e,question_number=n,category=k,explanation=s) for e,n,k,s in solutions]
body='<path d="M30 90H421" stroke="black"/>'
for i in range(34):
 x=30+i*11.7;body+=f'<path d="M{x} 90v{16 if i%10==0 else 12 if i%5==0 else 6}" stroke="black"/>'
 if i%10==0:body+=f'<text x="{x}" y="132" text-anchor="middle" font-size="17">{i//10}</text>'
x=30+13*11.7;body+=f'<path d="M{x} 48V90m-9 -10l9 10l9 -10" stroke="black" fill="none"/>'
rows[0]['figure_svg']=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 160" role="img" aria-label="Number line labelled 0, 1, 2, 3 with ten intervals per unit; arrow three intervals after 1"><rect width="450" height="160" fill="white"/>{body}</svg>'
Path(__file__).resolve().parents[3].joinpath('rebuild/archive-finishing.json').write_text(json.dumps(rows))
