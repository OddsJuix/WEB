const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ServerApiVersion } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = "mongodb+srv://honeistudios:0B9t81AT5FnDsdkf@cluster0.grko5vt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function run() {
  try {
    await client.connect();
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } catch (err) {
    console.error("Fucked up MongoDB:", err);
    process.exit(1);
  }
}
run().catch(console.dir);

// Define some fkn stupid API bullshit
app.post('/subscribe', async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  try {
    const database = client.db("newsletter");
    const collection = database.collection("subscribers");

    const result = await collection.insertOne({ email, subscribedAt: new Date() });
    res.status(200).json({ message: 'Email subscribed worked!!!', result });
  } catch (error) {
    if (error.code === 11000) {
      res.status(409).json({ error: 'Email is already subscribed, now quit!' });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
