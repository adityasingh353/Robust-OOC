# 🚀 Hmara Project: RobustOOC (Robust Out-Of-Context Detection)

Yeh document tumhari presentation ke liye ek simple aur detailed guide hai. Ise ek story ki tarah padho, aaram se yaad ho jayega!

---

## 1. Asal Mudda Kya Hai? (The Core Problem)
Imagine karo ek sachi photo hai: **"Ek aadmi Mumbai mein baarish mein chal raha hai."**
Lekin kisi ne internet par us photo ko daal diya aur caption likh diya: **"Dekho, Delhi mein bhayankar baadh (flood) aayi hai!"**

Photo asli hai, par uska jo **Caption (text)** hai, wo jhooth bol raha hai. Isko bolte hain **"Out-Of-Context" (OOC)** ya **"Cheapfake"**. Aaj kal fake news aise hi banti hai kyunki photo asli hone ki wajah se log jaldi vishwas kar lete hain.

**Hmara Goal:** Ek aisa AI (Artificial Intelligence) system test karna aur banana jo automatically bata sake ki:
- **NOOC (Not Out-Of-Context):** Photo aur caption dono match kar rahe hain (Sach).
- **OOC (Out-Of-Context):** Photo asli hai par caption kisi aur cheez ke baare mein hai (Jhooth).

---

## 2. Hmare Project Ka Naam "RobustOOC" Kyun Hai?
- **OOC:** Out-of-Context (jaisa upar bataya).
- **Robust (Majboot):** Hum sirf ye nahi check kar rahe ki AI normal fakes pakad pata hai ya nahi. Hum ye check kar rahe hain ki agar hum text mein thodi si hera-pheri (tricky changes) kar dein, toh kya AI fail ho jayega? Hum AI ki "majbooti" (robustness) test kar rahe hain.

---

## 3. Humne Ab Tak Kya Kiya? (Our 2 Main Phases)

Hmara project do bade hisso (Phases) mein divided hai:

### 🌟 Phase 1: Puraane Models Ki Checking (Reproducibility Audit)
Humne socha ki pehle dekhte hain ki duniya mein jo dusre researchers ne AI models banaye hain, wo kitne acche hain. 
- Humne bohot saare purane research papers ke code ko test kiya (jaise COSMOS, Unified Network, CSGM).
- **Result:** Humein pata chala ki zyada tar purane models ka code kaam hi nahi karta! (Dependencies purani hain, ya code missing hai).
- **Solution:** Toh humne apne khud ke 2 naye aur solid "Baseline Models" banaye:
  1. **Baseline A:** NLI + CLIP (Ek model jo photo dekhta hai aur doosra jo text samajhta hai, aur dono ko compare karta hai).
  2. **Baseline B:** LLaVA + RoBERTa (LLaVA ek smart AI hai jo photo dekh ke khud uski summary likhta hai, fir hum us summary ko fake caption se compare karte hain).

### 🌟 Phase 2: The "Robustness" Test (Hmara Main Kaam)
Ab hmare paas working AI models hain aur ek dataset hai jisme 900 photos aur captions hain (COSMOS-FIXED-v1 dataset). 

Ab hum AI ke saath ek **"Game"** khel rahe hain jise **"Perturbation" (Cher-chaar)** kehte hain. Hum original captions ke words ko thoda change karke dekhte hain ki AI confuse hota hai ya nahi. 

**Hum 5 tareeke se captions ko change karte hain:**
1. **Paraphrase:** Baat wahi hai, bas bolne ka tareeka badal diya. (Kiya AI samajh payega?)
2. **Entity Swap:** "Narendra Modi" ki jagah "Rahul Gandhi" likh diya. (Naam badal diya).
3. **Negation:** "Baarish ho rahi hai" ko "Baarish NAHI ho rahi hai" kar diya. (Ulta kar diya).
4. **Date Shift:** "2019" ki jagah "2024" likh diya.
5. **Location Shift:** "Mumbai" ki jagah "Delhi" kar diya.

**Hum dekhna chahte hain ki in chote-chote changes se AI kitna easily bewaqoof ban jata hai.**

---

## 4. Presentation Mein Bolne Ke Liye Important Terms (Cheat Sheet)

Presentation dete waqt in words ka use zaroor karna, isse impression accha padega:

- **Cheapfake:** Jab photo asli ho par context (caption) galat ho. Deepfake mein video nakli hoti hai, Cheapfake mein bas caption badal kar bewkoof banaya jata hai.
- **Reproducibility:** Jab koi doosra researcher kisi aur ke code ko chala kar same result laane ki koshish karta hai. Hmari Phase 1 puri isi par thi.
- **Robustness:** AI kitna strong hai. Agar hum data mein thoda noise ya change daalein, toh kya AI tab bhi sahi answer dega?
- **Perturbation:** Data ke andar jaan-boojh kar chhote changes (jaise location ya date badalna) karna, AI ki testing ke liye.
- **LLM (Large Language Model) / LLaVA:** Aaj kal ke smart AI (jaise ChatGPT) jo text aur photos dono samajh sakte hain. Hum inka use kar rahe hain apne experiments mein.

---

## 5. Summary (Sirf 4 Line Mein Poora Project)

*"Sir/Ma'am, hmara project Fake News detection par hai, specifically 'Cheapfakes' jahan log asli photos par jhoothe captions lagate hain. Humne pehle purane AI models ko test kiya aur dekha ki wo theek se kaam nahi karte, isliye humne apne naye modern AI baselines banaye. Ab hum un models ki 'Robustness' test kar rahe hain yeh dekhne ke liye ki agar hum captions mein chhote-mote tricky changes (jaise date ya location badalna) karte hain, toh AI kitna easily confuse hota hai. Isse humein pata chalega ki aaj ke AI systems real-world fake news se ladne ke liye kitne taiyaar hain."*

---
**Best of luck for your presentation! You've got this!** 👍
