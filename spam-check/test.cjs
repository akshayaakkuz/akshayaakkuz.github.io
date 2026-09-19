const assert = require('node:assert/strict');
const {analyze}=require('./detector.js');
assert.equal(analyze('Meet me at the library at 4.').score,0);
assert.equal(analyze('Claim your prize immediately! Pay a processing fee.').level,'Likely spam');
assert.equal(analyze('Enter your password at https://example.com').level,'Likely spam');
assert.equal(analyze('Send your\nverification code immediately').level,'Likely spam');
assert.equal(analyze('You have won You have won').score,3,'Repeated terms must not inflate points');
assert.equal(analyze('Read https://example.com/docs').level,'Few spam signals','A URL alone should not imply spam');
assert.equal(analyze('Your account is suspended').level,'Needs a closer look');
assert.equal(analyze('claim your pr\u200bize').score,3);
assert.equal(analyze('Your appointment is tomorrow. Please arrive 10 minutes early.').score,0);
assert.throws(()=>analyze('  '));assert.throws(()=>analyze('x'.repeat(5001)));
assert.equal(analyze('x'.repeat(5000)).score,0);
console.log('12 functional checks passed. These are regression checks, not a measured accuracy benchmark.');

