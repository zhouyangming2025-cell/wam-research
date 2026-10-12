from pathlib import Path
import base64,csv
P='''5N955qp5uQHTEPMZJdMBAXILJ8cBA2QLJb0BA1QNJ7UBA0YLKa0BAzYNJ6kBBygNKaMBBxoNK6EBCQwNK58BCwANLZ8BDQsNL6EBDxUPM6EBEx8PM6UBFSkPOakBGTERO60BGzUTQbEBHz0TRbcBIz8TSb0BJ0UXUcMBK0cXV8kBL0kZXc8BNU0bZ9UBOU0bbdsBP1Efd+EBR1Ehf+cBS1EhiwHtAVNPJZUB8wFZTSWfAfkBX0cpqwH9AWM/KbcB/wFnNS3c43i2h3jQVd4EbsYIcl7cASjOCI4BRPoBKtIIsAEmlgIy1AjQAQiyAjbQCPgBFcwCOsoIngI15gJAwAjIAlH4AkS0CPQCb44DSKIIngONAZwDTo4IzAOpAagDUPYH+gPDAbIDVNoHqATdAboDWL4H1ATzAb4DWp4HggWJAsADXvwGrAWfAsIDXtoG2AWxAsADYLIGggbFArwDYo4GqgbTArYDZOYF0AblAq4DYrwF+AbzAqQDZJQFmgeBA5oDYuoEvgeLA4oDYMAE4AeVA/4CYJgE/gebA+oCXuwDnAifA9wCXMYDuAifA8oCWJ4D0gifA7YCVvYC7AiXA6YCUtAChAmPA5QCTq4CnAmFA4ACSobGet6peMApwS6TDYAF2wO2AYgBOJAFywOyAY4BOJ4FuQOyAZIBOqwFpwOwAZgBOLoFlwOuAZoBOsYFgwOsAZ4BONQF8wKoAaABOOIF4QKoAaQBOu4FzwKkAaYBNvgFvwKeAagBOIYGrwKaAawBNo4GmwKUAa4BNpoGjQKMAbABNKQG/QGEAbIBNKwG7QF4sgEytgbdAXCyATK6BtEBYrABLsIGwQFYsAEuxga1AUysASzMBqcBQKYBKs4GnQE4ogEo0AaRAS6cASbSBocBKJIBItQGfyaMASLWBnUkggEg1gZvJngc2gZpKnAc3AZhMmYa3gZfOFwW5AZZQlIWqMd7rMl41wUonjBHBrkBCgBbBMkBCgBvCNsBDgCFAQjtAQ4BmwEK/QEOALcBDI8CEAHRAQ6fAhIB7QEQqwIUAIsCFLUCFgOrAha5AhYBywIavQIaA+kCHr0CGgGLAyC7AhoDqQMkvQIcAcsDJLsCGgHpAya9AhYAiwQmuwIUAKkEJrkCEALJBCS3AgoE5wQkrwIGBIcFIqkCAQalBR6hAgUGwQUelwINCN0FGI8CEwr3BRiFAhcIkwYS+wEbCqsGEPEBIQrDBgzpASMK2QYI3wElCvEGBNcBJwo='''
meta=[(46,1780,4.69,1.73),(47,1780,4.53,1.77),(26,980,7.39,2.6),(27,980,4.99,1.91)]
b=base64.b64decode(P);out=[];cur=shift=0
for x in b:
 cur|=(x&127)<<shift
 if x&128:shift+=7
 else:out.append(cur>>1 if cur%2==0 else -(cur>>1)-1);cur=shift=0
assert len(out)==4*31*5,len(out)
output=Path(__file__).parent/'data'/'interaction_extra_real_0p1s.csv'
with open(output,'w',newline='') as h:
 w=csv.writer(h);w.writerow('track_id,frame_id,timestamp_ms,agent_type,x,y,vx,vy,psi_rad,length,width'.split(','))
 j=0
 for id,first,L,W in meta:
  pos=[0]*5
  for f in range(first,first+31):
   for k in range(5):pos[k]+=out[j];j+=1
   w.writerow([id,f,f*100,'car']+[f'{u/1000:.3f}' for u in pos]+[L,W])
print(output,'rows',len(out)//5)
