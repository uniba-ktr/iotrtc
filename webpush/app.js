const express = require('express');
const bodyParser = require('body-parser');
const webpush = require('web-push');
const app = express();

// VAPID keys
const publicKey = "BL5TgGlIpmn3hADKeKxn3V8QmpWreSspLyIs3_wMfIq-bYuedL1LnnGQe9OQbB4keBXPP-fAAbimxsuEa3YOJR8";
const privateKey = "5LTTo-vsHNmql4H3gTbbm3y8UAgdCdgJYxLOcZZyAiI";

// Variable for subscription
var subscription;

// Parse JSON body
app.use(bodyParser.json());

// Serve static subscription page
app.use('/', express.static('public'));

// Post message to server, servers sends message as notification to subscription
app.post('/api/send-msg', (req, res) => {
  if(subscription == undefined){
    console.log("NO subscription available!");
  } else {
    let obj = new Object();
    obj.title = req.body.title;
    obj.text = req.body.text;
    obj.url = req.body.url;

    let objString = JSON.stringify(obj);

    const options = {
      vapidDetails: {
        subject: "mailto:test@example.com",
        publicKey: publicKey,
        privateKey: privateKey
      },
      TTL: 60 * 60
    };

    webpush.sendNotification(
      subscription,
      objString,
      options
    )
    .then(() => {
      res.status(200).send({success: true});
    })
    .catch((err) => {
      if (err.statusCode) {
        res.status(err.statusCode).send(err.body);
      } else {
        res.status(400).send(err.message);
      }
    });
  }
});

// Save subscription details, currently only works for one subscription.
app.post('/api/add-sub', (req, res) => {
  subscription = req.body;
  res.status(200).send({success: true});
});

// Start the server
const server = app.listen(process.env.PORT || '3000', () => {
  console.log('App listening on port %s', server.address().port);
});
