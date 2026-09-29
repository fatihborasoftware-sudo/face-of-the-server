(()=>{ const ss={cancel(){},speak(u){},pause(){},resume(){},speaking:false,pending:false,getVoices(){return [];},addEventListener(){},onvoiceschanged:null};
try{ Object.defineProperty(window,'speechSynthesis',{value:ss,configurable:true}); }catch(e){}
window.SpeechSynthesisUtterance=function(t){this.text=t;}; })();
