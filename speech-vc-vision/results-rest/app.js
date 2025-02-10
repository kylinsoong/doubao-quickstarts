const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

const dbUrl = process.env.DB_URL;
const dbName = process.env.DB_NAME;
const dbTableName = process.env.DB_TABLE_NAME;
const dbTableNameWZYT = process.env.DB_TABLE_WZYT_NAME;
const port = process.env.PORT || 3000;

const client = new MongoClient(dbUrl, {});

app.get('/api', (req, res) => res.send('REST API!'));

app.get('/api/videos', async (req, res) => {
    try {
        await client.connect();
        const collection = client.db(dbName).collection(dbTableName);
        const options = {projection: { _id: 0, type: 0 }};
        const users = await collection.find({},options).toArray();
        res.json(users);
    } catch (err) {
        res.status(500).send("An error occurred while fetching users.");
    } finally {
        await client.close();
    }
});

app.get('/api/video/:uid', async (req, res) => {
    const { uid } = req.params;  // Get the UID from the request parameters
    try {
        await client.connect();
        const collection = client.db(dbName).collection(dbTableName);
        const video = await collection.findOne({ uid }, { projection: { _id: 0, type: 0 }});  // Query by UID
        if (!video) {
            return res.status(404).json({ message: 'Video not found' });
        }
        res.json(video);
    } catch (err) {
        res.status(500).send("An error occurred while fetching the video.");
    } finally {
        await client.close();
    }
});

app.get('/api/wzyt/videos', async (req, res) => {
    try {
        await client.connect();
        const collection = client.db(dbName).collection(dbTableNameWZYT);
        const options = {projection: { _id: 0, type: 0 }};
        const users = await collection.find({},options).toArray();
        res.json(users);
    } catch (err) {
        res.status(500).send("An error occurred while fetching users.");
    } finally {
        await client.close();
    }
});

app.get('/api/wzyt/video/:uid', async (req, res) => {
    const { uid } = req.params;  // Get the UID from the request parameters
    try {
        await client.connect();
        const collection = client.db(dbName).collection(dbTableNameWZYT);
        const video = await collection.findOne({ uid }, { projection: { _id: 0, type: 0 }});  // Query by UID
        if (!video) {
            return res.status(404).json({ message: 'Video not found' });
        }
        res.json(video);
    } catch (err) {
        res.status(500).send("An error occurred while fetching the video.");
    } finally {
        await client.close();
    }
});


app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});

