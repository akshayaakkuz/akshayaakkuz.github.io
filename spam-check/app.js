'use strict';
const message = document.getElementById('message');
const examples = {
  normal:'Hey, are we still meeting at the library at 4? I will bring the notes.',
  prize:'Congratulations! You have won a prize. Claim your reward immediately! Pay a processing fee at https://example.com/claim !!!',
  account:'URGENT: Your account will be suspended. Enter your password at https://example.com/verify immediately.'
};
function resetResult() {
  document.getElementById('badge').textContent='READY WHEN YOU ARE';
  document.getElementById('verdict').textContent='A second look, in seconds.';
  document.getElementById('summary').textContent='Your result and the matching warning signs will appear here.';
  document.getElementById('signals').replaceChildren();
  document.getElementById('error').textContent='';
}
function edited(){document.getElementById('count').textContent=message.value.length.toLocaleString('en-US')+' / 5,000';resetResult();}
message.addEventListener('input',edited);
document.getElementById('clear').addEventListener('click',()=>{message.value='';edited();message.focus();});
document.querySelectorAll('[data-example]').forEach(button=>button.addEventListener('click',()=>{message.value=examples[button.dataset.example];edited();message.focus();}));
document.getElementById('checker').addEventListener('submit',event=>{
  event.preventDefault();resetResult();
  try {
    const result=SpamDetector.analyze(message.value);
    document.getElementById('badge').textContent=result.score+' SIGNAL POINT'+(result.score===1?'':'S');
    document.getElementById('verdict').textContent=result.level;
    document.getElementById('summary').textContent=result.matches.length ? 'These patterns contributed to the result. Consider the sender and the context too.' : 'No configured warning signs matched. This does not verify the sender or the message.';
    result.matches.forEach(item=>{const li=document.createElement('li');li.textContent=item.label+' (+'+item.points+')';document.getElementById('signals').append(li);});
  } catch(error){document.getElementById('error').textContent=error.message;}
});

