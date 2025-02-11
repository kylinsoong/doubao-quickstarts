const express = require('express');
const axios = require('axios');
const path = require('path');
const bodyParser = require('body-parser');
const session = require('express-session');

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true,
}));

app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));

const BACKEND_API_HOST = process.env.BACKEND_API_HOST || '127.0.0.1:3000';
const API_URL = `http://${BACKEND_API_HOST}/api/videos`;
const API_URL_WZYT = `http://${BACKEND_API_HOST}/api/wzyt/videos`;

app.get('/login', (req, res) => {
  res.render('login', { error: null });
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (username === 'admin' && password === 'demo@666') {
    req.session.user = username; 
    return res.redirect('/');
  }

  res.render('login', { error: 'Invalid username or password' });
});

app.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login'); // Redirect to login after logging out
  });
});

const requireAuth = (req, res, next) => {
  if (req.session.user) {
    return next();
  }
  res.redirect('/login');
};

app.get('/', (req, res) => {
  res.render('index'); // Renders index.ejs
});

app.get('/cfitc', requireAuth, async (req, res) => {
  const clientIp = req.ip;
  const userAgent = req.get('User-Agent');
  console.log(`Client request details: Client IP: ${clientIp}, User-Agent: ${userAgent}`);

  try {
    const response = await axios.get(API_URL);
    const videos = response.data;
 
   videos.forEach((video) => {
      const urlParts = video.url.split('/');
      video.url = urlParts[urlParts.length - 1];
      video.audio = video.audio.replace(/\n/g, '<br>');
      video.video = video.video.replace(/\n/g, '<br>');
   });

    res.render('cfitc', { videos });
  } catch (error) {
    console.error('Error fetching videos:', error);
    res.status(500).send('An error occurred while fetching videos.');
  }
});

app.get('/wzyt', requireAuth, async (req, res) => {
  const clientIp = req.ip;
  const userAgent = req.get('User-Agent');
  console.log(`Client request details: Client IP: ${clientIp}, User-Agent: ${userAgent}`);

  try {
    const response = await axios.get(API_URL_WZYT);
    const videos = response.data;

   videos.forEach((video) => {
      const urlParts = video.url.split('/');
      video.url = urlParts[urlParts.length - 1];
   });

    res.render('wzyt', { videos });
  } catch (error) {
    console.error('Error fetching videos:', error);
    res.status(500).send('An error occurred while fetching videos.');
  }
});

const port = 4000;
app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});

