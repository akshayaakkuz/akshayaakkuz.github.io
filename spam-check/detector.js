/* Explainable English-language heuristic baseline. No model or external requests. */
(function (root) {
  'use strict';
  const rules = [
    {id:'prize', points:3, label:'Prize or winner claim', pattern:/\b(you(?:'ve| have)? won|you are a winner|you(?:'re| are) (?:a |the )?lucky winner|claim your (?:prize|reward)|lottery winner|selected to win)\b/i},
    {id:'urgency', points:1, label:'Pressure to act quickly', pattern:/\b(act now|urgent|immediately|last chance|within \d+ hours?|expires? today|limited time)\b/i},
    {id:'credentials', points:4, label:'Request involving passwords or verification codes', pattern:/\b(?:send|share|provide|enter|confirm|verify)\b.{0,50}\b(?:password|otp|one[- ]time (?:password|code)|verification code|login details|bank details)\b/i},
    {id:'payment', points:3, label:'Unusual payment or advance-fee request', pattern:/\b(pay (?:a |the )?(?:small |processing |registration |delivery )?fee|wire transfer|send (?:money|bitcoin|crypto)|pay (?:with|using) gift cards)\b/i},
    {id:'profit', points:3, label:'Guaranteed income or unrealistic return', pattern:/\b(guaranteed (?:income|profit|returns?)|double your money|risk[- ]free investment|earn \$?\d+ (?:daily|per day)|get rich quick)\b/i},
    {id:'threat', points:2, label:'Account suspension or closure threat', pattern:/\b(?:account|access)\b.{0,40}\b(?:suspended|blocked|terminated|closed|disabled)\b/i},
    {id:'promotion', points:1, label:'Promotional offer language', pattern:/\b(free gift|exclusive offer|cash bonus|buy now|congratulations)\b/i},
    {id:'link', points:1, label:'Contains a web address', pattern:/\b(?:https?:\/\/|www\.)\S+/i},
    {id:'shortlink', points:1, label:'Shortened link hides its destination', pattern:/\b(?:https?:\/\/)?(?:bit\.ly|tinyurl\.com|t\.co|shorturl\.at)\//i},
    {id:'punctuation', points:1, label:'Repeated exclamation marks', pattern:/!{3,}/}
  ];
  function analyze(message) {
    if (typeof message !== 'string' || !message.trim()) throw new Error('Enter a message to check.');
    if (message.length > 5000) throw new Error('Keep the message under 5,000 characters.');
    const text = message.normalize('NFKC').replace(/[\u200B-\u200D\uFEFF]/g,'').replace(/[\r\n\t]+/g,' ');
    const matches = rules.filter(rule=>rule.pattern.test(text)).map(({id,points,label})=>({id,points,label}));
    const letters = text.match(/[a-z]/gi) || [];
    const capitals = text.match(/[A-Z]/g) || [];
    if (letters.length >= 20 && capitals.length / letters.length > .75) matches.push({id:'caps',points:1,label:'Mostly capital letters'});
    const score = matches.reduce((sum,item)=>sum+item.points,0);
    return {score,level:score>=5?'Likely spam':score>=2?'Needs a closer look':'Few spam signals',matches};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {analyze};
  else root.SpamDetector = {analyze};
})(typeof globalThis !== 'undefined' ? globalThis : this);

