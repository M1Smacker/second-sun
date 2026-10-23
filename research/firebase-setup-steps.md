# Firebase setup for Eyes mode cloud backup (Stage B): exact steps for Ahmed

*Researched 24 Oct 2026 against Firebase's own docs (links at the bottom). Project name: `second-sun`. About 15 minutes, free, no card. Use a computer browser if you can (the console is awkward on a phone). Claude cannot create accounts or log in for you. Menu names change now and then: if a screen looks different from what is written here, send a screenshot. Stage A (saving on your device) already works without any of this.*

## Part 1: create the project (console.firebase.google.com, signed in with your Google account)
1. Click **Create a project** (or **Add project**).
2. Name it **`second-sun`**. Under the name Firebase shows a *project ID*; it may add letters or numbers (for example `second-sun-1a2b3`). Leave it as it is and click **Continue**.
3. If it offers AI assistance, skip or turn it off. Turn **Google Analytics OFF**. Click **Create project**, wait, then **Continue**.
4. Stay on the free **Spark** plan. If any screen says Upgrade or asks for a card, do not click it: nothing here needs it.

## Part 2: create the database
5. In the left menu open **Databases & Storage**, then **Firestore** (older consoles: **Build, then Firestore Database**). Click **Create database** (or **Add database**).
6. Choose **Standard edition** (not Enterprise).
7. **Database ID**: leave `(default)`.
8. **Location**: choose **eur3 (Europe)**. It cannot be changed later; speed does not matter because rounds are saved on your device first.
9. **Security rules**: choose **Production mode**, then **Create**. Wait about a minute.
10. Open the **Rules** tab. Select everything in the editor, delete it, paste the rules below exactly, and click **Publish**.

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
These rules let the book add a round once and never change or read it. Only the service account key in Part 4 (Claude's reader) can read.

## Part 3: register the web app (two public values for the book)
11. Click the gear next to **Project Overview**, then **Project settings**, then the **General** tab.
12. Under **Your apps** click the **web icon `</>`**. Nickname: `eyes`. Leave **Firebase Hosting** unticked. Click **Register app**.
13. A block of code appears with `apiKey` and `projectId`. **Send me those two values in chat.** They are public by design (every Firebase website exposes them); they are not secrets. Ignore the rest and click **Continue to console**.

## Part 4: the key for Claude's reader (this one IS a secret)
14. Still in **Project settings**, open the **Service accounts** tab. Click **Generate new private key**, then **Generate key**. A `.json` file downloads. (If the button is greyed out or an error says key creation is disabled by an organisation policy, tell me and do not try to get around it: I will propose another way.)
15. **Move that file to `D:\second-sun-secrets\firebase-second-sun.json`** (create the folder if needed). Then **delete the copy from your Downloads folder and empty the Recycle Bin**: Downloads is on C:, and the key must live only on D:. **Never send me the file or its contents, never put it in the book or the repo.** Tell me only "the key is in place". My reader reads it from that path and never prints it.

## When you are done
Tell me **"Firebase is set up"** with the `apiKey` and `projectId` from step 13. I then build Stage B: the automatic upload (as soon as a round ends, or when the internet returns), the reader, and the daily pull into the repo. I test the rules myself (a good write must work; a read, a change and a junk write must be refused), and then we check one 5-curve round end to end: you do it on your phone, I read it back from Firebase and compare every number with what your screen showed.

## Part 5: one safety setting, AFTER I tell you the upload works (3 minutes)
16. Go to **console.cloud.google.com**, choose the project `second-sun` in the top bar, then **APIs and Services, then Credentials**. Under **API keys** click **Browser key (auto created by Firebase)**. Under **Application restrictions** choose **Websites** and add `https://m1smacker.github.io/*`. Leave **API restrictions** as Firebase set them. Save. This only limits quota abuse; the security rules are the real protection. I ask you to do it after my tests because it also blocks the key from my local test pages.

## Good to know
- **Free limits (Spark):** 20,000 document writes and 50,000 reads per day, no cost, and you cannot be billed without adding a card. One round is one write. If a limit were ever hit, saving to the cloud would pause; your rounds stay on the device and upload later.
- **Meanwhile:** practise at https://m1smacker.github.io/second-sun/eyes/ . On your iPhone use **Share, then Add to Home Screen**, so Safari keeps your rounds. Until Stage B I cannot see your scores, and you will never be asked to send them.

## Sources (Firebase and Google Cloud docs)
- Create the database, editions, production mode: https://firebase.google.com/docs/firestore/manage-databases and https://firebase.google.com/docs/firestore/quickstart
- Spark free quotas: https://firebase.google.com/docs/projects/billing/firebase-pricing-plans
- Service account key: https://firebase.google.com/docs/admin/setup
- API keys and why rules are the real protection: https://firebase.google.com/docs/projects/api-keys and https://docs.cloud.google.com/api-keys/docs/add-restrictions-api-keys
