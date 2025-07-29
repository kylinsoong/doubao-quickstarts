import express from 'express';
import { CozeAPI } from '@coze/api';

const app = express();
app.use(express.json());

const apiClient = new CozeAPI({
  token: process.env.COZE_API_TOKEN,  // Set this in an environment variable
  baseURL: 'https://api.coze.cn'
});

app.post('/chat', async (req, res) => {
  const { message } = req.body;
  try {
    const response = await apiClient.chat.stream({
      bot_id: '7531696470618554419',
      user_id: '7E44664E-74F4-4856-8CAB-E55D3967CD0B',
      additional_messages: [
        { role: 'user', content_type: 'text', content: message }
      ]
    });
    res.json(response);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Chat request failed' });
  }
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});

