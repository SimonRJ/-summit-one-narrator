// Match the complete public example so revised lessons never inherit a stale solution.
export const exampleMethods = new Map([
  ['What is 31 × 8?', {
    method: 'Double three times',
    working: 'Double 31 to get 62. Double again to get 124, then once more to get 248. Three doubles multiply by 2 × 2 × 2, which is 8.',
    comparison: 'The area method uses the fact that 31 is close to 30. Doubling uses the structure of the other factor, 8. Which would you try for 47 × 8?'
  }],
  ['A 12 cm ribbon and a 20 cm ribbon must be cut into equally long whole-centimetre pieces with no waste. What is the greatest possible length of a piece?', {
    method: 'List the possible cuts',
    working: 'The whole-centimetre lengths that divide 12 are 1, 2, 3, 4, 6 and 12. Test these against 20. Only 1, 2 and 4 work, so the greatest length is 4 cm.',
    comparison: 'The list lets you see every possible piece length. Using successive leftovers reaches the greatest length quickly even when the original ribbons are long.'
  }],
  ['Four jars hold an average of 6 marbles. Three jars hold 3, 7 and 8. How many marbles are in the fourth jar?', {
    method: 'Level the jars',
    working: 'Move one marble from the jar of 7 and two from the jar of 8 into the jar of 3. All three now hold 6. For the average of all four to be 6, the fourth jar must already hold 6.',
    comparison: 'The total method works for any jar sizes. Levelling is quick here because the extras in two jars exactly fill the gap in the third.'
  }],
  ['Two square coasters, each 4 cm on a side, touch along a whole side. What is the perimeter of the joined shape?', {
    method: 'Trace the new rectangle',
    working: 'After joining the coasters, trace the outside with your finger. The four sides are 8 cm, 4 cm, 8 cm and 4 cm long. Their sum is 24 cm.',
    comparison: 'Tracing is short because the outline is a rectangle. Subtracting the hidden edges also works when the outline has lots of corners.'
  }],
  ['A bag can carry any two-letter label made from A, B and C, with repeats allowed. How many labels contain at least one A?', {
    method: 'Sort by the first A',
    working: 'If the first A is in the first place, the labels are AA, AB and AC. If the first A is in the second place, the labels are BA and CA. That makes 3 + 2 = 5.',
    comparison: 'Sorting by the first A shows exactly where AA is counted. With longer labels, counting the labels that miss A can save a long list.'
  }],
  ['One machine finishes a batch in 6 minutes. A second takes 3 minutes. What fraction can they finish together in one minute?', {
    method: 'Watch for six minutes',
    working: 'In six minutes the slower machine makes one batch and the faster machine makes two. Together they make three batches in six minutes. At that steady pace, one minute gives 3/6 = 1/2 of a batch.',
    comparison: 'Starting with one minute gives fractions straight away. Starting with six minutes lets you count whole batches before dividing.'
  }],
  ['A baker has 18 rolls. She sells a third, then gives half the remainder to a neighbour. How many rolls does she give away?', {
    method: 'Make three equal groups',
    working: 'Picture the rolls in three equal groups. One group is sold. Half of the two groups left is one group, so the neighbour gets a third of the original rolls. That is 18 ÷ 3 = 6 rolls.',
    comparison: 'Working in groups tells you the neighbour’s share before you even know there are 18 rolls. Working with counts tells you how many are left at each step.'
  }],
  ['A walker covers 4 km in an hour and rests for half an hour. What is the average speed from start to finish?', {
    method: 'Repeat the walk and rest',
    working: 'Imagine doing the same walk and rest twice. In 3 hours the walker covers 8 km, so the average is 8/3 km/h. Repeating the journey doubles both the distance and the time, leaving their ratio unchanged.',
    comparison: 'Including the rest is essential in both methods. Repeating the journey makes the number of hours whole, which can make the division easier.'
  }],
  ['A pattern starts at 4 and doubles at each step. Add the first four terms, then compare their sum with the fifth term. How much larger is that fifth term?', {
    method: 'Add a spare 4',
    working: 'Add an extra 4 to the sum. The two 4s make 8, the two 8s make 16, and the two 16s make 32. The two 32s then make 64, the next term. The original sum was short by exactly that extra 4.',
    comparison: 'Adding up the terms checks this particular sum. Pairing equal terms shows why the same trick works if the doubling list grows longer.'
  }],
  ['A fair coin picks bag A on heads and bag B on tails. Bag A contains two red tokens. Bag B contains one red and one blue token. Draw one token uniformly from the selected bag. What is the probability of red?', {
    method: 'Label the four tokens',
    working: 'Mark the tokens A1, A2, B1 and B2. Each bag has a half chance of being selected, and drawing either token from it is equally likely. The four tokens therefore have equal chances. Three are red, so the chance is 3/4.',
    comparison: 'Counting tokens directly works because the bags are equally likely and have equal sizes. If one bag held more tokens, drawing the two branches would keep the chances straight.'
  }]
]);
