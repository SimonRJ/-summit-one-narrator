-- Correct repeated-prime factor counts. Preserve the old key in an explicit erratum.
with fixes(exam_id,question_number,expected_old,corrected,base,exponent) as (
 values ('summit-amc-mock-03',28,'16','7',15625,6),
 ('summit-amc-mock-04',28,'12','6',3125,5),
 ('summit-amc-mock-06',29,'8','5',625,4),
 ('summit-amc-mock-13',30,'20','8',78125,7),
 ('summit-amc-mock-19',29,'8','5',625,4),
 ('summit-amc-mock-22',30,'20','8',78125,7)
)
update public.exam_questions q set
 answer=to_jsonb(f.corrected),
 explanation=format('Write %s as one power of its prime factor: %s = 5^%s. Every positive factor is 5^k, where k can be any whole number from 0 to %s. There are %s such choices, including 5^0 = 1 and 5^%s = %s. So there are %s positive factors. Check: combine powers of the same prime before counting; multiplying separate exponent-choice counts would count the same factors more than once.',f.base,f.base,f.exponent,f.exponent,f.corrected,f.exponent,f.base,f.corrected),
 metadata=coalesce(q.metadata,'{}'::jsonb)||jsonb_build_object('answer_erratum',jsonb_build_object('previous_answer',f.expected_old,'corrected_answer',f.corrected,'reason','Repeated powers of the same prime must be combined before counting factors.','corrected_on','2026-11-12'))
from fixes f where q.exam_id=f.exam_id and q.question_number=f.question_number and q.answer=to_jsonb(f.expected_old)
returning q.exam_id,q.question_number,q.answer;
