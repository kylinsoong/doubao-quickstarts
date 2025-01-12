const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));

const BACKEND_API_HOST = process.env.BACKEND_API_HOST || '127.0.0.1:3000';
const API_URL = `http://${BACKEND_API_HOST}/api/videos`;

app.get('/', async (req, res) => {
  const clientIp = req.ip;
  const clientPort = req.connection.remotePort;
  const userAgent = req.get('User-Agent');
  console.log(`Client request details:
    IP: ${clientIp}
    Port: ${clientPort}
    User-Agent: ${userAgent}
  `);

  try {
    const response = await axios.get(API_URL);
    const videos = response.data;
 
   videos.forEach((video) => {
      const urlParts = video.url.split('/');
      video.url = urlParts[urlParts.length - 1];
      video.audio = video.audio.replace(/\n/g, '<br>');
      video.video = video.video.replace(/\n/g, '<br>');
   });

    res.render('index', { videos });
  } catch (error) {
    console.error('Error fetching videos:', error);
    res.status(500).send('An error occurred while fetching videos.');
  }
});

const port = 4000;
app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});

