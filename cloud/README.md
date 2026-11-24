# Online saves (Firebase)

My Work, teacher mode, Learn publishing and Class Sounds use Firebase Authentication and Cloud Firestore (free Spark plan).
They stay hidden until `cloud-config.json` exists in the site root:

```json
{ "apiKey": "...", "authDomain": "...", "projectId": "...", "appId": "..." }
```

These values are public by design. Access is controlled by `firestore.rules` (paste it into Firestore > Rules).
Roles:
- Teachers sign up in the app (My Work > I'm a teacher > Make a teacher account). Each teacher only sees their own classes.
- Students sign in with the class code on their login card, their picture and their PIN.
- The developer is any account listed in `admins/{uid}` (added by hand in the Firestore console). Only the developer
  can publish Learn examples. To sign in as the developer, tap the My Work title 5 times, or open the site with `#dev`.
