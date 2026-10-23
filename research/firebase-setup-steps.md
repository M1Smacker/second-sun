# Firebase setup for Eyes mode cloud backup (Stage B): steps for Ahmed

*About 10 to 15 minutes, free, no card. Claude cannot create accounts or log in for you. Menu names can differ a little; if anything looks different, send a screenshot. Stage A (saving on your device) already works without any of this.*

## Part 1: the project (console.firebase.google.com, signed in with your Google account)
1. Click **Create a project** (or **Add project**). Name it `second-sun-eyes`. Turn **Google Analytics OFF** (not needed). Click **Create project**, then **Continue**.
2. Stay on the **Spark (free)** plan. Never click Upgrade or add a card.

## Part 2: the database
3. In the left menu: **Build, then Firestore Database, then Create database**.
4. Location: pick **eur3 (Europe)** (it cannot be changed later; speed does not matter because rounds are saved on your device first).
5. Choose **Start in production mode**, then **Create**.
6. Open the **Rules** tab, delete what is there, paste the rules below exactly, and click **Publish**.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /eyes_rounds/{id} {
      allow create: if request.resource.data.keys().hasOnly(['v','id','mode','source','n','t0','t1','status','device','a','s'])
        && request.resource.data.v == 1
        && request.resource.data.id == id
        && request.resource.data.mode in ['practice','test','real']
        && request.resource.data.n is int && request.resource.data.n <= 200
        && request.resource.data.a is list && request.resource.data.a.size() <= 200;
      allow read, update, delete: if false;
    }
  }
}
```
These rules let the book add a round once and never change or read it; only you and Claude (with the key in Part 4) can read.

## Part 3: the web app (two public values for the book)
7. Click the gear next to **Project Overview, then Project settings**.
8. Under **Your apps**, click the **web icon `</>`**. Nickname: `eyes`. Do NOT tick Firebase Hosting. Click **Register app**.
9. You will see a block of code with `apiKey` and `projectId`. **Send me those two values in chat** (they are public by design; they are not secrets). You can ignore the rest.

## Part 4: the key for Claude's reader (this one IS a secret)
10. Still in Project settings, open the **Service accounts** tab and click **Generate new private key**, then **Generate key**. A `.json` file downloads.
11. **Move that file to `D:\second-sun-secrets\firebase-eyes.json`** (create the folder if needed), then **delete the copy from your Downloads folder and empty the Recycle Bin** (Downloads is on C:, and the key must live only on D:). **Never send the file or its contents to me or anyone; never put it in the repo.** Tell me only "the key is in place". The reader reads it from that path and never prints it.

## Part 5: one safety setting (optional but recommended, 3 minutes)
12. Open **console.cloud.google.com**, same project, **APIs and Services, then Credentials**. Click the **Browser key** (created by Firebase). Under **Application restrictions** choose **Websites** and add `https://m1smacker.github.io/*`. Under **API restrictions** choose **Restrict key** and tick only **Cloud Firestore API**. Save.

## When you are done
Tell me: "Firebase is set up", plus the two values from step 9. Then I build Stage B: the automatic upload (as soon as a round ends or the internet returns), the reader script, and the daily pull into the repo, and we check one 5-curve round end to end: you do it, I read it back and compare every number with your screen.

## Meanwhile
Open https://m1smacker.github.io/second-sun/eyes/ and practise. On your iPhone, **Share, then Add to Home Screen**, so Safari keeps your rounds. Until Stage B, results live on the device you used and I cannot see them (you will never be asked to send anything: once Firebase is set up, every finished round reaches me by itself).
